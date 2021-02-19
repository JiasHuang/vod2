import re

import xurl

from .jsunpack import unpackURL

VALID_URL = r'mixdrop\.co'

def getSource(url, fmt, ref):
    txt = unpackURL(url) or ''
    m = re.search(r'MDCore.wurl="([^"]+)"', txt)
    return xurl.urljoin(url, m.group(1)) if m else None

