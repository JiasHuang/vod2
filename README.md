# VOD2

## USAGE:
web/server.py -n HostName -p HostPort -P PlayerName -b BookmarkURL

## Player Name
mpv, ffplay, or omxplayer (for raspberry pi).

## bookmark
Remote URL or local file.

ex:
https://gist.githubusercontent.com/JiasHuang/30f6cc0f78ee246c1e28bd537764d6c4/raw/bookmark.json

## Example:
web/server.py -n localhost -p 9000 -P mpv -b ~/Downloads/bookmark.json

VOD Server started http://localhost:9000
