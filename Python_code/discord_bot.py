# Doku
# https://docs.pycord.dev/en/master/

# Für den nächsten Stream 
# Tic Tac Toe
# 4 gewinnt
# umfragen 
# wetten
# led Matrix kontrollieren 

import discord
import json

token = ""
with open('Y:\\token.json','r') as f:
    token = json.load(f)

bot = discord.Bot()

@bot.event
async def on_ready():
        print(f"{bot.user} ist online")

@bot.event
async def on_message(msg):
        if msg.author.bot:
                return

        await msg.channel.send("Ich hab deine Nachricht gelesen und antworte jetzt.")

bot.run(token["token"])