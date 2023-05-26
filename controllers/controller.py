from flask import request
from classes.tiktokapi import TikTok
from models.mysqlmodel import Video, Music, Author, db
from views.view import View


class Controller:
    def __init__(self):
        self.tiktok = TikTok()
        self.view = View()

    def insert_into_database(self):
        dictionary = self.tiktok.get_next_dictionary()
        video_id = self.tiktok.next_video_id
        video_insert = Video(video_id=video_id,
                             region=dictionary['region'],
                             title=dictionary['title'],
                             origin_cover=dictionary['origin_cover'],
                             duration=dictionary['duration'],
                             play=dictionary['play'],
                             music_id=dictionary['music_id'],
                             play_count=dictionary['play_count'],
                             like_count=dictionary['digg_count'],
                             comment_count=dictionary['comment_count'],
                             share_count=dictionary['share_count'],
                             download_count=dictionary['download_count'],
                             author_id=dictionary['author_id'],
                             video_google_url=dictionary['video_url'],
                             transcript=dictionary['transcript'])

        music_insert = Music(music_id=dictionary['music_id'],
                             title=dictionary['music_title'],
                             album=dictionary['music_album'])

        author_insert = Author(author_id=dictionary['author_id'],
                               unique_id=dictionary['author_unique_id'],
                               avatar_url=dictionary['author_avatar'])

        try:
            db.session.add(video_insert)
            db.session.add(music_insert)
            db.session.add(author_insert)
            db.session.commit()
        except Exception as e:
            print(e)

    def upload_next_video(self):
        self.tiktok.upload_next_video_gc()
        return 'Video Uploaded'

    def uploading_video(self):
        if request.method == 'POST':
            if self.tiktok.video_dictionary == {}:
                user_prompt = request.form['user_prompt']
                user_num_videos = int(request.form['user_num_videos'])
                self.tiktok.search(user_prompt, user_num_videos)
        return self.view.render_uploading(self.tiktok.number_video, self.tiktok.total_number)

    def transcribe_next_video(self):
        self.tiktok.transcribe_next_video()
        self.insert_into_database()
        self.tiktok.delete_next_video()
        return 'Video Transcribed'

    def transcribing_video(self):
        return self.view.render_transcribing(self.tiktok.number_video, self.tiktok.total_number,
                                             self.tiktok.get_total_number_of_videos())

    def finished(self):
        return self.view.render_finished()

    def render_home(self):
        return self.view.render_home()
