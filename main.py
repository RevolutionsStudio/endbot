import sys, os
import discord.py

import CommandLineGenerator

CommandLine = CommandLineGenerator.CommandLine()

def echo(*args):
    print(*args)
    sys.stdout.flush()

echo("--- App Started ---")




echo(os.environ['TOKEN'])