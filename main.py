import sys, os

def echo(*args):
    print(*args)
    sys.stdout.flush()

echo("--- App Started ---")

import asyncio, discord
client = discord.Client()

import DiscordCommandLineGenerator
CommandLine = DiscordCommandLineGenerator.CommandLine()



@client.event
@asyncio.coroutine
def on_message(message):
    echo(message)


try:
    token = os.environ['TOKEN']
except KeyError:
    # Not on server
    echo("Quit because TOKEN not found.")
    exit()

client.run(token)