
# Code by Cypooos - Twitter: @cypooos - Revolutions STUDIO 2020

# /----------------------
# | Importation
# \----------------------


import sys, os
import shlex

def echo(*args):
  print(*args)
  sys.stdout.flush()

echo("--- App Started ---")

import asyncio, discord
CLIENT = discord.Client()

import DiscordCommandLineGenerator
CommandLine = DiscordCommandLineGenerator.CommandLine(CLIENT)


# /----------------------
# | Commands of bot
# \----------------------


@CommandLine.addFunction
def ping(**kwargs) -> "ping":
  """
It just answer pong.
  """
  return "pong !"

# /----------------------
# | Bot
# \----------------------


@CLIENT.event
@asyncio.coroutine
async def on_message(message):
  if message.content == "stop":
    exit()
  echo(message.content)
  await message.channel.send(CommandLine.execute(message))



# /----------------------
# | Start
# \----------------------


try:
  token = os.environ['TOKEN']
except KeyError:
  # Not on server
  echo("Quit because TOKEN not found.")
  exit()

CLIENT.run(token)