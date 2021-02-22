import os
import re

import xdef
import xurl
import xproc
import xsrc
import xurl

class defvals:
    prog = 'vlc'
    passwd = '__p_a_s_s_w_o_r_d__'
    port = '9090'
    args = '-I http --http-port %s --http-password %s --no-video-title-show -f' %(port, passwd)
    intf = 'http://127.0.0.1:%s/requests/status.xml?command=' %(port)

def setAct(act, val):

    intf = defvals.intf

    if act == 'forward' and val:
        intf += 'seek&val=' + xurl.quote('+' + val)
    elif act == 'backward' and val:
        intf += 'seek&val=' + xurl.quote('-' + val)
    elif act == 'percent' and val:
        intf += 'seek&val=' + xurl.quote(val + '%')
    elif act in ['pause', 'stop']:
        intf += 'pl_' + act
    elif act == 'in_play':
        intf += 'in_play&input=' + xurl.quote(val)
    else:
        print('unsupported: %s %s' %(act, val))
        return

    if not len(xurl.load(intf, opts=['-u :'+defvals.passwd], cache=False)):
        print('failed to setAct')

    return

def play(url, ref, opts, cookies=None):

    args = ['--http-user-agent=\'%s\'' %(xurl.defvals.ua)]

    url, cookies, ref = xsrc.getSource(url, opts.format, ref)

    if not url:
        print('\n[vlc][play] invalid url\n')
        return

    if isRunning():
        setAct('in_play', url)
        return

    cmd = '%s %s %s \'%s\'' %(defvals.prog, defvals.args, ' '.join(args), url)
    print('\n[vlc][cmd]\n\n\t'+cmd+'\n')
    os.system(cmd)

    return

def isRunning():
    return xproc.checkProcessRunning(defvals.prog)
