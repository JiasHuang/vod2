import os
import re
import subprocess
import json

import xdef
import xurl

class play_obj:
    def __init__(self, video, opts=None):
        self.type = 'play'
        self.video = video
        self.opts = opts

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
    cmd = '%s -c %s' %(xdef.vod, cmd)
    subprocess.Popen(cmd, shell=True)

def playURL(url, opts=[]):
    cmd = '%s %s \'%s\'' %(xdef.vod, ' '.join(opts), url)
    subprocess.Popen(cmd, shell=True)

def sendACT(act, num, opts):
    cmd = '%s %s -a \'%s\' -v \'%s\'' %(xdef.vod, ' '.join(opts), act, num)
    os.system(cmd)

def getOptionsByCookies(cookies):
    opts = []
    for key in ['format', 'subtitle', 'pagelist', 'dlconf', 'playbackMode']:
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
    if player:
        opts.append('-p ' + player)
    playURL(v, opts)
    obj.opts = opts
    return json.dumps(obj.__dict__)

def entry_act(player, a, n):
    obj = act_obj(a, n)
    opts = []
    if player:
        opts.append('-p ' + player)
    sendACT(a, n, opts)
    return json.dumps(obj.__dict__)

def entry_cmd(c):
    status = handleCmd(c)
    obj = cmd_obj(status)
    return json.dumps(obj.__dict__)

def entry_extract(v, fmt):
    # FIXME
    if fmt not in ['bestaudio']:
        fmt = 'bestvideo'
    cmd = 'yt-dlp -q -g -f %s \'%s\'' %(fmt, v)
    url = subprocess.check_output(cmd, shell=True)
    obj = play_obj(url.decode('utf8'))
    return json.dumps(obj.__dict__)
