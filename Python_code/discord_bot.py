# Doku
# https://docs.pycord.dev/en/master/

# Für den nächsten Stream 
# Tic Tac Toe
# 4 gewinnt
# umfragen 
# wetten
# led Matrix kontrollieren (fertig)
# Datenbankabfragen machen (fertig)
# Command für mich als Admin um den Bot auszuschalten
# Command für mich als Admin um das Messintervall zu setzen/abzufragen
# Datenbank auswertung

# !Logging implementieren!

import discord
import json
from discord.ext import commands
import socket
import pymysql.cursors
import os

# Config for ESP (Matrix)
ESP32_IP = "192.168.178.26"
ESP32_PORT = 80

# Config for Bot Token
script_dir = os.path.dirname(os.path.abspath(__file__))
token_file = os.path.join(script_dir, 'token.json')

token = ""
with open(token_file,'r') as f:
    token = json.load(f)
bot = discord.Bot()

# Config for DB
mysql_server = "192.168.178.40"
mysql_user = "mqtt"
mysql_password = "1234"
mysql_database = "SmartTempESP32"
mysql_table = "Measurments"

@bot.event
async def on_ready():
        print(f"{bot.user} ist online")

# @bot.event
# async def on_message(msg):
#         if msg.author.bot:
#                 return

#         await msg.channel.send(f"Hallo {msg.author.name} ✌😜.")
#         await msg.add_reaction("💻")

# Ping zum Bot
@bot.command(description="Sendet die Latenz zum Bot") # this decorator makes a slash command
async def ping(ctx): # a slash command will be created with the name "ping"
        await ctx.respond(f"Pong! Die Latenzzeit berträgt: {round(bot.latency,2)} ms")
    
# Befehl zum Steuern der physischen LED-Matrix
@bot.command(description="Kontrolliert die LED-Matrix")
async def matrix(ctx, index, r, g, b):
        response = ""
        
        led_data = {}
        led_data["led"] = index
        led_data["r"] = r
        led_data["g"] = g
        led_data["b"] = b
        json_data = json.dumps(led_data)

        #print(json_data)

        try:
                # Try sending
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((ESP32_IP, ESP32_PORT))

                client_socket.sendall(json_data.encode())
                response = "Die Anfrage wurde erfolgreich bearbeitet"
                #print("Daten erfolgreich gesendet:", json_data)

        except Exception as e:
                response = f"Die Anfrage konnte nicht erfolgreich bearbeitet werden.| {e}"
                #print("Fehler beim Senden der Daten:", e)

        finally:
                if 'client_socket' in locals():
                        client_socket.close()
                await ctx.responde(response)
     
# Datenbank auswertung
# vlt sollte ich die DB erst pingen bevor ich eine abfrage versuche
@bot.command(description="Zeigt eine Datenbank auswertung")
async def auswertung(ctx):
        # === Datenbankauswertung ===
        # Anzahl der Einträge: []
        # Wärmster Messpunkt: []
        # Kältester Messpunkt: []
        # Letzter Messpunkt: []
        number_of_records = await get_from_DB("select max(ID) as 'Count' from {};".format(mysql_table))
        max_t = await get_from_DB("select max(Temperature) as 'max_t' from {};".format(mysql_table))
        min_t = await get_from_DB("select min(Temperature) as 'min_t' from {}".format(mysql_table))
        result = await get_from_DB("select ID, DateTime, Temperature, Humidity from {} order by ID desc limit 1;".format(mysql_table))

        if(number_of_records["Error"] != None or max_t["Error"] != None or min_t["Error"] != None or result["Error"] != None):
                await ctx.respond("Es ist ein Fehler in der Abfrage aufgetreten.")
                return

        response = """=== Datenbankauswertung ===
Anzahl der Einträge: {}
Wärmster Messpunkt: {} °C
Kältester Messpunkt: {} °C""".format(number_of_records["Count"],max_t["max_t"],min_t["min_t"])
        response += "\nLetzter Eintrag: [ {} | {} | {} °C | {} % ]".format(result["ID"],result["DateTime"].strftime("%d.%m.%Y, %H:%M"),result["Temperature"],result["Humidity"])
        await ctx.respond(response)

# Gibt den letzen Messeintrag aus der Datenbank aus
@bot.command(description="Fragt den letzten Eintrag aus der Datenbank ab")
async def last(ctx):
        result = await get_from_DB("select ID, DateTime, Temperature, Humidity from {} order by ID desc limit 1;".format(mysql_table))
        response = "Letzter Eintrag: [ {} | {} | {} °C | {} % ]".format(result["ID"],result["DateTime"].strftime("%d.%m.%Y, %H:%M"),result["Temperature"],result["Humidity"])
        await ctx.respond(response)

# Das soll ein Command nur für mich als Admin werden um den Bot aus der ferne ausschalten zu könnnen
@bot.command(description="Fragt den letzten Eintrag aus der Datenbank ab")
async def shutdown(ctx):
        ctx.respond("Hier steht im Moment noch nichts.")

# Hilfsfunktion zum verarbeiten von SQL's 
async def get_from_DB(query):
        result = {}
        result["Error"] = "True"
        try:
                with pymysql.connect(host=mysql_server,
                        user=mysql_user,
                        password=mysql_password,
                        database=mysql_database,
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor) as connection:
                        with connection.cursor() as cursor:
                                cursor.execute(query)
                                result = cursor.fetchone()
        except Exception as e:
                print(f"Hier ist leider ein Fehler aufgetreten.[{e}]")
        finally:
                return result

bot.run(token["token"])

