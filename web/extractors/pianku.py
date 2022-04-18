import re

import xurl
from .utils import *

VALID_URL = r'pianku'

def extract(url):
    objs = []
    basename = url.split('/')[-1]
    if re.search('/detail/', url):
        for m in re.finditer(r'<a class="btn btn-default" href="(.*?)">(.*?)</a>', load(url)):
            link, title = urljoin(url, m.group(1)), m.group(2)
            objs.append(entryObj(link, title))
    else:
        for m in re.finditer(r'href="(.*?)" title="(.*?)" data-original="(.*?)"', load(url)):
            link, title, img = urljoin(url, m.group(1)), m.group(2), m.group(3)
            objs.append(pageObj(link, title, img))

    return objs
