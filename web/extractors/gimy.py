import re

from .utils import *

VALID_URL = r'gimy'

def extract(url):
    objs = []
    if re.search(r'/cat/', url):
        for m in re.finditer(r'data-original="([^"]*)" href="([^"]*)" title="([^"]*)"', load(url)):
            image = m.group(1)
            link = urljoin(url, m.group(2))
            title = m.group(3)
            objs.append(pageObj(link, title, image))
    elif re.search(r'/vod/', url):
        for x in re.finditer(r'<li><a rel="follow" href="([^"]*)">(.*?)</a></li>', load(url)):
            link = urljoin(url, x.group(1))
            title = x.group(2)
            objs.append(videoObj(link, title))
    return objs

def search_gimy(q, start=None):
    objs = []
    url = 'https://gimy.app/search/-------------.html?wd=' + q
    for m in re.finditer(r'href="([^"]*)" title="([^"]*)" data-original="([^"]*)"', load(url)):
        link = urljoin(url, m.group(1))
        title = m.group(2)
        image = m.group(3)
        objs.append(pageObj(link, title, image))
    return objs
