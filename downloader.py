#===========IMPORTS=============#
from pytube import YouTube as yt
from pytube import *
from dhooks import Webhook
import argparse
from colorama import init, Fore
from pytube.cli import on_progress
from playlist import playlist_to_watch_urls
#===============================#

# init for colorama
init(autoreset=True)
# Your DISCORD WEBHOOK URL goes here
DISCORD_API = ''

# Func to download videos with reference to its resolution
def download_vid(video):
    hook = Webhook(DISCORD_API)
    if type == 'mp4':
        try:
            if res == '1080':
                video.streams.get_by_itag(137).download()
            elif res == '720':
                video.streams.get_by_itag(22).download()
            elif res == '480':
                video.streams.get_by_itag(135).download()
            elif res == '360':
                video.streams.get_by_itag(18).download()
            elif res == '240':
                video.streams.get_by_itag(133).download()
            elif res == '144':
                video.streams.get_by_itag(160).download()
        except:
           # If the resolution isnt available for that particular video
           print('Invalid Resolution!')
           exit(0)

    elif type == "mp3":
        try:
            video.streams.get_by_itag(140).download()
        except:
           print(Fore.RED + '[-] Invalid ITAG!')
           exit(0)
    else:
        # Incase a wrong TYPE is given
        print(Fore.RED + '[-] Invalid type!!')
        exit(0)

    # The following message will be sent to your discord webhook notifying you when the video has finished downloading
    hook.send(f'"{video.title}" downloaded successfully! ')
    print(Fore.LIGHTBLACK_EX + f'[*] "{video.title}" downloaded successfully! ')

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
        print(Fore.RED + '[-] Invalid URL!')
        exit(0)

    type = args.type
    res = args.res
    if isPlaylist:
        for video in playlist_videos:
            print(Fore.CYAN + f'[+] Trying to download "{video.title}"......')
            download_vid(video)
    elif isMultiple:
        for video in multiple_videos:
            print(Fore.CYAN + f'[+] Trying to download "{video.title}"......')
            download_vid(video)
    else:
        print(Fore.CYAN + f'[+] Trying to download "{video.title}"......')
        download_vid(video)
