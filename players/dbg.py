import os
import re

import xurl
import xsrc

class defvals:
    forward_url = os.path.join(os.path.dirname(__file__), 'forward-url.py')
    exclude_list = [r'youtube']

def setAct(act, val):
    return

def get_source(url, ref, opts, exclude_list):
    if exclude_list:
        for p in exclude_list:
            if re.search(p, url):
                return url, None, ref
    return xsrc.getSource(url, opts.format, ref)

def play(url, ref, opts):
    is_video = opts.format != 'bestaudio'
    exclude_list = defvals.exclude_list if is_video else None
    url, cookies, ref = get_source(url, ref, opts, exclude_list)
    print('[dbg] url {}'.format(url))
    print('[dbg] ref {}'.format(ref))
    if opts.out_extract:
        xurl.saveLocal(opts.out_extract, url)
    if opts.forward_url == 'yes':
        os.system('{} {} {}'.format(defvals.forward_url, url))
    return

def isRunning():
    return False
