
# Code by Cypooos - Twitter: @cypooos - Revolutions STUDIO 2020

# /----------------------
# | Importation
# \----------------------


import sys, os
import shlex

def echo(*args):
  print(*args)
  sys.stdout.flush()

echo("Code Started")

import asyncio, discord
CLIENT = discord.Client()

import DiscordCommandLineGenerator
CommandLine = DiscordCommandLineGenerator.CommandLine(CLIENT)

class Config():

  def __init__(self):
    self.roles = {"rasylium":672561014541123612, "revolutions":672561273690390558, "rideos":672561319609761832, "rogemus":672561348751917056}

CONF = Config()
# /----------------------
# | Commands of bot
# \----------------------



@CommandLine.addFunction()
def notification(name:str,**kwargs) -> "notif (Rasylium|Revolutions|Rideos|Rogemus|all)":
  '''Vous donne le role de notification
	'''
  name = name.lower()
  message = CL.message
  if name == "all":
    for x in CONF.roles.values():
      message.author.add_roles(discord.utils.get(message.author.server.roles, id=x))
    return "Tout les rôles ont été atribuées."
  try:
    role = CONF.roles[name]
  except KeyError:
    return "__Erreur:__ Le role `"+name+"` n'est pas dans la liste."
  message.author.add_roles(get(message.author.server.roles, id=role))

# ---- GENRAL COMMANDS ----
@CommandLine.addFunction()
def ping(**kwargs) -> "ping":
  """It just answer pong."""
  return "pong !"

@CommandLine.addFunction("botmoderator")
def stop(**kwargs) -> "stop":
  """Stop the bot.\n To use in case of emergency."""
  quit()

@CommandLine.addFunction()
def echoCMD(name:max,**kwargs) -> "echo *TEXT":
  '''Affiche du texte.
	'''
  return name

@CommandLine.addFunction()
def grab(element:max,**kwargs) -> "grab [*TEXT]":
  """Selectionne et affiche seulement les lignes contenant [*TEXT] à l'interieur, suite à l'execution d'une commande.
Souvent à utillisé avec le séparateur de commande.
	
__Exemple :__ `help; grab ping`"""
  return "\n".join([line for line in CommandLine.cmdReturn.split("\n") if element in line])

@CommandLine.addFunction()
def help(info:(str,""),**kwargs) -> "help [COMMAND|cmd]":
	'''Affiche l'aide d'une commande'''
	if info == "": return "__**Liste des fonctions :**__\n\n"+"\n".join(["> `"+fct.__name__+"`" for fct in CommandLine.funct])+"\n\nTapez `help COMMANDE` pour plus d'informations sur une commande en particulier.\nTapez `help cmd` pour les informations d'utillisation des commandes.*(complexe)*"

	for funct in CommandLine.funct:
		if funct.__name__.split(" ")[0] == info:return "**__AIDE pour "+funct.__name__.split(" ")[0]+":__**\n**Syntaxe:** `"+funct.__name__+"`\n"+"\n"+str(funct.__doc__)
	if info.lower() == "cmd": return """
Vous pouvez aussi executer plusieurs commandes à la suite en utillisant le séparateur `;`.
De cette manière, vous pouvez les combiner.

__Exemple:__
`help;grab echo` : renverra seulement la ligne de l'aide sur la commande echo.

	"""
	return "Commande inconnue.\nTapez `help` pour la liste des commandes.\nTapez `help cmd` pour les informations d'utillisation des commandes.*(complexe)*"

# /----------------------
# | Bot
# \----------------------


@CLIENT.event
async def on_message(message):
  if message.author.id == CLIENT.user.id: return
  if len(message.content)>2 and message.content[0] == "!":
    message.content = message.content[1:]
    await message.channel.send(CommandLine.execute(message))

@CLIENT.event
async def on_ready():
  echo('BOT LOGGED IN !')
  echo("Username: "+CLIENT.user.name)
  echo("ID: "+str(CLIENT.user.id))


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
# if this sentence is modified, it just mean that I need to update the code for refresh the bot on Heraku server