import re
import subprocess

import xdef
import xurl
import xproc
import xsrc

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
    result = subprocess.check_output('%s%s %s' %(xdef.codedir, 'dbuscontrol.sh', cmd), shell=True)
    print('\n[omxplayer][result]\n\n\t%s' %(result))
    return

def play(url, ref, opts, cookies=None):

    args = '--user-agent=\'%s\'' %(xurl.defvals.ua)

    url, cookies, ref = xsrc.getSource(url, opts.format, ref)

    if not url:
        print('\n[omxplayer][play] invalid url\n')
        return

    if xproc.checkProcessRunning('omxplayer.bin'):
        setAct('stop', None)

    if cookies:
        args = ' '.join([args, '--avdict headers:\"Cookie: %s\"' %(cookies)])

    if re.search(r'/hls_playlist/', url):
        cmd = 'livestreamer --player omxplayer --fifo \'hls://%s\' best 2>&1 | tee %s' %(url, xdef.log)
    else:
        cmd = '%s %s \'%s\' 2>&1 | tee %s' %(xdef.omxplayer, args, url, xdef.log)

    print('\n[omx][cmd]\n\n\t'+cmd+'\n')
    subprocess.Popen(cmd, shell=True).communicate()

    return

def isRunning():
    return xproc.checkProcessRunning('omxplayer.bin')
