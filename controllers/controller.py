from flask import request
from classes.tiktokapi import TikTok
from models.mysqlmodel import Video, Music, Author, db, Topic
from views.view import View
from classes.machinelearning import ModelBart


class Controller:
    def __init__(self):
        self.tiktok = TikTok()
        self.view = View()
        self.user_prompt = None
        self.user_num_videos = None
        self.model_bart = ModelBart()

    def is_video_id_in_database(self):
        video_id = self.tiktok.next_video_id
        if Video.query.filter_by(video_id=video_id).first() is not None:
            return True
        return False

    def insert_into_database(self):
        if not self.is_video_id_in_database():
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
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
            finally:
                db.session.close()

            try:
                db.session.add(music_insert)
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
            finally:
                db.session.close()

            try:
                db.session.add(author_insert)
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
            finally:
                db.session.close()

    def upload_next_video(self):
        self.tiktok.increase_number_video()
        while self.is_video_id_in_database() and len(self.tiktok.video_dictionary) > 0:
            self.tiktok.delete_next_video()
            self.tiktok.increase_number_video()
        if not self.is_video_id_in_database():
            self.tiktok.upload_next_video_gc()
        return 'Video Uploaded'

    def uploading_video(self):
        return self.view.render_uploading(self.tiktok.number_video, self.tiktok.total_number)

    def searching_video(self):
        if self.user_prompt is not None:
            cursor = self.tiktok.current_cursor
            cursor += self.tiktok.total_number
            self.tiktok.reset()
            self.tiktok.current_cursor = cursor
        else:
            # self.tiktok.video_dictionary == {} and self.user_prompt is None
            self.user_prompt = request.form['user_prompt']
            self.user_num_videos = int(request.form['user_num_videos'])
        print(self.tiktok.current_cursor)
        return self.view.render_searching(self.tiktok.number_video, self.tiktok.total_number)

    def searching_video_logic(self):
        self.tiktok.search(self.user_prompt, self.user_num_videos, cursor=self.tiktok.current_cursor)
        return 'Search Finished'

    def transcribe_next_video(self):
        try:
            if not self.is_video_id_in_database():
                self.tiktok.transcribe_next_video()
                self.insert_into_database()
        except Exception as e:
            print(e)
        finally:
            return 'Video Transcribed'

    def transcribing_video(self):
        print(len(self.tiktok.video_dictionary))
        return self.view.render_transcribing(self.tiktok.number_video, self.tiktok.total_number,
                                             self.tiktok.get_total_number_of_videos())

    def insert_into_database_topics(self, topics, source):
        video_id = self.tiktok.next_video_id
        for topic in topics:
            topic_insert = Topic(video_id=video_id,
                                 topic_name=topic,
                                 source=source)
            try:
                db.session.add(topic_insert)
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
            finally:
                db.session.close()

    def get_topics_next_video(self):
        print(f"transcript: {self.tiktok.get_next_video_transcript()}")
        try:
            transcript = self.tiktok.get_next_video_transcript()
            title = self.tiktok.get_next_video_title()
            if transcript is not None and transcript != '':
                topics = self.model_bart.topic_model(transcript)
                print(f"topics: {topics}")
                self.insert_into_database_topics(topics, source='transcript')
            if title is not None and title != '':
                topics = self.model_bart.topic_model(title)
                print(f"topics: {topics}")
                self.insert_into_database_topics(topics, source='title')
        except Exception as e:
            print(e)
        finally:
            self.tiktok.delete_next_video()
            return 'Topics Extracted'

    def get_topics(self):
        return self.view.render_topics(self.tiktok.number_video, self.tiktok.total_number, self.tiktok.get_total_number_of_videos())

    def finished(self):
        return self.view.render_finished(self.tiktok.total_number)

    def render_home(self):
        self.user_num_videos = None
        self.user_prompt = None
        self.tiktok.reset()

        return self.view.render_home()
