#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import cgi
import cgitb

def get_redirect_location(i):
    if i.startswith('#'):
        return 'index.html?c=' + i[1:]
    elif i.startswith('http'):
        return 'index.html?v=' + i
    elif i.startswith('/') and os.path.isdir(i):
        return 'list.html?d=' + i
    elif i.startswith('/') and os.path.exists(i):
        return 'index.html?f=' + i
    else:
        return 'search.html?q=' + i

def main():
    args = cgi.FieldStorage()
    loc = get_redirect_location(args.getvalue('i'))
    print('Location: {}\n'.format(loc))
    return

cgitb.enable()
main()
