#===========IMPORTS=============#
from pytube import YouTube as yt
from pytube import *
from dhooks import Webhook
import argparse
from pytube.cli import on_progress
from playlist import playlist_to_watch_urls
#===============================#


# Your DISCORD WEBHOOK URL goes here
DISCORD_API = ''

# Colors
cyan = "\033[96;1m"
red = "\033[91;1m"
yellow = "\033[93;1m"
reset = "\033[0m"

# Func to download videos with reference to its resolution
def download_vid(video):
    hook = Webhook(DISCORD_API)
    if type == 'mp4':
        try:
            video.streams.filter(mime_type="video/mp4",res=res).first().download()
        except AttributeError as e:
           # If the resolution isnt available for that particular video
           print(red + f'[-] Resolution {res} not available!')
           print(reset)
           exit(0)

    elif type == "mp3":
        try:
            video.streams.filter(mime_type='audio/mp3').first().download()
        except AttributeError as e:
            video.streams.filter(mime_type='audio/mp4').first().download()
        except:
            print(red + '[-] Audio format is not supported for this link!!')
            print(reset)
            exit(0)
    else:
        # Incase a wrong TYPE is given
        print(red + '[-] Invalid type!!')
        print(reset)
        exit(0)

    # The following message will be sent to your discord webhook notifying you when the video has finished downloading
    hook.send(f'"{video.title}" downloaded successfully! ')
    print(yellow + f'[*] "{video.title}" downloaded successfully! ')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, help='url to the video or playlist')
    parser.add_argument('-t', '--type', type=str, help='type of file mp3 or mp4')
    parser.add_argument('-r', '--res', type=str, help='resolution of the video')
    args = parser.parse_args()
    isPlaylist = False # Playlist or not
    playlist_videos = []
    isMultiple = False # Multiple URLS or not
    multiple_videos = []
    url = args.url
    try:
        if 'playlist' in url:
            videos = playlist_to_watch_urls(url)
            for video in videos:
                url = "https://www.youtube.com/watch?v="+video
                playlist_videos.append(yt(url, on_progress_callback=on_progress))
            isPlaylist = True
        elif ',' in url:
            urls = url.split(',')
            for url in urls:
                multiple_videos.append(yt(url, on_progress_callback=on_progress))
            isMultiple = True
        else:
            video = yt(url, on_progress_callback=on_progress)
    except:
        print(red + '[-] Invalid URL!')
        print(reset)
        exit(0)

    type = args.type
    if args.res is None:
        pass
    elif args.res[-1:] != 'p':
        res = args.res+'p'
    else:
        res = args.res

    if isPlaylist:
        for video in playlist_videos:
            print(cyan + f'[+] Trying to download "{video.title}"......')
            download_vid(video)
    elif isMultiple:
        for video in multiple_videos:
            print(cyan + f'[+] Trying to download "{video.title}"......')
            download_vid(video)
    else:
        print(cyan + f'[+] Trying to download "{video.title}"......')
        download_vid(video)
    print(reset)
