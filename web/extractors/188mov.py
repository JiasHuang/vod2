import re

from .utils import *

VALID_URL = r'188mov'

class defs:
    domain = 'https://www.188mov.com'

def extract(url):
    objs = []
    if re.search(r'vod-read-id', url):
        for m in re.finditer(r'href="(/.*?vod-play-id-[^"]*)">(.*?)<', load(url)):
            link = defs.domain + m.group(1)
            title = m.group(2)
            objs.append(entryObj(link, title))
    elif re.search(r'(list-read-id|list-select-id)', url):
        for m in re.finditer(r'<h6><a class="text-light" href="(.*?)">(.*?)</a></h6>', load(url)):
            link = defs.domain + m.group(1)
            title = m.group(2)
            objs.append(pageObj(link, title))
    return objs

def search_188mov(q, start=None):
    objs = []
    url = defs.domain + '/vod-search-wd-%s.html' %(q)
    for m in re.finditer(r'<h6><a class="text-light" href="(.*?)">(.*?)</a></h6>', load(url)):
        link = defs.domain + m.group(1)
        title = m.group(2)
        objs.append(pageObj(link, title))
    return objs

