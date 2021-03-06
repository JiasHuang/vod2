#!/usr/bin/python3

import re
import os
import configparser

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
from urllib.parse import urlparse, parse_qs, quote, unquote, unquote_plus
from optparse import OptionParser

import view
import page
import xdef
import xurl

opts = None

def get_redirect_location(post_data):
    i = unquote_plus(post_data.decode('utf8'))[2:]
    x = quote(i)
    if i.startswith('#'):
        return 'index.html?c=' + quote(i[1:])
    elif i.startswith('http'):
        return 'index.html?v=' + x
    elif i.startswith('/') and os.path.isdir(i):
        return 'list.html?d=' + x
    elif i.startswith('/') and os.path.exists(i):
        return 'index.html?f=' + x
    else:
        return 'search.html?q=' + x
    print('FAILED TO GET REDIRECT LOCATION ' + i)
    return None

def dispatch_request(s, cookies=None):
    if s.startswith('a='):
        m = re.search(r'a=([^&]*)&n=(.*)', s)
        return view.entry_act(opts.player, m.group(1), m.group(2))
    if s.startswith('c='):
        return view.entry_cmd(s[2:])
    if s.startswith(('v=', 'f=')):
        return view.entry_play(opts.player, s[2:], cookies)
    if s.startswith('p='):
        return page.entry_page(s[2:])
    if s.startswith('j='):
        if s == 'j=':
            return page.entry_json(opts.bookmark)
        return page.entry_json(s[2:])
    if s.startswith('q='):
        m = re.search(r'q=([^&]*)&s=(.*)', s)
        return page.entry_search(m.group(1), m.group(2))
    if s.startswith('d='):
        return page.entry_dir(s[2:])
    print('FAILED TO DISPATCH ' + s)
    return None
 
class VODServer(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_data = self.rfile.read(content_len)
        self.send_response(302)
        self.send_header('Location', get_redirect_location(post_data))
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
            cookies = SimpleCookie(self.headers.get('Cookie'))
            self.send_response(200)
            self.send_header('Content-type', "text/html")
            self.end_headers()
            results = dispatch_request(p.query, cookies)
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
                        self.send_header('Set-Cookie', 'playbackMode=' + xurl.readLocal(xdef.playbackMode))
                    self.end_headers()
                    self.wfile.write(fd.read())
                    return
        self.send_error(404, 'File Not Found: %s' %(self.path))
        return

def main():
    global opts

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    parser = OptionParser()
    parser.add_option("-n", "--hostname", dest="hostname", default=xdef.hostname)
    parser.add_option("-p", "--hostport", type="int", dest="port", default=xdef.hostport)
    parser.add_option("-P", "--player", dest="player")
    parser.add_option("-b", "--bookmark", dest="bookmark", default=xdef.bookmark)
    parser.add_option("-c", "--config", dest="config")
    (opts, args) = parser.parse_args()

    if opts.config:
        parser = configparser.ConfigParser()
        parser.read(opts.config)
        for k in parser['VODServer']:
            setattr(opts, k, parser['VODServer'][k])

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
