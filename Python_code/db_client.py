import paho.mqtt.client as mqtt
import pymysql.cursors
import sys
import json

if len(sys.argv) < 2:
    print("Keine Parameter erkannt.")
    #sys.exit(1)
    print("Setting up MQTT-Connection...(Standard)")
    mqtt_broker = "localhost"
    mqtt_port = 1883
    mqtt_topic = "/home/sensors"

    print("Setting up DB-Connection...(Standard)")
    mysql_server = "localhost"
    mysql_user = "mqtt"
    mysql_password = "1234"
    mysql_database = "SmartTempESP32"
    mysql_table = "Measurments"
else:
    print("Setting up MQTT-Connection...(Parameter)")
    mqtt_broker = "localhost" if sys.argv[1] == None else sys.argv[1]
    mqtt_port = 1883 if sys.argv[2] == None else int(sys.argv[2])
    mqtt_topic = "/home/sensors" if sys.argv[3] == None else sys.argv[3]

    print("Setting up DB-Connection...(Parameter)")
    mysql_server = "localhost" if sys.argv[4] == None else sys.argv[4]
    mysql_user = "mqtt" if sys.argv[5] == None else sys.argv[5]
    mysql_password = "1234" if sys.argv[6] == None else sys.argv[6]
    mysql_database = "SmartTempESP32" if sys.argv[7] == None else sys.argv[7]
    mysql_table = "Measurments" if sys.argv[8] == None else sys.argv[8]

def on_message(client, userdata, message):
    print(message.topic + " | " + str(message.payload.decode("utf-8")))
    
    payload = message.payload.decode("utf-8")
    data = json.loads(payload)
    print("Recieved JSON data:", data)
    
    with pymysql.connect(host=mysql_server,
                         user=mysql_user,
                         password=mysql_password,
                         database=mysql_database,
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor) as connection:
        with connection.cursor() as cursor:
            sql = "insert into {}(Sensor_ID,Temperature,Humidity) Values('{}',{},{});".format(mysql_table,data["id"],data["t"],data["h"])
            cursor.execute(sql)
            connection.commit()

client = mqtt.Client()
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port)
client.subscribe(mqtt_topic)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print()
    print("KeyboardInterrupt: Exiting...")
    client.unsubscribe(mqtt_topic)
    client.disconnect()
    sys.exit(0)
