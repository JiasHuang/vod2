import re
import subprocess

import xproc
import xurl

from .youtubedl import extractURL

VALID_URL = r'dailymotion\.com'

def getRedirectLink(url):
    cmd = 'curl -I \"%s\"' %(url)
    output = xproc.checkOutput(cmd)
    cookies = []
    cookies_str = None
    for m in re.finditer('Set-Cookie: (.*?)(\n|\r)', output):
        cookies.append(m.group(1))
    if len(cookies) > 0:
        cookies_str = '; '.join(cookies)
    m = re.search('Location: (.*?)\n', output)
    if m:
        return m.group(1), cookies_str
    return url, None

def removeHashTag(url):
    m = re.search('(.*?)#', url)
    if m:
        return m.group(1)
    return url

def getSource(url, fmt, ref):
    src, cookies = extractURL(url, fmt)
    src, extra_cookies = getRedirectLink(src)
    src = removeHashTag(src)
    if extra_cookies:
        cookies = extra_cookies
    return (src, cookies, url)

