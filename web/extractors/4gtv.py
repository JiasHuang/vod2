import re
import json

from .utils import *

VALID_URL = r'4gtv'

def extract(url):
    objs = []
    m = re.search(r'/GetVodIndex/(\w+)/', url)
    if m:
        vodtype = m.group(1)
        data = json.loads(load(url))
        for d in data['Data']:
            link = 'https://www.4gtv.tv/{}/{}'.format(vodtype, d['VODID'])
            title = d['Title']
            image = d['HeadFrame']
            objs.append(pageObj(link, title, image))
    elif re.search(r'/GetChannelBySetId/', url):
        data = json.loads(load(url))
        for d in data['Data']:
            link = 'https://www.4gtv.tv/channel_sub.html?channelSet_id=4&asset_id={}&channel_id={}'.format(d['fs4GTV_ID'], d['fnID'])
            title = d['fsNAME']
            image = d['fsHEAD_FRAME']
            objs.append(entryObj(link, title, image))
    else:
        for m in re.finditer(r'<a href=\'([^\']*)\' title=\'([^\']*)\'>', load(url)):
            link = urljoin(url, m.group(1))
            title = m.group(2)
            objs.append(entryObj(link, title))
    return objs
