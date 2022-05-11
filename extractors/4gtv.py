import re
import subprocess
import os
import signal

import xurl

VALID_URL = r'4gtv'

def getSource(url, fmt, ref):
    result = None
    cmd = 'google-chrome-stable --headless --disable-gpu --enable-logging --v=1 --virtual-time-budget=30000 --timeout=30000 \'%s\'' %(url)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    for line in p.stdout:
        m = re.search(r'https://4gtvfree-cds.cdn.hinet.net/.*', line.decode('utf8'))
        if m:
            result = m.group(0)
            break
    p.terminate()
    return result
