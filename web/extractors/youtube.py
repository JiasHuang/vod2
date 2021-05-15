import re
import json

import xurl
from .utils import *

VALID_URL = r'youtube'

def loadYouTube(url):
    txt = xurl.load(url)
    if not re.search(r'ytInitialData', txt):
        txt = xurl.load(url, cache=False)
    return txt

def parseYoutubeInitialDataJSON(url):
    txt = loadYouTube(url)
    m = re.search(r'ytInitialData\W*= (.*?});', txt)
    if m:
        try:
            return json.loads(m.group(1))
        except:
            print('Exception:\n'+m.group(1))
    return None

def extract_youtube_videos(url):
    data = parseYoutubeInitialDataJSON(url)
    objs = []
    if data:
        for x in findItem(data, ['gridVideoRenderer']):
            try:
                videoId = x['videoId']
                link = 'https://www.youtube.com/watch?v='+videoId
                title = x['title']['runs'][0]['text']
                image = x['thumbnail']['thumbnails'][0]['url']
                desc = None
                for timeStatus in findItem(x, ['thumbnailOverlayTimeStatusRenderer']):
                    if 'simpleText' in timeStatus['text']:
                        desc = timeStatus['text']['simpleText']
                objs.append(entryObj(link, title, image, desc))
            except:
                print('Exception:\n'+str(x))

    return objs

def extract_youtube_channels(url):
    objs = []
    datas = []
    datas.append(parseYoutubeInitialDataJSON(url))
    txt = xurl.load(url)
    m1 = re.search(r'"INNERTUBE_CONTEXT_CLIENT_VERSION":"([^"]*)"', txt)
    m2 = re.search(r'"INNERTUBE_CONTEXT_CLIENT_NAME":(\w+)', txt)
    for m in re.finditer(r'"continuation":"([^"]*)"', txt):
        cont_url = 'https://www.youtube.com/browse_ajax?continuation=' + m.group(1)
        opts = []
        opts.append('-H \'x-youtube-client-version: %s\'' %(m1.group(1)))
        opts.append('-H \'x-youtube-client-name: %s\'' %(m2.group(1)))
        cont_txt = xurl.load(cont_url, opts=opts, ref=url)
        cont_data = json.loads(cont_txt)
        datas.append(cont_data)
    for data in datas:
        for x in findItem(data, ['gridChannelRenderer']):
            try:
                channelId = x['channelId']
                link = 'https://www.youtube.com/channel/'+channelId
                title = x['title']['simpleText']
                image = x['thumbnail']['thumbnails'][0]['url']
                objs.append(entryObj(link, title, image, 'Channel', False))
            except:
                print('Exception:\n'+str(x))

    return objs

def extract_youtube_playlists(url):
    data = parseYoutubeInitialDataJSON(url)
    objs = []
    if data:
        for x in findItem(data, ['playlistRenderer']):
            try:
                playlistId = x['playlistId']
                link = 'https://www.youtube.com/playlist?list='+playlistId
                title = x['title']['simpleText']
                image = x['thumbnails'][0]['thumbnails'][0]['url']
                objs.append(entryObj(link, title, image, 'Playlist', False))
            except:
                print('Exception:\n'+str(x))
        for x in findItem(data, ['gridPlaylistRenderer']):
            try:
                playlistId = x['playlistId']
                link = 'https://www.youtube.com/playlist?list='+playlistId
                title = x['title']['runs'][0]['text']
                image = x['thumbnail']['thumbnails'][0]['url']
                objs.append(entryObj(link, title, image, 'Playlist', False))
            except:
                print('Exception:\n'+str(x))

    return objs

def extract_youtube_playlistVideo(url):
    data = parseYoutubeInitialDataJSON(url)
    objs = []
    channels = False
    if data:
        for x in findItem(data, ['playlistMetadataRenderer']):
            if x['title'] == '@channels':
                channels = True
        for x in findItem(data, ['playlistVideoRenderer']):
            try:
                videoId = x['videoId']
                if channels:
                    browseId = x['shortBylineText']['runs'][0]['navigationEndpoint']['browseEndpoint']['browseId']
                    link = 'https://www.youtube.com/channel/' + browseId
                    title = x['shortBylineText']['runs'][0]['text']
                    image = 'http://img.youtube.com/vi/%s/0.jpg' %(videoId)
                    desc = 'Channel'
                    objs.append(entryObj(link, title, image, desc, False))
                else:
                    link = 'https://www.youtube.com/watch?v='+videoId
                    title = x['title']['runs'][0]['text']
                    image = 'http://img.youtube.com/vi/%s/0.jpg' %(videoId)
                    desc = None
                    for timeStatus in findItem(x, ['thumbnailOverlayTimeStatusRenderer']):
                        if 'simpleText' in timeStatus['text']:
                            desc = timeStatus['text']['simpleText']
                    objs.append(entryObj(link, title, image, desc))
            except:
                print('Exception:\n'+str(x))

    return objs

def extract_youtube_channel(url):
    data = parseYoutubeInitialDataJSON(url)
    objs = []
    if data:
        for x in findItem(data, ['gridVideoRenderer']):
            try:
                image = x['thumbnail']['thumbnails'][0]['url']
                objs.append(entryObj(url+'/videos', 'VIDEOS', image, 'Videos', False))
                break
            except:
                print('Exception:\n'+str(x))

    objs.extend(extract_youtube_videos(url+'/videos?view=2'))
    objs.extend(extract_youtube_playlists(url+'/playlists'))

    return objs

def extract(url):
    if re.search(r'/playlists$', url):
        return extract_youtube_playlists(url)
    elif re.search(r'/channels$', url):
        return extract_youtube_channels(url)
    elif re.search(r'/channel/([^/]*)$', url):
        return extract_youtube_channel(url)
    elif re.search(r'list=', url):
        return extract_youtube_playlistVideo(url)
    else:
        return extract_youtube_videos(url)

def search_youtube(q, sp=None):
    objs = []
    url = 'https://www.youtube.com/results?q=' + q
    if sp:
        url = url+'&sp='+sp
    data = parseYoutubeInitialDataJSON(url)
    if data:
        for x in findItem(data, ['videoRenderer', 'playlistRenderer']):
            if 'videoId' in x:
                videoId = x['videoId']
                link = 'https://www.youtube.com/watch?v=' + videoId
                title = x['title']['runs'][0]['text']
                if 'lengthText' in x:
                    desc = x['lengthText']['simpleText']
                else:
                    desc = 'live'
                image = x['thumbnail']['thumbnails'][0]['url']
                objs.append(entryObj(link, title, image, desc))
            elif 'playlistId' in x:
                playlistId = x['playlistId']
                link = 'https://www.youtube.com/playlist?list='+playlistId
                title = x['title']['simpleText']
                image = x['thumbnails'][0]['thumbnails'][0]['url']
                objs.append(pageObj(link, title, image, 'Playlist'))

    return objs

def search_long(q, sp=None):
    return search_youtube(q, sp or 'EgIYAlAU')

def search_playlist(q, sp=None):
    return search_youtube(q, sp or 'EgIQA1AU')

def search_live(q, sp=None):
    return search_youtube(q, sp or 'EgJAAQ%3D%3D')

