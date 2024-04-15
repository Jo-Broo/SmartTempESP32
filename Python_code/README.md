# Python Code

## Table of Contents
- [MQTT Database Client](#mqtt-database-client)
- [Discord Bot](#discord-bot)

## MQTT Database Client

This neat little tool listens to a, for now hardcoded, topic on the MQTT network. As I mentioned in the [Project README](../README.md), this is a workaround because I found no other way to save things from the MQTT broker to the database.

I experimented here first with the ability to call the script with parameters, but that is not necessary and I will remove this later. Secondly, I experimented with listening for the 'KeyboardInterrupt'. The second feature is really great in my opinion because you can cleanly shut down the software in the testing stage and not just brutally terminate the task :D.

## Discord Bot

**DISCLAIMER:** Before deploying the bot, please note that I tested it on my Windows PC and then transferred the code to my Raspberry Pi. It's important to adjust the code there to correctly read the token. Failure to do so may result in unexpected behavior.


Setting up a Discord bot is optional, but it's really easy with the use of the [Pycord Library](https://docs.pycord.dev/en/stable/), and it's also very convenient to control such a bot.

The tasks/functions the bot has are really easy to meet your requirements.

