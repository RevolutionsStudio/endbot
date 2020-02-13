import shlex
import sys
import asyncio
import discord 
def echo(*args):
  print(*args)
  sys.stdout.flush()

# La classe de la ligne de commande
class CommandLine():

  def __init__(self,client,config,**kwargs):
    self.funct = []
    self.client = client
    self.CONF = config
    self.cmdReturn = ""
    self.vars = {}  

    self.__msgUnknow = kwargs.get("unknow","La commande est inconnue.\nTapez `!help` pour obtenir la liste des commandes")
    self.__msgWrgParam = kwargs.get("wrongParameter","Le parametre $ doit etre $$")
    self.__paramList = kwargs.get("parameterList",["Vrai/Faux","du texte","un nombre","un float"])
    self.__haveMsgError = kwargs.get("commandErrorFeedback",True)
    self.__msgArguments = kwargs.get("argumentsError","Vous n'avez pas le bon nombre de paramètres.")

    self.__cmdErrorFeedback = kwargs.get("commandErrorFeedback",True)
    self.__debug = kwargs.get("debug",True)

    self.activeSymbol = kwargs.get("activeSymbol","=> ")
  
  def setVars(self,kwargs):
    self.vars = kwargs

  def addFunction(self,authGroup=None,caller = None) -> "Methode de passage":
    def inner(funct) -> "retourne la nouvelle fonction":

      def newFunct(*arg,**kwargs) -> "Nouvelle fonction":
        # On rajoute le code de tester si les arguments sont bons
        new_args = []
        i = 0

        for annot in list(funct.__annotations__.values()):

          if annot == max:
            param = " ".join(list(arg)[i:])
            new_args.append(param)
            break
          try:
            param = arg[i]
          except:
            if isinstance(annot,tuple):
              try:
                if not isinstance(annot[0],arg[i]): param = annot[0]
                else:param = annot[1]
              except IndexError: param = annot[1]
            else: raise AssertionError(self.__msgArguments)
          if annot == "return": pass
          elif annot == None:
            pass
          
            # Oblige d'avoir un argument
          elif annot == bool:
            try: param = bool(param)
            except:raise AssertionError(self.__msgWrgParam.replace("$",param).replace("$$",self.__paramList[0]))
          elif annot == str:
            try: param = str(param)
            except:raise AssertionError(self.__msgWrgParam.replace("$",param).replace("$$",self.__paramList[1]))
          elif annot == int:
            try: param = int(param)
            except:raise AssertionError(self.__msgWrgParam.replace("$",param).replace("$$",self.__paramList[2]))
          elif annot == float:
            try: param = float(param)
            except: raise AssertionError(self.__msgWrgParam.replace("$",param).replace("$$",self.__paramList[3]))
          new_args.append(param)
          i+=1
        return funct(*tuple(new_args),**kwargs) # Si tout est bon, on execute la fonction


      # Ajout au dictionnaire de la fonction
      newFunct.caller = caller # ajout du contexte self
      newFunct.authGroup = authGroup # ajout de la sécurité concernant le role à avoir pour la commande
      self.funct.append(newFunct)
      self.funct[self.funct.index(newFunct)].__name__ = funct.__annotations__.pop("return")
      self.funct[self.funct.index(newFunct)].__doc__ = funct.__doc__
      
      if self.__debug: print("Called for "+funct.__name__+", arguments is "+", ".join([i+":"+str(x) for i,x in funct.__annotations__.items()]))
      return newFunct # On retourne notre meilleure fonction.
    return inner


  async def execute(self,message):
    commandes = message.content.split(";")
    if len(commandes) > 4 and not self.CONF.isAdmin(message.author):
      embed=discord.Embed(title="TUTUTUTUTU.", description="Vous utillisez trop de commande.\nLa limite est de 4 ", color=0xfb0013)
      embed.set_thumbnail(url="https://media.tenor.com/images/a4fd1165d9d64832bc2b0fda3ecdf0e1/tenor.gif")
      await message.channel.send(embed=embed)
      return
    self.message = message
    for commande in commandes:
      trt_commande = commande.split(" ")
      self.cmdReturn = await self.__command(trt_commande,[y.name.lower() for y in message.author.roles])
    if self.cmdReturn != None: return self.cmdReturn

  def start(self):
    if self.__debug: print("\n"*10)
    print(self.__msgStart)

  # executer une commande
  async def __command(self,execute,userRole=[]):
    if isinstance(execute,str):execute = execute.split(" ") # if argument not in list, conversion to list

    if execute == []: return None # is command is empty
    returning = None 
    find = False
    for funct in self.funct: # for every command register
      if funct.__name__.split(" ")[0] == execute[0]: # Found the command
        allow = funct.authGroup == None
        if not allow:
          for x in [y.name.lower() for y in self.message.author.roles]:
            if x in funct.authGroup:allow = True;
        if allow: # if role right to command AUTH
          try:
            if funct.caller: # Call the function w/ the caller
              returning = await funct(funct.caller,*execute[1:],**self.vars)
            else: # call the function without
              returning = await funct(*execute[1:],**self.vars) # if courotine, await it
          except AssertionError as err: # if argument error
            returning = "Erreur d'argument:\n"+str(err)
          finally:
            find = True # we found the function
        else:
          embed=discord.Embed(title="Vous n'avez pas accès à cette commande.", description="Cette commande n'est utilisable seulement avec le role "+str(" ou ".join(funct.authGroup).lower()), color=0xfb0013)
          embed.set_thumbnail(url="https://media.tenor.com/images/a4fd1165d9d64832bc2b0fda3ecdf0e1/tenor.gif")
          await message.channel.send(embed=embed)
          return 
    if not find: # if we havn't find the function
      returning = self.__msgUnknow # echoing the error message
    return returning
