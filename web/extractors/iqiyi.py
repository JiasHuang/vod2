import re
import string
import json

import xurl
from .utils import *

VALID_URL = r'iq\.com'

def extract(url):
    objs = []
    if re.search(r'albumList?', url):
        data = json.loads(load(url))
        for x in data['data']['epg']:
            link = 'https://www.iq.com/play/' + x['albumLocSuffix']
            image = x['albumPic']
            title = x['name']
            objs.append(pageObj(link, title, image))
    else:
        for m in re.finditer(r'class="drama-item" href="(.*?)" title="(.*?)"', load(url)):
            link, title = urljoin(url, m.group(1)), m.group(2)
            objs.append(entryObj(link, title))

    return objs

def search_iqiyi(q, start=None):
    objs = []
    url = 'http://www.google.com/search?tbm=vid&num=100&hl=en&q=site%3Aiqiyi.com%20' + xurl.quote(q)
    if start:
        url = url+'&start='+start
    txt = load(url)
    img_codes = re.findall(r'var s=\'([^\']*)\'', txt)
    for m in re.finditer(r'<a href="(http:[^"]*\.iqiyi\.com/\w+\.html)".*?>(.*?)<img id="([^"]*)"', txt):
        link, desc, img_id = m.group(1), m.group(2), m.group(3)
        m2 = re.search(r'<h3.*?>(.*?)</h3>', desc)
        title = m2.group(1) if m2 else None
        m3 = re.search(r'"'+re.escape(img_id)+r'":"([^"]*)"', txt)
        image = m3.group(1) if m3 else None
        idx = int(img_id.strip(string.ascii_letters)) - 1
        if not image and idx < len(img_codes):
            image = img_codes[idx]
        if link and title:
            objs.append(entryObj(link, title, image))

    return objs
