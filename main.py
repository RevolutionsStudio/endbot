import sys, os

def echo(*args):
    print(*args)
    sys.stdout.flush()

echo("--- App Started ---")

echo(os.environ['TOKEN'])