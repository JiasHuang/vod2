#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import time

def gethash(local):
    if os.path.exists(local):
        ver = time.strftime('%Y_%m%d_%H%M', time.gmtime(os.path.getmtime(local)))
        print('{} {}'.format(local, ver))
        return ver
    return ''

def main():

    os.chdir('web')

    files = glob.glob("*.js") + glob.glob("*.css")

    for html in glob.glob("*.html"):
        if os.path.islink(html):
            continue
        for f in files:
            ver = gethash(f)
            os.system('sed -i -r \'s/%s([^"]*)/%s\?v=%s/g\' %s' %(f, f, ver, html))

    return

if __name__ == '__main__':
    main()
