import re

from .jsunpack import unpackURL

VALID_URL = r'up2stream\.com'

def getSource(url, fmt, ref):
    txt = unpackURL(url) or ''
    m = re.search(r'http://([^"]+)', txt)
    return m.group() if m else None

