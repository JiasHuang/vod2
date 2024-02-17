#!/usr/bin/python3

import os
import re
import sys
import argparse
import traceback
import ast

import xdef
import xplay
import xsrc
import xurl

def cmd_update():
    os.chdir(xdef.codedir)
    os.system('git pull')
    return

def handle_cmd(cmd):
    if cmd == 'update':
        cmd_update()
    return

def getSettingDefs():
    local = os.path.join(xdef.codedir, 'web', 'settings.js')
    m = re.search(r'var settings = ({.*?});', xurl.readLocal(local), re.DOTALL | re.MULTILINE)
    if m:
        return ast.literal_eval(m.group(1))
    return None

def main():

    url = None
    ref = None

    defs = getSettingDefs()
    os.chdir(xdef.workdir)

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--player', default=xplay.getPlayer())
    parser.add_argument('-f', '--format', default=defs['format']['defs'])
    parser.add_argument('--subtitle', default=defs['subtitle']['defs'])
    parser.add_argument('--pagelist')
    parser.add_argument('--playbackMode')
    parser.add_argument('--dlthreads', default=-1, type=int)
    parser.add_argument('--dlconf', default=defs['dlconf']['defs'])
    parser.add_argument('--forward_url')
    parser.add_argument('--forward_url_ip')
    parser.add_argument('-a', '--act')
    parser.add_argument('-v', '--val')
    parser.add_argument('-c', '--cmd')
    parser.add_argument('-o', '--out_extract')
    args, unparsed = parser.parse_known_args()

    print('[cmd]\n\t' + ' '.join(sys.argv))

    if args.cmd:
        handle_cmd(args.cmd)
        return

    if args.act:
        xplay.setAct(args.act, args.val, args)
        return

    if len(unparsed) >= 1:
        url = unparsed[0].strip()

    if len(unparsed) >= 2:
        ref = unparsed[1].strip()

    if args.dlconf and args.dlthreads == -1:
        for conf in args.dlconf.split(','):
            try:
                c = conf.split('=')
                key = c[0].strip()
                val = c[1].strip()
                if re.search(re.escape(key), url):
                    args.dlthreads = int(val)
            except:
                continue

    try:
        xplay.playURL(url, ref or url, args)
        return
    except:
        print(sys.exc_info())
        traceback.print_tb(sys.exc_info()[2])

    return

if __name__ == '__main__':
    main()
