#!/usr/bin/python3

import re
import os
import configparser
import argparse

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
from urllib.parse import urlparse, parse_qs, quote, unquote, unquote_plus

import view
import page
import xdef
import xurl

class defvals:
    section = 'VODServer'

def get_m3u_txt():
    out_extract = '/tmp/out_extract'
    txt = []
    txt.append('#EXTM3U')
    txt.append('#EXT-X-STREAM-INF')
    if os.path.exists(out_extract):
        with open(out_extract, 'r') as fd:
            txt.append(fd.read())
    return '\n'.join(txt)

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

def dispatch_request(args, s, cookies=None):
    if s.startswith('a='):
        m = re.search(r'a=([^&]*)&n=(.*)', s)
        return view.entry_act(args.player, m.group(1), m.group(2))
    if s.startswith('c='):
        return view.entry_cmd(s[2:])
    if s.startswith('v='):
        if cookies and 'forward_url' in cookies and cookies['forward_url'].value == 'yes':
            return view.entry_extract(s[2:], cookies)
        if cookies and 'run_as_extractor' in cookies and cookies['run_as_extractor'].value == 'yes':
            return view.entry_extract(s[2:], cookies)
        return view.entry_play(args.player, s[2:], cookies)
    if s.startswith('f='):
        f = unquote_plus(s[2:])
        return view.entry_play(args.player, f)
    if s.startswith('p='):
        return page.entry_page(s[2:])
    if s.startswith('j='):
        if s == 'j=null':
            return page.entry_json(args.bookmark)
        return page.entry_json(s[2:])
    if s.startswith('q='):
        m = re.search(r'q=([^&]*)&s=(.*)', s)
        return page.entry_search(m.group(1), m.group(2))
    if s.startswith('d='):
        d = unquote_plus(s[2:])
        return page.entry_dir(d)
    if s == 'm3u':
        return get_m3u_txt()
    print('FAILED TO DISPATCH ' + s)
    return None
 
class VODServer(BaseHTTPRequestHandler):
    args = None
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
        if self.path == '/m3u':
            self.send_response(200)
            self.send_header('Content-type', "text/html")
            self.end_headers()
            self.wfile.write(bytes(get_m3u_txt(), 'utf8'))
            return
        p = urlparse(self.path)
        if p.path.endswith('.py'):
            cookies = SimpleCookie(self.headers.get('Cookie'))
            self.send_response(200)
            self.send_header('Content-type', "text/html")
            self.end_headers()
            results = dispatch_request(self.args, p.query, cookies)
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

class LoadConfig(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        cfg = configparser.ConfigParser()
        cfg.read(values)
        for k in cfg[defvals.section]:
            if isinstance(getattr(namespace, k), int):
                setattr(namespace, k, int(cfg[defvals.section][k]))
            elif isinstance(getattr(namespace, k), bool):
                setattr(namespace, k, str2bool(cfg[defvals.section][k]))
            else:
                setattr(namespace, k, cfg[defvals.section][k])

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main():

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--hostname', default=xdef.hostname)
    parser.add_argument('-p', '--hostport', default=xdef.hostport)
    parser.add_argument('-P', '--player')
    parser.add_argument('-b', '--bookmark', default=xdef.bookmark)
    parser.add_argument('-c', '--config', action=LoadConfig)
    parser.add_argument('-v', '--verbose', type=str2bool, nargs='?', const=True, default=False)
    parser.add_argument('-e', '--eval')
    parser.add_argument('-o', '--output')
    parser.add_argument('--cookies')
    args = parser.parse_args()

    if args.eval and args.output:
        # FIXME: set DISPLAY
        if os.path.exists('/usr/bin/xterm'):
            xdef.vod = '/usr/bin/xterm -geometry 80x24-50+50 -display :0 -e ' + xdef.vod
        else:
            xdef.vod = 'DISPLAY=:0 ' + xdef.vod
        with open(args.output, 'w') as fd:
            cookies = SimpleCookie(args.cookies) if args.cookies else None
            fd.write(eval('dispatch_request(args, args.eval, cookies)'))
        return

    VODServer.args = args
    webServer = HTTPServer((args.hostname, args.hostport), VODServer)
    print('VOD Server started http://%s:%s' % (args.hostname, args.hostport))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print('VOD Server stopped.')

    return

if __name__ == '__main__':
    main()
