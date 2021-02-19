import re
import json

from .utils import *

VALID_URL = r'api\.cntv\.cn'

def extract(url):
    objs = []
    txt = load(url)
    try:
        data = json.loads(txt)
        for d in data['data']['list']:
            title, image, url = darg(d, 'title', 'image', 'url')
            objs.append(entryObj(url, title, image, video=False))
    except:
        print('Exception:\n'+txt)

    return objs
