# SmartTempESP32

I've come up with an idea for a self-made Home Automation Sensor based on the ESP32 and a Server running on a Raspberry Pi.

My overall intention is to become more comfortable with project documentation and the thinking style that comes with it.

There will be a lot of diagrams at first, but at this point, I already have a working prototype, so the code will follow shortly.

# Why Temperature?

The Temperature Measuring aspect was, at least for me, the easiest to start with, but I already have other ideas such as Watering and Measuring Air Quality. There is really no limit on what you could include here because there are a lot of sensors available for the ESP Platform.

# How does it work?

## ESP32

For the project, I have chosen the ESP32 D1 Mini Board from [AZ-Delivery](https://www.az-delivery.de/products/d1-mini) together with the [DHT-11](https://www.az-delivery.de/products/5-x-dht11-temperatursensor) Temperature and Humidity Sensor. The sensor communicates with the ESP via a One-Wire Bus. The sketch and the wiring will be included in the project.

**Future Goal:** Come up with a Web Interface for the ESP to configure the WiFi and the MQTT parameters. For now, the configuration will be static in the code.

The ESP periodically reads data from the sensor, wraps it up in a JSON format, and then sends the data via the MQTT Protocol to the Raspberry Pi. I just have to come up with a good naming scheme for the MQTT topics, but I will figure that out along the way.

## Raspberry Pi 4

I got the Raspberry Pi from [Reichelt](https://www.reichelt.de/raspberry-pi-4-b-4x-1-5-ghz-4-gb-ram-wlan-bt-rasp-pi-4-b-4gb-p259920.html) and configured a basic x64 Raspberry Pi OS.

The Raspberry Pi is configured to be the MQTT Server and the Database at the same time. I've installed an Apache2 Web Server together with MySQL and PHPMyAdmin for the Database Part, and a Mosquitto MQTT Server. I don't really know, but I've found no real way to get the MQTT Server speaking to the Database, so I worked around it by creating an MQTT Client with Python that saves the Data it receives.

# What to do with the Data ?
I dont really know. As i Mentioned at the beginning maybe a auto watering System would be cool. Ive Heard of Grafana or NodeRed for Data Visualisation but i didnt really look into that, but thats not the difficult part at least i think it isnt.
