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

def setAct(act, val):

    if act == 'forward' and val:
        cmd = 'seek %s' %(int(val) * 1000000)
    elif act == 'backward' and val:
        cmd = 'seek -%s' %(int(val) * 1000000)
    elif act == 'percent' and val:
        with open(xdef.log, 'r') as fd:
            m = re.search(r'Duration: (.*?):(.*?):(.*?),', fd.read())
            if m:
                duration = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(float(m.group(3)))
                position = duration * int(val) * 1000000 / 100
                cmd = 'setposition %s' %(position)
            else:
                print('Get Duration Fail')
                return
    elif act in ['pause', 'stop']:
        cmd = '%s' %(act)
    else:
        print('unsupported: %s %s' %(act, val))
        return

    print('\n[omxplayer][act]\n\n\t%s%s %s' %(xdef.codedir, 'dbuscontrol.sh', cmd))
    os.system('%s%s %s' %(xdef.codedir, 'dbuscontrol.sh', cmd))
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
        cmd = 'livestreamer --player omxplayer --fifo \'hls://%s\' best 2>&1 | tee %s' %(url, xdef.log)
    else:
        cmd = '%s %s %s \'%s\' 2>&1 | tee %s' %(defvals.prog, defvals.args, ' '.join(args), url, xdef.log)

    print('\n[omx][cmd]\n\n\t'+cmd+'\n')
    os.system(cmd)

    return

def isRunning():
    return xproc.checkProcessRunning(defvals.proc)
