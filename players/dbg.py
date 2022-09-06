import os
import re

import xurl
import xsrc

class defvals:
    exe_out_extract = os.path.expanduser('~/bin/exe_out_extract')
    exclude_list = [r'youtube']

def setAct(act, val):
    return

def get_source(url, ref, opts):
    if opts.format != 'bestaudio':
        for p in defvals.exclude_list:
            if re.search(p, url):
                return url, None, ref
    return xsrc.getSource(url, opts.format, ref)

def play(url, ref, opts):
    url, cookies, ref = get_source(url, ref, opts)
    print('[dbg] url {}'.format(url))
    print('[dbg] ref {}'.format(ref))
    if opts.out_extract:
        xurl.saveLocal(opts.out_extract, url)
    if os.path.exists(defvals.exe_out_extract):
        os.system('{} {}'.format(defvals.exe_out_extract, url))
    return

def isRunning():
    return False
