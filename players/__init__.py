import os
import glob

mods = {}

files = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
for f in files:
    if os.path.isfile(f) and not os.path.islink(f) and not f.endswith('__.py'):
        name = os.path.basename(f)[:-3]
        __import__('%s.%s' %(__package__, name))
        mods.update({name:globals()[name]})

class player:
    def __init__(self, n):
        if n not in mods:
            raise ValueError('Invalid Player Name')
        self.n = n
    def isRunning(self):
        return mods[self.n].isRunning()
    def play(self, url, ref, opts):
        mods[self.n].play(url, ref, opts)
        return
    def setACT(self, act, val):
        mods[self.n].setACT(act, val)
        return
