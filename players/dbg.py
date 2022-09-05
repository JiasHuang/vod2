import os
import re

import xurl
import xsrc

def setAct(act, val):
    return

def play(url, ref, opts):
    url, cookies, ref = xsrc.getSource(url, opts.format, ref)
    print('[dbg] url {}'.format(url))
    print('[dbg] ref {}'.format(ref))
    if opts.out_extract:
        xurl.saveLocal(opts.out_extract, url)
    return

def isRunning():
    return False
