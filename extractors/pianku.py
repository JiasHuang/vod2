import re

import xurl

VALID_URL = r'pkmp4'

def getSource(url, fmt, ref):
    txt = xurl.load(url)
    m = re.search(r'"url":"(.*?)","url_next":"(.*?)"', txt)
    return m.group(1).replace('\\', '') if m else None

