import os
import re
import subprocess
import json

import conf
import xurl

class play_obj:
    def __init__(self, video):
        self.type = 'play'
        self.video = video

class act_obj:
    def __init__(self, act='', num=''):
        self.type = 'act'
        self.act = act
        self.num = num

class cmd_obj:
    def __init__(self, status):
        self.type = 'cmd'
        self.status = status

def search(pattern, txt, flags=0):
    if not txt:
        return None
    m = re.search(pattern, txt, flags)
    if m:
        return m.group(1)
    return None

def runCmd(cmd):
    if not os.path.exists(conf.vod):
        return
    cmd = '%s %s' %(conf.cmd, cmd or '')
    print(cmd)
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-geometry', '80x24-50+50', '-display', ':0', '-e', cmd])
    else:
        subprocess.Popen(cmd, shell=True).communicate()

def playURL(url, opt=None):
    if not os.path.exists(conf.vod):
        return
    cmd = '%s \'%s\' %s' %(conf.vod, url, opt or '')
    print(cmd)
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-geometry', '80x24-50+50', '-display', ':0', '-e', cmd])
    else:
        subprocess.Popen(cmd, shell=True)

def sendACT(act, num):
    if not os.path.exists(conf.act):
        return
    cmd = '%s \'%s\' \'%s\'' %(conf.act, act, num)
    print(cmd)
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-geometry', '80x24-50+50', '-display', ':0', '-e', cmd]).communicate()
    else:
        subprocess.Popen(cmd, shell=True).communicate()

def getOptionByCookies(cookies):
    opt = []
    for key in ['format', 'subtitle', 'pagelist', 'dlconf']:
        if key in cookies:
            opt.append('--%s \'%s\'' %(key, cookies[key].value))
    return ' '.join(opt)

def handleCmd(cmd):
    cmd = cmd.lower()
    if cmd in ['update', 'updatedb']:
        os.system('rm -f '+conf.workdir+'vod_*')
        runCmd(cmd)
    else:
        return 'error'
    return 'success'

def entry_play(v, cookies=None):
    obj = play_obj(v)
    opt = None
    if cookies:
        opt = getOptionByCookies(cookies)
    playURL(v, opt)
    return json.dumps(obj.__dict__)

def entry_act(a, n):
    obj = act_obj(a, n)
    sendACT(a, n)
    return json.dumps(obj.__dict__)

def entry_cmd(c):
    status = handleCmd(c)
    obj = cmd_obj(status)
    return json.dumps(obj.__dict__)

