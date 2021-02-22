import os
import re

import xdef
import xsrc
import xproc

class defvals:
    prog = 'ffplay'
    args = '-fs -window_title ffplay'

def setAct(act, val):

    if not isRunning():
        print('\n[ffplay][secAct] no running')
        return

    wid = xproc.checkOutput('xdotool search --name ffplay', r'([0-9]*)$')
    if not wid:
        print('\n[ffplay][secAct] no wid')
        return

    os.system('xdotool windowactivate --sync %s' %(wid))

    if act == 'stop':
        os.system('xdotool key q')
    elif act == 'pause':
        os.system('xdotool key p')
    elif act == 'forward':
        os.system('xdotool key Up')
    elif act == 'backward':
        os.system('xdotool key Down')
    elif act == 'percent' and val:
        geometry = xproc.checkOutput('xdotool getwindowgeometry %s' %(wid), r'Geometry: ([0-9x]*)')
        if not geometry:
            print('\n[ffplay][setAct] no geometry')
            return
        w = int(geometry.split('x')[0])
        h = int(geometry.split('x')[1])
        x = str(w * int(val) / 100)
        y = str(h / 2)
        os.system('xdotool mousemove --sync --window %s %s %s click 1' %(wid, x, y))
    else:
        print('\n[ffplay][setAct] unsupported: %s %s' %(act, val))
    return

def play(url, ref, opts):

    args = []

    url, cookies, ref = xsrc.getSource(url, opts.format, ref)

    if not url:
        print('\n[ffplay][play] invalid url')
        return

    if cookies:
        args.append('-headers "Cookie: %s"' %(cookies))

    if isRunning():
        setAct('stop', None)

    cmd = '%s %s %s \'%s\'' %(defvals.prog, defvals.args, ' '.join(args), url)
    print('\n[ffplay][cmd]\n\n\t'+cmd+'\n')
    os.system(cmd)

    return

def isRunning():
    return xproc.checkProcessRunning(defvals.prog)
