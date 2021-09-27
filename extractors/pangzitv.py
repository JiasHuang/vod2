import re
import base64

import xurl

VALID_URL = r'pangzitv\.com'

def getSource(url, fmt, ref):
    if re.search(r'vod-play-id', url):
        try:
            m = re.search(r'num-(\d+)', url)
            ep_num = m.group(1)
            txt = xurl.load(url)
            m = re.search(r'base64decode\(\'([^\']*)', txt)
            code = m.group(1)
            decoded = xurl.unquote(base64.b64decode(code).decode('utf8'))
            # process unicode special character
            decoded = decoded.replace('%u','\\u').encode().decode('unicode_escape')
            print('\n[pangzitv][DBG][decoded]\n\n\t%s' %(decoded))
            urls = []
            for m in re.finditer(r'http[^#$\n]*', decoded):
                urls.append(m.group())
            if len(urls) >= int(ep_num):
                return urls[int(ep_num) - 1]
            return urls[0]
        except:
            print('Exception')
    return None

