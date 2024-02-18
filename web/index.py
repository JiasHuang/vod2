#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import tempfile
import cgi
import cgitb

def main():

    print('Content-type:text/html\n')

    args = cgi.FieldStorage()
    func_args = []

    for k in args.keys():
        func_args.append('{}={}'.format(k, args.getvalue(k)))

    func = os.path.basename(__file__).replace('.py', '')
    tmpf = tempfile.NamedTemporaryFile(delete=False).name
    server = os.path.join(os.path.dirname(__file__), 'server.py')
    cmd = '%s -o %s -e \'%s\'' %(server, tmpf, '&'.join(func_args))

    if 'HTTP_COOKIE' in os.environ:
        cmd += ' --cookies \'%s\'' %(os.environ['HTTP_COOKIE'])

    os.system(cmd)
    with open(tmpf, 'r') as fd:
        print(fd.read())
    os.remove(tmpf)

    return

cgitb.enable()
main()
