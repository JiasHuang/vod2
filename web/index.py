#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import tempfile

from mod_python import util, Cookie

def index(req):

    req.content_type = 'text/html; charset=utf-8'
    form = req.form or util.FieldStorage(req)

    x = req.unparsed_uri.split('?', 1)
    f = os.path.basename(x[0]).replace('.py', '')
    q = x[1]
    o = tempfile.NamedTemporaryFile(delete=False).name

    s = os.path.join(os.path.dirname(__file__), 'server.py')
    cmd = '%s -o %s -e \'%s\'' %(s, o, q)
    if 'cookie' in req.headers_in:
        cmd += ' --cookies \'%s\'' %(req.headers_in['cookie'])

    os.system(cmd)
    with open(o, 'r') as fd:
        txt = fd.read()
        if len(txt):
            req.write(txt)
        else:
            req.write(cmd)
    os.remove(o)

    return

