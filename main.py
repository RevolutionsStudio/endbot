
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

import CommandLineGenerator
CommandLine = CommandLineGenerator.CommandLine()


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


def setToDiscordCommandLine(CL,name="discordCommand"):

  def foo(self,message):
    commandes = message.content.split(";")
    self.vars
    for commande in commandes:
      trt_commande = shlex.split(commande)
      self.cmdReturn = self.__command(trt_commande)
    if self.cmdReturn != None: return self.cmdReturn

  setattr(CL, name, foo)

# Setup the command-line to be Discord compatible
setToDiscordCommandLine(CommandLine,"discordCommand")

@CLIENT.event
@asyncio.coroutine
async def on_message(message):
  echo(message.content)
  await CLIENT.send_message(message.channel, CommandLine.discordCommand(message))


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