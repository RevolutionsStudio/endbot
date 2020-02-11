
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
async def notification(name:str,**kwargs) -> "notif (Rasylium|Revolutions|Rideos|Rogemus|all)":
  '''Vous donne un role de notification.
Si un role est déja présent, il sera retirer *(sauf dans le cas de `notif all`, ou quoiqu'il ce passe, tout les roles sont ajouter)*.
	'''
  name = name.lower()
  message = CommandLine.message
  if name == "all":
    for x in CONF.roles.values():
      await message.author.add_roles(discord.utils.get(message.author.guild.roles, id=x))
    return "Tout les rôles ont été atribuées."
  try:
    role = CONF.roles[name]
  except KeyError:
    return "__Erreur:__ Le role `"+name+"` n'est pas dans la liste."
  role = discord.utils.get(message.author.guild.roles, id=role)
  if role not in message.author.roles:
    await message.author.add_roles(role)
    return "Le role <@&"+str(role.id)+"> vous a été ajouté !"
  else:
    await message.author.remove_roles(role)
    return "Le role <@&"+str(role.id)+"> vous a été retiré !"

# ---- DEBUGS COMMAND ----

@CommandLine.addFunction("botmoderator")
async def evaluate(commands:max,**kwargs) -> "eval *PYTHON":
  """Execute du code python.
Execute du code python.
**A éviter !** une fausse manip pourrais casser le bot ou détruire des données.
**IL N'Y A PAS DE RETOUR EN ARRIERE POSSIBLE**
Prévenir <@349114853333663746> en cas de problème."""
  
  return "__Return:__\n```python\n"+eval(commands)+"```\n"

@CommandLine.addFunction()
async def ping(**kwargs) -> "ping":
  """Répond `pong !`
Répond `pong !`"""
  await CommandLine.message.channel.send("Pong !")


# ---- GENERAL COMMANDS ----

@CommandLine.addFunction("botmoderator")
async def stop(**kwargs) -> "stop":
  """Arrete le bot.
A utilliser en cas d'urgence: spam, crash, ou incontrollable.
Prévenir <@349114853333663746> en cas de problème."""
  await CommandLine.message.channel.send("Bye !")
  quit()

@CommandLine.addFunction()
async def help(info:(str,""),**kwargs) -> "help [COMMAND|cmd]":
  '''Affiche l'aide d'une commande.
Affiche de l'aide sur une commande, ou sur les commandes en général.
Les aides sont détaillé au possible, en utillisant la syntaxe usuele.
Tapez `help cmd` pour une aide sur le fonctionnement des commandes'''
  message = CommandLine.message
  if info == "":
    embed_cmdUti=discord.Embed(title="__Liste des commandes utilisateurs__", color=0x80ffff)
    
    embed_cmdUti.add_field(name="Nom", value="\n".join(["`"+fct.__name__.split(" ")[0]+"`" for fct in CommandLine.funct if fct.authGroup == None]), inline=True)
    embed_cmdUti.add_field(name="Description", value="\n".join([fct.__doc__.split("\n")[0] for fct in CommandLine.funct if fct.authGroup == None]), inline=True)

    embed_cmdAdm=discord.Embed(title="__Liste des commandes administrateurs__", color=0xfb0013)

    embed_cmdAdm.add_field(name="Nom", value="\n".join(["`"+fct.__name__.split(" ")[0]+"`" for fct in CommandLine.funct if fct.authGroup != None]), inline=True)
    embed_cmdAdm.add_field(name="Description", value="\n".join([fct.__doc__.split("\n")[0] for fct in CommandLine.funct if fct.authGroup != None]), inline=True)

    embed_cmdUti.set_thumbnail(url="https://media3.giphy.com/media/B7o99rIuystY4/source.gif")
    embed_cmdAdm.set_thumbnail(url="https://media3.giphy.com/media/B7o99rIuystY4/source.gif")
    embed_cmdAdm.set_footer(text="Le bot EndBot a été créé par Cyprien Bourotte, du studio Révolutions")
    await message.channel.send(embed=embed_cmdUti)
    await message.channel.send(embed=embed_cmdAdm)
    return 

  for funct in CommandLine.funct:
    if funct.__name__.split(" ")[0] == info:
      # HELP FUNCTION
      embed=discord.Embed(title="Commande : "+funct.__name__.split(" ")[0], description=str("\n".join(funct.__doc__.split("\n")[1:])), color=0x80ffff)
      embed.set_author(name="Aide")
      embed.set_thumbnail(url="https://media1.giphy.com/media/IQ47VvDzlzx9S/giphy.gif")
      embed.add_field(name="Syntaxe :", value="`"+funct.__name__+"`", inline=False)
      if funct.authGroup != None: embed.set_footer(text="Cette commande n'est utilisable seulement avec le role "+str(funct.authGroup.upper()))
      await message.channel.send(embed=embed)
      return 
  if info.lower() == "cmd":
    embed=discord.Embed(title="__Aide sur l'utillisation des commandes__", description="Les messages qui sont des commandes doivent commancer par `!`\nVous pouvez aussi executer plusieurs commandes à la suite en utillisant le séparateur `;`.\nSeulement le retour de la dernière commande sera affiché.", color=0xfbe800)
    embed.add_field(name="Exemple :", value="`!notif all;notif rogemus` : Donera tout les rôles sauf le rôle Rogemus", inline=False)
    embed.set_thumbnail(url="https://media1.giphy.com/media/IQ47VvDzlzx9S/giphy.gif")
    embed.set_footer(text="Le bot EndBot a été créé par Cyprien Bourotte, du studio Révolutions.")
    await message.channel.send(embed=embed)
    return 
  return "Commande pour l'aide inconnue.\nTapez `help` pour la liste des commandes.\nTapez `help cmd` pour les informations d'utillisation des commandes."

# /----------------------
# | Bot
# \----------------------


@CLIENT.event
async def on_message(message):
  if message.author.id == CLIENT.user.id: return
  if len(message.content)>2 and message.content[0] == "!":
    message.content = message.content[1:]
    ret = await CommandLine.execute(message)
    if ret != None and ret != "": await message.channel.send(ret)

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
# if this sentence is modified, it just mean that I need to update the code for refresh the bot on Heraku server.