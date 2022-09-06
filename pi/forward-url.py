#!/bin/env python3

import os
import sys

def main():
    url = sys.argv[1]
    os.system('adb connect 192.168.0.101')
    if url.startswith('https://www.youtube.com/'):
        os.system('adb shell am start -a android.intent.action.VIEW -d {} --activity-clear-top -i VOD'.format(url))
    else:
        os.system('adb shell am start -a android.intent.action.VIEW -t video/mp4 -d {} --activity-clear-top -i VOD'.format(url))
    return

if __name__ == '__main__':
    main()
