
# Code by Cypooos - Twitter: @cypooos - Revolutions STUDIO 2020

# /----------------------
# | Importation
# \----------------------


import sys, os
import shlex
import com.log as log

LATENCY = []

from time import gmtime, strftime
import asyncio, discord
CLIENT = discord.Client()

def echo(*arg):
  print(*arg)
  sys.stdout.flush()

class Config():

  def __init__(self):
    self.roles = {"rasylium":672561014541123612, "revolutions":672561273690390558, "rideos":672561319609761832, "rogemus":672561348751917056,"discord":676757120003080223}
    self.adminRoles = ["botmoderator","administrateurs"]
    self.logChannel = 677859982087159828
  
  def isAdmin(self,user):
    returning = False
    for x in [y.name.lower() for y in user.roles]:
      if x in self.adminRoles:returning = True;
    return returning
  
  def canBeUse(self,funct,user):
    allow = funct.authGroup == None
    if not allow:
      for x in [y.name.lower() for y in user.roles]:
        if x in funct.authGroup:allow = True;
    return allow

  async def send_warn(self,title,reason,message):
    await LOG.warn("de <@"+str(message.author.id)+">, titre: "+title+"\nReason: "+reason)
    embed=discord.Embed(title=title, description=reason, color=0xfb0013)
    embed.set_author(name="TUTUTUTU")
    embed.set_thumbnail(url="https://media.tenor.com/images/a4fd1165d9d64832bc2b0fda3ecdf0e1/tenor.gif")
    embed.set_footer(text="Ce message ce détruira au bout de 3 secondes.")
    to_destroy = await message.channel.send(embed=embed)
    await message.delete()
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, delete(to_destroy,3))

CONF = Config()

import DiscordCommandLineGenerator
CommandLine = DiscordCommandLineGenerator.CommandLine(CLIENT,CONF)


# /----------------------
# | Commands of bot
# \----------------------

# ---- COMMAND'S COMMAND ---
async def delete(message,time):
  await asyncio.sleep(time)
  await message.delete()
  await CommandLine.message.channel.send("Deleted")




# ---- General commands ----

