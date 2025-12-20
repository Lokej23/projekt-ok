import sys
import json

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def loadJson(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def calcFuelCost(dist, a, b):
    return a * dist + b * (dist ** 2)