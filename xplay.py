import os
import re
import subprocess
import hashlib
import dl

from multiprocessing import Process

import xdef
import xproc
import xurl
import xsrc
import players

def getPlayer():
    if re.search(r'raspberrypi', subprocess.check_output('uname -a', shell=True).decode('utf8')):
        return 'omxplayer'
    if os.path.exists('/usr/bin/mpv') or os.path.exists('/usr/local/bin/mpv'):
        return 'mpv'
    if os.path.exists('/usr/bin/ffplay'):
        return 'ffplay'
    return 'err'

def nextLine(playing, playlist):
    try:
        lines = playlist.splitlines()
        index = lines.index(playing)
        return lines[(index + 1) % len(lines)]
    except:
        return None

def getNext(playing, playlist):

    if playlist != xurl.readLocal(xdef.playlist):
        return None

    playbackMode = xurl.readLocal(xdef.playbackMode).lower()

    if playbackMode == 'loopone':
        return playing

    if playbackMode in ['autonext', 'loopall']:
        return nextLine(playing, playlist)

    return None

def playURL_core(url, ref, opts):

    print('\n[xplay][%s]\n' %(opts.player))
    print('\turl : %s' %(url or ''))
    print('\tref : %s' %(ref or ''))

    if url == None or url == '':
        return

    xurl.saveLocal(xdef.playing, url)

    player = players.player(opts.player)
    player.play(url, ref, opts)

    return

def playURL(url, ref, opts):
    if opts.dlthreads > 0:
        src, cookies, ref = xsrc.getSource(url, opts.format, ref)
        url = dl.createJobs(src, xdef.dldir, opts.dlthreads)

    player = players.player(opts.player)

    if player.isRunning():
        if os.path.exists(xdef.playlist):
            playbackMode = xurl.readLocal(xdef.playbackMode).lower()
            if len(playbackMode) > 0 and playbackMode != 'normal':
                os.remove(xdef.playlist)
                setAct('stop', None, opts)

    if opts.playbackMode:
        xurl.saveLocal(xdef.playbackMode, opts.playbackMode)

    if opts.pagelist:
        playlist = xurl.readLocal(opts.pagelist)
        xurl.saveLocal(xdef.playlist, playlist)
        while url != None:
            nextURL = getNext(url, playlist)
            if nextURL:
                p = Process(target=xsrc.getSource, args=(nextURL, opts.format))
                p.start()
                playURL_core(url, ref, opts)
                p.join()
            else:
                playURL_core(url, ref, opts)
            url = ref = getNext(url, playlist)
    else:
        playURL_core(url, ref, opts)

    return

def checkActVal(act, val):

    if act == 'percent':
        if not val:
            return False
        if int(val) < 0 or int(val) > 100:
            return False

    return True

def setAct(act, val, opts):

    if checkActVal(act, val) == False:
        print('\n[xplay][setAct] invalid command: %s %s\n' %(act, val))
        return

    if act == 'stop' and val != '#':
        if os.path.exists(xdef.playlist):
            os.remove(xdef.playlist)

    if act == 'playbackMode':
        xurl.saveLocal(xdef.playbackMode, val)
        if val.lower() in ['autonext', 'loopall']:
            playing = xurl.readLocal(xdef.playing)
            playlist = xurl.readLocal(xdef.playlist)
            nextURL = nextLine(playing, playlist)
            if nextURL:
                if os.fork() == 0:
                    xsrc.getSource(nextURL, opts.format)
        return

    player = players.player(opts.player)

    print('\n[xplay][setAct]\n\n\t'+ '%s,%s,%s' %(player.n, act, val))

    if player.isRunning():
        return player.setAct(act, val)