@CommandLine.addFunction()
async def notification(name:str,**kwargs) -> "notif (Rasylium|Revolutions|Rideos|Rogemus|discord|all)":
  '''Enlève ou rajoute un rôle.
Si un rôle est déja présent, il sera retirés *(sauf dans le cas de `notif all`, ou quoiqu'il ce passe, tout les rôles sont ajoutés)*.
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


@CommandLine.addFunction()
async def invite(**kwargs) -> "invite":
  """Donne le lien d'invitation
Donne le liens d'invitation."""
  embed=discord.Embed(title="Invitation", url="https://discord.gg/fFhrv8a", color=0xf2ff06)
  embed.set_thumbnail(url="https://www.stickpng.com/assets/images/5897ac11cba9841eabab6165.png")
  embed.add_field(name="__**Lien :**__", value="https://discord.gg/fFhrv8a", inline=True)
  await CommandLine.message.channel.send(embed=embed)

@CommandLine.addFunction()
async def speak(text:max,**kwargs) -> "speak *MESSAGE":
  """Parle à ta place 
Tapez un message et il l'envoie !"""
  embed=discord.Embed(title="Message de "+CommandLine.message.author.name,description=text, color=0xf2ff06)
  await CommandLine.message.channel.send(embed=embed)
  await CommandLine.message.delete()




# ---- DEBUGS COMMAND ----
@CommandLine.addFunction(["botmoderator"])
async def evaluate(commands:max,**kwargs) -> "eval *PYTHON":
  """Execute du code python.
Execute du code python.
**A éviter !** une fausse manip pourrais casser le bot ou détruire des données.
**IL N'Y A PAS DE RETOUR EN ARRIERE POSSIBLE**
Prévenir <@349114853333663746> en cas de problème."""
  try:
    ret = eval(commands)
  except:
    ret = sys.exc_info()[0]
  return "__Return:__\n```python\n"+ret+"```\n"


@CommandLine.addFunction()
async def ping(**kwargs) -> "ping":
  """Répond `pong !`
Répond `pong !`"""
  await CommandLine.message.channel.send("Pong !")



# ---- ADMINS COMMANDS ----
@CommandLine.addFunction(CONF.adminRoles)
async def stop(**kwargs) -> "stop":
  """Arrête le bot.
A utilliser en cas d'urgence: spam, crash, ou incontrollable.
Prévenir <@349114853333663746> en cas de problème."""
  await CommandLine.message.channel.send("Bye !")
  quit()

@CommandLine.addFunction(CONF.adminRoles)
async def deleteCmd(nbMsg:(int,1),**kwargs) -> "delete [INT]":
  """Supprimme X messages.
Ne rien indiqué surprimme le dernier message. Nous ne comptons pas la commande dans le nombre message."""
  nbMsg += 1
  async for message in CommandLine.message.channel.history(limit=int(nbMsg)):
    await message.delete()
  




# ---- HELP COMMAND ----
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
    if CONF.isAdmin(message.author):await message.channel.send(embed=embed_cmdAdm)
    return "Je t'incite à faire `!help COMMANDE` pour plus d'infos, ou encore `!help cmd` pour des informations complémentaire"

  for funct in CommandLine.funct:
    if funct.__name__.split(" ")[0] == info:
      if CONF.canBeUse(funct,message.author):
        # HELP FUNCTION
        embed=discord.Embed(title="Commande : "+funct.__name__.split(" ")[0], description=str("\n".join(funct.__doc__.split("\n")[1:])), color=0x80ffff)
        embed.set_author(name="Aide")
        embed.set_thumbnail(url="https://media1.giphy.com/media/IQ47VvDzlzx9S/giphy.gif")
        embed.add_field(name="Syntaxe :", value="`"+funct.__name__+"`", inline=False)
        if funct.authGroup != None: embed.set_footer(text="Cette commande n'est utilisable seulement avec le role "+str(" ou ".join(funct.authGroup).lower()))
        await message.channel.send(embed=embed)
        return 
      else:
        # DONT ALLOW
        embed=discord.Embed(title="Vous n'avez pas accès à cette commande.", description="Cette commande n'est utilisable seulement avec le role "+str(" ou ".join(funct.authGroup).lower()), color=0xfb0013)
        embed.set_thumbnail(url="https://media.tenor.com/images/a4fd1165d9d64832bc2b0fda3ecdf0e1/tenor.gif")
        await message.channel.send(embed=embed)
        return
  if info.lower() == "cmd":
    embed=discord.Embed(title="__Aide sur l'utillisation des commandes__", description="Les messages qui sont des commandes doivent commancer par `!`\nVous pouvez aussi executer plusieurs commandes à la suite en utillisant le séparateur `;`.\nSeulement le retour de la dernière commande sera affiché.", color=0xfbe800)
    embed.add_field(name="Exemple :", value="`!notif all;notif rogemus` : Donera tout les rôles sauf le rôle Rogemus", inline=False)
    embed.set_thumbnail(url="https://media1.giphy.com/media/IQ47VvDzlzx9S/giphy.gif")
    embed.set_footer(text="Le bot EndBot a été créé par Cyprien Bourotte, du studio Révolutions.")
    await message.channel.send(embed=embed)
    return 
  return "Commande pour l'aide inconnue.\nTapez `!help` pour la liste des commandes.\nTapez `help cmd` pour les informations d'utillisation des commandes."



# /----------------------
# | Bot
# \----------------------

async def checkCommand(message):
  if CONF.isAdmin(message.author):return True
  if "\n" in message.content:await CONF.send_warn("Les commandes sont en une ligne !","Sinon, c'est limite du spam.",message);return False
  if len(message.content)>200:await CONF.send_warn("Les commandes sont en moins de 200 charactères !","Encore, ça fais beaucoup là non ?\nTu en as tant besoin que cela ?",message);return False
  if len(message.content.split(";")) > 4:await CONF.send_warn("Vous utillisez trop de commandes.","La limite est de 4.\nTu en as tant besoin que cela ?",message);return False
  return True


@CLIENT.event
async def on_message(message):
  if message.author.id != CLIENT.user.id: await LOG.message("<@!"+str(message.author.id)+"> "+message.content)
  if isinstance(message.channel,discord.DMChannel): await message.channel.send("Je ne marche pas en privé, veuillez envoyer votre commande dans <#676549676916539517>")


  elif len(message.content)>2 and message.content[0] == "!":
    message.content = message.content[1:]
    if not await checkCommand(message):return # SECURITY
    ret = await CommandLine.execute(message)
    if ret != None and ret != "": await message.channel.send(ret)
  


@CLIENT.event
async def on_ready():
  global LOG
  LOG = log.Log(CLIENT.get_channel(CONF.logChannel))
  await LOG.info("Username: "+CLIENT.user.name+";    ID: "+str(CLIENT.user.id))


# /----------------------
# | Start
# \----------------------


try:
  token = os.environ['TOKEN']
except KeyError:
  # Not on server
  echo("Exit because TOKEN not found")
  exit()

echo("TOKEN:",token)

CLIENT.run(token)
# if this sentence is modified, it just mean that I need to update the code for refresh the bot on Heraku server.