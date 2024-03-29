import os

codedir   = os.path.dirname(os.path.realpath(__file__))
workdir   = '/var/tmp/'
dldir     = '/var/tmp/'
fifo      = workdir + 'vod.fifo'
log       = workdir + 'vod_%s.log' %(os.getuid())

# playlist settings
playlist     = workdir + 'vod_%s_playlist' %(os.getuid())
playbackMode = workdir + 'vod_%s_playbackMode' %(os.getuid())
playing      = workdir + 'vod_%s_playing' %(os.getuid())

# command locations
vod = os.path.join(codedir, 'vod.py')

# server settings
hostname = ''
hostport = 8080
bookmark = 'https://gist.githubusercontent.com/JiasHuang/30f6cc0f78ee246c1e28bd537764d6c4/raw/bookmark.json'

