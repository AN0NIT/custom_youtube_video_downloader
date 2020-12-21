import requests
from bs4 import BeautifulSoup as bs
import re

def playlist_to_watch_urls(url):
    r = requests.get(url)
    video_urls = []
    soup = bs(r.text,'html.parser')
    scripts = soup.find_all('script')
    for script in scripts:
        for raw_data in script.contents:
            if 'var ytInitialData' in raw_data:
                pattern = r'"videoId":"[(A-Za-z0-9\-\_\+\=\$\#\@\!\%\^\&\*\(\)\:)]{11}'
                result = re.findall(pattern,raw_data)
                for raw_urls in result:
                    raw_urls = raw_urls.split(':"')[1]
                    if raw_urls not in video_urls:
                        video_urls.append(raw_urls)
    return video_urls

if __name__ == "__main__":
    url = input("Enter a playlist url:")
    videos = playlist_to_watch_urls(url)
    for video in videos:
        print("https://www.youtube.com/watch?v="+video)
        
