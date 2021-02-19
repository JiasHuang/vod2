# vod2

## USAGE:
web/server.py -n hostName -p hostPort -P playerName -b bookmark

## Player Name
mpv, ffplay, or omxplayer (for raspberry pi).

## bookmark
Remote URL or local file.

## Example:
web/server.py -n localhost -p 9000 -P ffplay -b 'https://gist.githubusercontent.com/JiasHuang/30f6cc0f78ee246c1e28bd537764d6c4/raw/bookmark.json'

VOD Server started http://localhost:9000
