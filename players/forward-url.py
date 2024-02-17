#!/bin/env python3

import os
import sys

def main():
    remote_ip = sys.argv[1]
    url = sys.argv[2]
    os.system('adb connect {}'.format(remote_ip))
    if url.startswith('https://www.youtube.com/'):
        os.system('adb shell am start -a android.intent.action.VIEW -d {} --activity-clear-top'.format(url))
    else:
        os.system('adb shell am start -a android.intent.action.VIEW -t video/mp4 -d {} --activity-clear-top'.format(url))
    return

if __name__ == '__main__':
    main()
