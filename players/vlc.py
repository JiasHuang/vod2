import os
import re

import xdef
import xurl
import xproc
import xsrc
import xurl

class defvals:
    prog = 'vlc'
    port = '9090'
    args = '-I rc --rc-host :%s --no-video-title-show -f' %(port)
    dest = 'nc -q0 127.0.0.1 %s' %(port)

def setAct(act, val):
    if act == 'forward' and val:
        os.system('echo seek +%s | %s' %(val, defvals.dest))
    elif act == 'backward' and val:
        os.system('echo seek -%s | %s' %(val, defvals.dest))
    elif act == 'percent' and val:
        os.system('echo seek %s | %s' %(val+'%', defvals.dest))
    elif act in ['pause', 'stop']:
        os.system('echo %s | %s' %(act, defvals.dest))
    elif act == 'add':
        os.system('echo add \'%s\' | %s' %(val, defvals.dest))
    else:
        print('unsupported: %s %s' %(act, val))
    return

def play(url, ref, opts, cookies=None):

    args = ['--http-user-agent=\'%s\'' %(xurl.defvals.ua)]

    url, cookies, ref = xsrc.getSource(url, opts.format, ref)

    if not url:
        print('\n[vlc][play] invalid url\n')
        return

    if isRunning():
        setAct('add', url)
        return

    cmd = '%s %s %s \'%s\'' %(defvals.prog, defvals.args, ' '.join(args), url)
    print('\n[vlc][cmd]\n\n\t'+cmd+'\n')
    os.system(cmd)

    return

def isRunning():
    return xproc.checkProcessRunning(defvals.prog)
