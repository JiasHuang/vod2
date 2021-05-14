#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from mod_python import util, Cookie

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
    print('FAILED TO GET REDIRECT LOCATION ' + i)
    return None

def index(req):

    req.content_type = 'text/html; charset=utf-8'
    form = req.form or util.FieldStorage(req)

    i = form.get('i', None)

    if i:
        loc = get_redirect_location(i)
        util.redirect(req, loc)

    return

