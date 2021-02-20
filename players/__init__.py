import os
import glob

mods = {}

files = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
for f in files:
    if os.path.isfile(f) and not os.path.islink(f) and not f.endswith('__.py'):
        name = os.path.basename(f)[:-3]
        __import__('%s.%s' %(__package__, name))
        mods.update({name:globals()[name]})

def isRunning(player):
    if player in mods:
        return mods[player].isRunning()
    return False

def play(player, url, ref, opts):
    if player in mods:
        mods[player].play(url, ref, opts)
    return

def setACT(player, act, val):
    if player in mods:
        mods[player].setACT(act, val)
    return
