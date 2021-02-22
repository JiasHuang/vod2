# VOD (Video-On-Demand)

## Description

- Play online streaming videos on Raspberry Pi.
- Browse and control videos via your mobile phone or tablet.
- [Demo](https://www.youtube.com/watch?v=nKMpzaaDPuw)

## Requirements

- youtubedl
- sudo apt install nodejs curl
- xdotool (Optional. For ffplay)
- livestreamer (Optional. For omxplayer)

## USAGE

web/server.py -n HostName -p HostPort -P PlayerName -b BookmarkURL
web/server.py -c config

## Supported Players

- mpv
- ffplay
- omxplayer
- vlc

## Bookmark URL and Example

- Remote URL or local file.
- [Example](https://gist.githubusercontent.com/JiasHuang/30f6cc0f78ee246c1e28bd537764d6c4/raw/bookmark.json)

## Example

web/server.py -n localhost -p 9000 -P mpv -b ~/Downloads/bookmark.json

```
VOD Server started http://localhost:9000
```

## Control Guide

Button   | Description
------   | -----------
⏹        | stop
▶        | play/pause
num + ▶  | seek num%
num + ⏭  | seek +num secs
num + ⏮  | seek -num secs

### Installation on Raspberry Pi

- Install youtube-dl
- Install livestreamer
	```
	sudo apt install livestreamer
	```
- Edit /home/pi/.config/lxsession/LXDE-pi/autostart
	```
	@lxpanel --profile LXDE-pi
	@pcmanfm --desktop --profile LXDE-pi
	@lxterminal -geometry=80x24 -e /home/pi/work/vod2/web/server.py -c /home/pi/.myconfig
	```
- Edit /home/pi/.myconfig
	```
	[VODServer]
	hostport = 8080
	player = omxplayer
	```

