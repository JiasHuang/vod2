import re

import xurl

VALID_URL = r'gimy'

def getSource(url, fmt, ref):
    m = re.search(r'"url":"(http[^"]*)"', xurl.load(url))
    if m:
        return m.group(1).replace('\\', '')
    return None
