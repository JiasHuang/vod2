import re

import xurl

VALID_URL = r'pianku\.tv'

def getSource(url, fmt, ref):
    txt = xurl.load(url)
    m = re.search(r'geturl\(\'(.*?)\'\)', txt)
    return m.group(1) if m else None

