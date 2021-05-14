import os
import re

import xdef
import xurl
import xproc
import xsrc

class defvals:
    prog = 'omxplayer'
    proc = 'omxplayer.bin'
    args = '-b -o both -I'
    dbus = os.path.join(xdef.codedir, 'dbuscontrol.sh')

def setAct(act, val):

    if act == 'forward' and val:
        cmd = 'seek %s' %(int(val) * 1000000)
    elif act == 'backward' and val:
        cmd = 'seek -%s' %(int(val) * 1000000)
    elif act == 'percent' and val:
        output = xproc.checkOutput('%s status' %(defvals.dbus))
        m = re.search(r'Duration: (\d*)', output)
        if m:
            duration = int(m.group(1))
            position = duration * int(val) / 100
            cmd = 'setposition %s' %(position)
        else:
            print('Get Duration Fail')
            return
    elif act in ['pause', 'stop']:
        cmd = '%s' %(act)
    else:
        print('unsupported: %s %s' %(act, val))
        return

    print('\n[omxplayer][act]\n\n\t%s %s' %(defvals.dbus, cmd))
    os.system('%s %s' %(defvals.dbus, cmd))
    return

def play(url, ref, opts, cookies=None):

    args = ['--user-agent=\'%s\'' %(xurl.defvals.ua)]

    url, cookies, ref = xsrc.getSource(url, opts.format, ref)

    if not url:
        print('\n[omxplayer][play] invalid url\n')
        return

    if isRunning():
        setAct('stop', None)

    if cookies:
        args.append('--avdict headers:\"Cookie: %s\"' %(cookies))

    if re.search(r'/hls_playlist/', url):
        cmd = 'livestreamer --player omxplayer --fifo \'hls://%s\' best' %(url)
    else:
        cmd = '%s %s %s \'%s\'' %(defvals.prog, defvals.args, ' '.join(args), url)

    print('\n[omx][cmd]\n\n\t'+cmd+'\n')
    os.system(cmd)

    return

def isRunning():
    return xproc.checkProcessRunning(defvals.proc)
