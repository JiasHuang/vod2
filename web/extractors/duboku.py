import re

from .utils import *

VALID_URL = r'duboku'

def extract(url):
    objs = []
    if re.search(r'/vodshow/', url):
        for m in re.finditer(r'href="([^"]*)" title="([^"]*)" data-original="([^"]*)">', load(url)):
            link = urljoin(url, m.group(1))
            title = m.group(2)
            image = m.group(3)
            objs.append(pageObj(link, title, image))
    elif re.search(r'/voddetail/', url):
        for m in re.finditer(r'<a class="btn btn-default" href="([^"]*)">([^<]*)</a>', load(url)):
            link = urljoin(url, m.group(1))
            title = m.group(2)
            objs.append(videoObj(link, title))
    return objs

def search_duboku(q, start=None):
    objs = []
    url = 'https://www.duboku.tv/vodsearch/-------------.html?wd=' + q
    for m in re.finditer(r'href="([^"]*)" title="([^"]*)" data-original="([^"]*)"', load(url)):
        link = urljoin(url, m.group(1))
        title = m.group(2)
        image = m.group(3)
        objs.append(pageObj(link, title, image))
    return objs
