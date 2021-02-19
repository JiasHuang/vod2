import re
import os
import glob

from .utils import entryObj, navObj

mods = []
searches = {}

files = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
for f in files:
    if os.path.isfile(f) and not f.endswith('__.py'):
        name = os.path.basename(f)[:-3]
        __import__('%s.%s' %(__package__, name))
        mod = globals()[name]
        if hasattr(mod, 'VALID_URL') and hasattr(mod, 'extract'):
            mods.append(mod)
        for s in dir(mod):
            if s.startswith('search_'):
                searches[s[7:]] = vars(mod)[s]

def extract(url):
    for m in mods:
        if re.search(m.VALID_URL, url):
            return m.extract(url)
    return None

def extract_debug(url):
    results = extract(url)
    if results:
        for idx, obj in enumerate(results, 1):
            print('%s:' %(idx))
            obj.show()

def search(q, s=None, x=None):
    s = s or 'youtube'
    if s in searches:
        return searches[s](q, x)
    return None

def search_debug(q, s='youtube', x=None):
    results = search(q, s, x)
    if results:
        for idx, obj in enumerate(results, 1):
            print('%s:' %(idx))
            obj.show()

