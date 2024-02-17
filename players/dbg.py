import os
import re

import xurl
import xsrc

class defvals:
    exclude_list = [r'youtube']

def setAct(act, val):
    return

def get_source(url, ref, opts, exclude_list):
    if exclude_list:
        for p in exclude_list:
            if re.search(p, url):
                return url, None, ref
    return xsrc.getSource(url, opts.format, ref)

def forward_url(remote_ip, url):
    os.system('adb connect {}'.format(remote_ip))
    if url.startswith('https://www.youtube.com/'):
        os.system('adb shell am start -a android.intent.action.VIEW -d {} --activity-clear-top'.format(url))
    else:
        os.system('adb shell am start -a android.intent.action.VIEW -t video/mp4 -d {} --activity-clear-top'.format(url))
    return

def play(url, ref, opts):
    is_video = opts.format != 'bestaudio'
    exclude_list = defvals.exclude_list if is_video else None
    url, cookies, ref = get_source(url, ref, opts, exclude_list)
    print('[dbg] url {}'.format(url))
    print('[dbg] ref {}'.format(ref))
    print('[dbg] opts {}'.format(opts))
    if opts.out_extract:
        xurl.saveLocal(opts.out_extract, url)
    if opts.forward_url == 'yes':
        forward_url(opts.forward_url_ip, url)
    return

def isRunning():
    return False
