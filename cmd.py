#!/usr/bin/python3

import os
import re
import sys

import xdef
import xurl

def update():
    os.chdir(xdef.codedir)
    os.system('git pull')
    return

def main():

    if len(sys.argv) < 2:
        return

    cmd = sys.argv[1]

    if cmd == 'update':
        update()

    return

if __name__ == '__main__':
    main()
