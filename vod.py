#!/usr/bin/python3

import os
import re
import sys
import traceback
import ast

import xdef
import xplay
import xsrc
import xurl

from optparse import OptionParser

def cmd_update():
    os.chdir(xdef.codedir)
    os.system('git pull')
    return

def handle_cmd(cmd):
    if cmd == 'update':
        cmd_update()
    return

def getSettingDefs():
    local = xdef.codedir + 'web/settings.js'
    m = re.search(r'var settings = ({.*?});', xurl.readLocal(local), re.DOTALL | re.MULTILINE)
    if m:
        return ast.literal_eval(m.group(1))
    return None

def main():

    url = None
    ref = None

    defs = getSettingDefs()
    os.chdir(xdef.workdir)

    parser = OptionParser()
    parser.add_option("-p", "--player", dest="player", default=xplay.getPlayer())
    parser.add_option("-f", "--format", dest="format", default=defs['format']['defs'])
    parser.add_option("--subtitle", dest="subtitle", default=defs['subtitle']['defs'])
    parser.add_option("--pagelist", dest="pagelist")
    parser.add_option("--playbackMode", dest="playbackMode")
    parser.add_option("--dl-threads", dest="dl_threads")
    parser.add_option("--dlconf", dest="dlconf", default=defs['dlconf']['defs'])
    parser.add_option("-a", "--act", dest="act")
    parser.add_option("-v", "--val", dest="val")
    parser.add_option("-c", "--cmd", dest="cmd")
    (opts, args) = parser.parse_args()

    if opts.cmd:
        handle_cmd(opts.cmd)
        return

    if opts.act:
        xplay.setAct(opts.act, opts.val, opts)
        return

    if len(args) >= 1:
        url = args[0].strip()

    if len(args) >= 2:
        ref = args[1].strip()

    if opts.dlconf and not opts.dl_threads:
        for conf in opts.dlconf.split(','):
            try:
                c = conf.split('=')
                key = c[0].strip()
                val = c[1].strip()
                if re.search(re.escape(key), url):
                    opts.dl_threads = val
            except:
                continue

    try:
        xplay.playURL(url, ref or url, opts)
        return
    except:
        print(sys.exc_info())
        traceback.print_tb(sys.exc_info()[2])

    return

if __name__ == '__main__':
    main()
