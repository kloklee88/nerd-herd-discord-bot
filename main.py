import discord
import os
import nerd_service
import aiocron
from keep_alive import keep_alive

#Flask Server to keep repl.it alive
keep_alive()

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
      return

  #Process message commands
  full_command = message.content.strip().split(' ')
  if message.content.startswith('!nerd'):
    print(full_command)
    if len(full_command) == 2:
      first_command = full_command[1]
      if first_command.startswith('<@!'):
        await message.channel.send(personalized_message(message.mentions[0]))
      elif first_command == 'about':
        await message.channel.send(about())
      elif first_command == 'help':
        await message.channel.send(help())
    else:
      await message.channel.send(help())

  if message.content.startswith('!gme'):
    print(full_command)
    await message.channel.send(gme())

@aiocron.crontab('* * * * *')
async def gme_alert():
  print('Checking GME stock price alert')
  channel = discord.utils.get(client.get_all_channels(), guild__name='Nerd Herd', name='general')
  gme_price = nerd_service.check_gme()
  if(gme_price > 225):
    await channel.send(f'GME Price Alert: {gme_price}')

def personalized_message(mentions):
  return nerd_service.get_personalized_message(mentions)

def about():
  return "A dedicated Discord bot for Nerd Herd server for everything, anything, and nothing :smile:"

def help():
  return 'Commands:\n**!nerd about** -- bot description\n**!nerd @mention** -- where @mention is anybody in the server to receive a random customized message.\n**!gme** -- checks current GME stock price'

def gme():
  return nerd_service.check_gme()

client.run(os.getenv('TOKEN'))