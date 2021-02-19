import os
import re
import subprocess
import json

import xdef
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

def runCmd(cmd):
    cmd = '%s %s' %(xdef.cmd, cmd or '')
    print(cmd)
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-geometry', '80x24-50+50', '-display', ':0', '-e', cmd])
    else:
        subprocess.Popen(cmd, shell=True).communicate()

def playURL(player, url, opts=[]):
    cmd = '%s -p %s %s \'%s\'' %(xdef.vod, player, ' '.join(opts), url)
    print(cmd)
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-geometry', '80x24-50+50', '-display', ':0', '-e', cmd])
    else:
        subprocess.Popen(cmd, shell=True)

def sendACT(player, act, num):
    cmd = '%s -p %s \'%s\' \'%s\'' %(xdef.act, player, act, num)
    print(cmd)
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-geometry', '80x24-50+50', '-display', ':0', '-e', cmd]).communicate()
    else:
        subprocess.Popen(cmd, shell=True).communicate()

def getOptionsByCookies(cookies):
    opts = []
    for key in ['format', 'subtitle', 'pagelist', 'dlconf']:
        if key in cookies:
            opts.append('--%s \'%s\'' %(key, cookies[key].value))
    return opts

def handleCmd(cmd):
    cmd = cmd.lower()
    if cmd in ['update']:
        runCmd(cmd)
    else:
        return 'error'
    return 'success'

def entry_play(player, v, cookies=None):
    obj = play_obj(v)
    opts = []
    if cookies:
        opts.extend(getOptionsByCookies(cookies))
    playURL(player, v, opts)
    return json.dumps(obj.__dict__)

def entry_act(player, a, n):
    obj = act_obj(a, n)
    sendACT(player, a, n)
    return json.dumps(obj.__dict__)

def entry_cmd(c):
    status = handleCmd(c)
    obj = cmd_obj(status)
    return json.dumps(obj.__dict__)

