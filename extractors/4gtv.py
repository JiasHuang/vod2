import re
import subprocess

import xurl

VALID_URL = r'4gtv'

def getSource(url, fmt, ref):
    cmd = 'google-chrome-stable --headless --disable-gpu --enable-logging --v=1 --virtual-time-budget=8000 --timeout=8000 \'%s\'' %(url)
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode('utf8')
    m = re.search(r'https://4gtvfree-cds.cdn.hinet.net/.*', output)
    if m:
        return m.group(0)
    return None
