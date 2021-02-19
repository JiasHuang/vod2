#!/usr/bin/python3

import re
import os

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, unquote
from optparse import OptionParser

import conf
import view
import page
import xurl

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
        return 'search.html?q=' + re.sub('\s+', ' ', i)

def dispatch_request(s):
    if s.startswith('a='):
        m = re.search(r'a=([^&]*)&n=(.*)', s)
        return view.entry_act(m.group(1), m.group(2))
    if s.startswith('c='):
        return view.entry_cmd(s[2:])
    if s.startswith(('v=', 'f=')):
        return view.entry_play(s[2:])
    if s.startswith('p='):
        return page.entry_page(s[2:])
    if s.startswith('j='):
        return page.entry_json(s[2:])
    if s.startswith('q='):
        m = re.search(r'q=([^&]*)&s=(.*)', s)
        return page.entry_search(m.group(1), m.group(2))
    if s.startswith('d='):
        return page.entry_dir(s[2:])
    print('FAILED TO DISPATCH ' + s)
    return None
 
class VODServer(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_data = self.rfile.read(content_len)
        arg = unquote(post_data.decode('utf8'))[2:]
        self.send_response(302)
        self.send_header('Location', get_redirect_location(arg))
        self.end_headers()
        return
    def do_GET(self):
        if self.path == '/':
            self.send_response(302)
            self.send_header('Location', 'index.html')
            self.end_headers()
            return
        p = urlparse(self.path)
        if p.path in ['/view', '/load']:
            self.send_response(200)
            self.send_header('Content-type', "text/html")
            self.end_headers()
            results = dispatch_request(p.query)
            self.wfile.write(bytes(results, 'utf8'))
            return
        if p.path.endswith(('.css', '.js', '.html', '.png', '.gif')):
            local = os.path.abspath(os.curdir) + p.path
            if os.path.exists(local):
                with open(local, 'rb') as fd:
                    self.send_response(200)
                    if local.endswith('.css'):
                        self.send_header('Content-type', 'text/css')
                    elif local.endswith('.js'):
                        self.send_header('Content-type', 'application/javascript')
                    elif local.endswith('.png'):
                        self.send_header('Content-type', 'image/png')
                    elif local.endswith('.gif'):
                        self.send_header('Content-type', 'image/gif')
                    else:
                        self.send_header('Content-type', "text/html")
                        self.send_header('Set-Cookie', 'playbackMode=' + xurl.readLocal(conf.playbackMode))
                    self.end_headers()
                    self.wfile.write(fd.read())
                    return
        self.send_error(404, 'File Not Found: %s' %(self.path))
        return

def main():

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    parser = OptionParser()
    parser.add_option("-p", "--port", type="int", dest="port", default=8080)
    parser.add_option("-n", "--hostname", dest="hostname", default="")
    (opts, args) = parser.parse_args()

    webServer = HTTPServer((opts.hostname, opts.port), VODServer)
    print('VOD Server started http://%s:%s' % (opts.hostname, opts.port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print('VOD Server stopped.')

    return

if __name__ == '__main__':
    main()
