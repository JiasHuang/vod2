#!/usr/bin/python3

import os
import re
import subprocess
import time
import hashlib
import argparse

import xurl
import xsrc

def isM3U(url):
    parsed = xurl.urlparse(url)
    if len(parsed.netloc) > 0:
        if xurl.getContentType(url).lower() in ['application/vnd.apple.mpegurl', 'application/x-mpegurl', 'audio/x-mpegurl']:
            return True
        if parsed.path.endswith('/index.m3u8'):
            return True
    elif os.path.exists(url):
        if re.search(r'#EXTM3U', xurl.readLocal(url)):
            return True
    return False

def getM3U8Variants(url):
    best_var = url
    best_bw = -1
    for m in re.finditer(r'#EXT-X-STREAM-INF:(.*?)\n(.*?)\s', xurl.load(url)):
        bw = 0
        var = m.group(2)
        m_bw = re.search(r'BANDWIDTH=(\d+)', m.group(1))
        if m_bw:
            bw = int(m_bw.group(1))
        if bw > best_bw:
            best_var = xurl.urljoin(url, var)
            best_bw = bw
    return best_var

def genLocal(url):
    return 'vod_dl_' + hashlib.md5(url.encode('utf8')).hexdigest() + '.' + os.path.basename(url)

def filter(url, flt):

    local = genLocal(url)

    parsed = xurl.urlparse(url)
    if len(parsed.netloc) > 0:
        txt = xurl.load(url, local)
    else:
        txt = xurl.readLocal(url)

    m = re.search(r'#EXT-X-KEY:METHOD=AES-128,URI="(.*?)"', txt)
    if m and not m.group(1).startswith('http'):
        txt = txt.replace(m.group(1), xurl.urljoin(url, m.group(1)))

    newtxt = txt
    results = []
    for m in re.finditer(flt, txt):
        if re.compile(flt).groups > 0:
            link = xurl.urljoin(url, m.group(1))
        else:
            link = xurl.urljoin(url, m.group())
        if link not in results:
            basename = os.path.basename(xurl.urlparse(link).path)
            newtxt = newtxt.replace(m.group(1), basename)
            results.append(link)
    xurl.saveLocal(local, newtxt)
    return results

def genName(name, suffix, sn):
    i = int(sn)
    while os.path.exists("%s_%03d.%s" %(name , i, suffix)):
        i += 1
    return '%s_%03d.%s' %(name, i, suffix)

def dl(url, args):
    if args.execute == 'ytdl':
        cmd = 'yt-dlp \'%s\'' %(url)
        return subprocess.Popen(cmd, shell=True)
    elif args.execute == 'ffmpeg':
        src, cookie, ref = xsrc.getSource(url)
        local = genName(args.name, args.type, args.sn)
        cmd = 'ffmpeg -i \'%s\' -vcodec copy -acodec copy %s' %(src, local)
        return subprocess.Popen(cmd, shell=True)
    elif args.execute == 'wget':
        basename = os.path.basename(xurl.urlparse(url).path)
        cmd = 'wget -qc -o /dev/null -O %s \'%s\'' %(basename, url)
        return subprocess.Popen(cmd, shell=True)
    elif args.execute == 'curl':
        basename = os.path.basename(xurl.urlparse(url).path)
        cmd = 'curl -kLs -C - -o %s \'%s\'' %(basename, url)
        return subprocess.Popen(cmd, shell=True)
    elif args.cmd:
        cmd = '%s \'%s\'' %(args.cmd, url)
        return subprocess.Popen(cmd, shell=True)
    else:
        return None

def waitJobs(procs, args):
    while len(procs) >= int(args.jobs):
        time.sleep(0.1)
        for p in procs:
            if p.poll() != None:
                p.communicate()
                procs.remove(p)
                break
    return procs

def getM3U8Stat(local):
    dls = 0
    dlsz = 0
    files = 0
    dldir = os.path.dirname(local)
    for m in re.finditer(r'#EXTINF:.*?\n(.*?)\n', xurl.readLocal(local)):
        f = os.path.join(dldir, m.group(1))
        if os.path.exists(f):
            dls += 1
            dlsz += os.path.getsize(f)
        files += 1
    return dls, dlsz, files

def waitM3U8Ready(local, min_dls = 4, min_dlsz = 10485760, verbose = False):
    while True:
        dls, dlsz, files = getM3U8Stat(local)
        if verbose:
            print('waiting jobs ... (dls %s/%s dlsz %s)' %(dls, files, dlsz))
        if files > 0 and dls == files:
            break
        if dls > min_dls or dlsz > min_dlsz:
            break
        time.sleep(2)

def createJobs(url, dldir, jobs, wait_complete=False):
    prog = os.path.realpath(__file__)
    if prog.endswith('.pyc'):
        prog = prog[:-1]

    if isM3U(url):
        url = getM3U8Variants(url)

    local = dldir + genLocal(url)

    procs = subprocess.check_output('ps aux', shell=True).decode('utf8')
    pattern = '%s -i %s' %(os.path.basename(prog), url)
    if re.search(re.escape(pattern), procs):
        return local

    if isM3U(url):
        flt = '#EXTINF:.*?\n(.*?)\n'
        cmd = '%s -i \'%s\' -c %s -f \'%s\' -j %s -x curl' %(
                prog, url, dldir, flt, jobs)
        p = subprocess.Popen(cmd, shell=True)
        print('create download process %s' %(p.pid))
        if wait_complete:
            p.communicate()
        else:
            waitM3U8Ready(local, verbose = True)
        return local

    print('createJobs fail : {}'.format(url))
    return None


def dl_m3u8(url, dldir, jobs, out):
    if not os.path.exists(dldir):
        os.makedirs(dldir)
        url = createJobs(url, dldir, jobs, True)
    if out:
        os.system('ffmpeg -i {} -c copy {}'.format(url, out))
    return

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', action='append', default=[])
    parser.add_argument('-o', '--output')
    parser.add_argument('-c', '--chdir')
    parser.add_argument('-f', '--filter', action='append', default=[])
    parser.add_argument('-s', '--sort', action='append', default=[])
    parser.add_argument('-x', '--execute')
    parser.add_argument('-j', '--jobs', default=1, type=int)
    parser.add_argument('-n', '--name', default='dl')
    parser.add_argument('-t', '--type', default='mp4')
    parser.add_argument('--sn', default='1')
    parser.add_argument('--cmd')
    parser.add_argument('--m3u8', action='store_true', default=False)
    args, unparsed = parser.parse_known_args()

    if args.m3u8:
        for url in args.input:
            dldir = args.chdir or 'dldir_' + hashlib.md5(url.encode('utf8')).hexdigest()
            dl_m3u8(url, dldir, max(args.jobs, 4), args.output)
        return

    if args.chdir:
        os.chdir(args.chdir)

    results = args.input
    results_next = []
    procs = []
    for i in range(len(args.filter)):
        for x in results:
            results_next.extend(filter(x, args.filter[i]))
        if args.sort and str(i) in args.sort:
            results_next.sort()
        results = results_next
        results_next = []

    for x in results:
        p = dl(x, args)
        if p:
            procs.append(p)
            procs = waitJobs(procs, args)

    for p in procs:
        p.communicate()

    return

if __name__ == '__main__':
    main()
