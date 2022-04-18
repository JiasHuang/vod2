import re

import xurl
from .utils import *

VALID_URL = r'pkmp4'

def extract(url):
    objs = []
    basename = url.split('/')[-1]
    if re.search('/mv/', url):
        for m in re.finditer(r'<li><a href="(.*?)" target="_blank">(.*?)<', load(url)):
            link, title = urljoin(url, m.group(1)), m.group(2)
            objs.append(entryObj(link, title))
    else:
        for m in re.finditer(r'<a href="(.*?)" title="(.*?)" target="_blank"><img src="(.*?)"', load(url)):
            link, title, img = urljoin(url, m.group(1)), m.group(2), urljoin(url, m.group(3))
            objs.append(pageObj(link, title, img))

    return objs
