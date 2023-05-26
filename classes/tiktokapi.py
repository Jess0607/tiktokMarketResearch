import requests
from dotenv import load_dotenv
import os
import urllib.request
from classes.googlestorage import GoogleStorage
from classes.googletranscribe import GoogleTranscribe
from cleantext import clean

load_dotenv()


class TikTok:
    def __init__(self):
        self.headers = {
            "X-RapidAPI-Key": os.getenv("TIKTOK_API_KEY"),
            "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
        }
        self.video_dictionary = {}
        self.google_storage = GoogleStorage(os.getenv("GOOGLE_CLOUD_PROJECT"))
        self.google_transcribe = GoogleTranscribe()
        self.next_video_id = None
        self.number_video = 0
        self.total_number = 0

    def search(self, keyword, count=10, cursor=0, region="MX", publish_time=0, sort_type=0):
        self.video_dictionary = {}
        self.number_video = 0
        self.total_number = 0
        self.next_video_id = None
        print("Searching TikTok videos...")
        url = "https://tiktok-video-no-watermark2.p.rapidapi.com/feed/search"
        querystring = {"keywords": keyword, "count": count, "cursor": cursor, "region": region,
                       "publish_time": publish_time,
                       "sort_type": sort_type}
        response = requests.get(url, headers=self.headers, params=querystring)
        response_json = response.json()
        response_videos = response_json["data"]["videos"]
        for video in response_videos:
            video_id = video["video_id"]
            region = video["region"]
            title = clean(video["title"], no_emoji=True)
            origin_cover = video["origin_cover"]
            duration = video["duration"]
            play = video["play"]
            music_id = video["music_info"]["id"]
            music_title = video["music_info"]["title"]
            music_album = video["music_info"]["album"]
            play_count = video["play_count"]
            digg_count = video["digg_count"]
            comment_count = video["comment_count"]
            share_count = video["share_count"]
            download_count = video["download_count"]
            author_id = video["author"]["id"]
            author_unique_id = video["author"]["unique_id"]
            author_avatar = video["author"]["avatar"]
            self.video_dictionary[video_id] = {'region': region, 'title': title, 'origin_cover': origin_cover,
                                               'duration': duration, 'play': play, 'music_id': music_id,
                                               'music_title': music_title, 'music_album': music_album,
                                               'play_count': play_count, 'digg_count': digg_count,
                                               'comment_count': comment_count, 'share_count': share_count,
                                               'download_count': download_count, 'author_id': author_id,
                                               'author_unique_id': author_unique_id, 'author_avatar': author_avatar}
        self.total_number = len(self.video_dictionary)

    def upload_video_gc(self, video_url, video_id):
        video_id_mp4 = f"{video_id}.mp4"
        try:
            print(f"Downloading video {video_id_mp4}")
            urllib.request.urlretrieve(video_url, video_id_mp4)
            print(f"Uploading video {video_id_mp4} to Google Cloud...")
            self.google_storage.upload_blob(video_id_mp4, video_id_mp4)
            self.video_dictionary[video_id]['video_url'] = self.google_storage.get_gs_url(video_id_mp4)
            os.remove(video_id_mp4)
        except Exception as e:
            print(e)
            os.remove(video_id_mp4)

    def upload_next_video_gc(self):
        self.number_video += 1
        try:
            self.next_video_id = list(self.video_dictionary.keys())[0]
        except Exception as e:
            return
        self.upload_video_gc(self.video_dictionary[self.next_video_id]['play'], self.next_video_id)

    def get_next_dictionary(self):
        if self.next_video_id and len(self.video_dictionary) > 0:
            return self.video_dictionary[self.next_video_id]

    def transcribe_next_video(self):
        self.transcribe_video(self.next_video_id)
        print(self.video_dictionary)

    def delete_next_video(self):
        if self.next_video_id and len(self.video_dictionary) > 0:
            self.video_dictionary.pop(self.next_video_id)

    def get_total_number_of_videos(self):
        return len(self.video_dictionary)

    def search_and_upload(self, keyword, count=10, cursor=0, region="MX", publish_time=0, sort_type=0):
        self.search(keyword, count, cursor, region, publish_time, sort_type)
        for video_id in self.video_dictionary:
            self.upload_video_gc(self.video_dictionary[video_id]['play'], video_id)

    def transcribe_video(self, video_id):
        print(f"Transcribing video {video_id}...")
        video_url = self.video_dictionary[video_id]['video_url']
        self.video_dictionary[video_id]['transcript'] = self.google_transcribe.get_transcription(video_url)

    def transcribe_all_videos(self):
        for video_id in self.video_dictionary:
            self.transcribe_video(video_id)

    def do_everything(self, keyword, count=10, cursor=0, region="MX", publish_time=0, sort_type=0):
        self.search_and_upload(keyword, count, cursor, region, publish_time, sort_type)
        self.transcribe_all_videos()

    def get_video_dictionary(self):
        return self.video_dictionary


if __name__ == '__main__':
    tiktok = TikTok()
    tiktok.do_everything("vino", 1)
    print(tiktok.get_video_dictionary())
