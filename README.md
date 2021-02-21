# VOD (Video-On-Demand)

## Description

- Play online streaming videos on Raspberry Pi.
- Control playback on your mobile phone or tablet.
- [Demo](https://www.youtube.com/watch?v=nKMpzaaDPuw)

## Requirements

- youtubedl
- sudo apt install nodejs xterm curl
- xdotool (Optional. For ffplay)
- livestreamer (Optional. For omxplayer)

## USAGE

web/server.py -n HostName -p HostPort -P PlayerName -b BookmarkURL
web/server.py -c config

## Supported Players

- mpv
- ffplay
- omxplayer (For Raspberry Pi)

## Bookmark URL and Example

- Remote URL or local file.
- [Example](https://gist.githubusercontent.com/JiasHuang/30f6cc0f78ee246c1e28bd537764d6c4/raw/bookmark.json)

## Example

web/server.py -n localhost -p 9000 -P mpv -b ~/Downloads/bookmark.json

VOD Server started http://localhost:9000

