import re
import subprocess
import os
import signal

import xurl

VALID_URL = r'4gtv'

def getSource(url, fmt, ref):
    result = None
    cmd = 'google-chrome-stable --headless --disable-gpu --enable-logging --v=1 --virtual-time-budget=90000 \'%s\'' %(url)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    for line in p.stdout:
        l = line.decode('utf8')
        m = re.search(r'https://4gtvfree-cds.cdn.hinet.net/.*', l)
        if m:
            result = m.group(0)
            break
        m = re.search(r'https://4gtvfreepc-mozai.4gtv.tv/.*', l)
        if m:
            result = m.group(0)
            break
    p.terminate()
    return result
