import sys
import json
import subprocess

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def loadJson(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def calcFuelCost(dist, a, b):
    return a * dist + b * (dist ** 2)

def runCommand(cmd):
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        eprint(f"[BŁĄD] {e.returncode}:")
        eprint(f"Polecenie: {' '.join(cmd)}")
        eprint(f"--- ERROR ---")
        eprint(e.stderr)
        eprint(f"----------------------------")
        sys.exit(1)
