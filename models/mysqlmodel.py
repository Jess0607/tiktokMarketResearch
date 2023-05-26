from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Video(db.Model):
    __tablename__ = 'video'
    video_id = db.Column(db.BigInteger, primary_key=True)
    region = db.Column(db.String(10))
    title = db.Column(db.String(1000))
    origin_cover = db.Column(db.Text)
    play = db.Column(db.Text)
    music_id = db.Column(db.BigInteger)
    play_count = db.Column(db.BigInteger)
    like_count = db.Column(db.BigInteger)
    comment_count = db.Column(db.BigInteger)
    share_count = db.Column(db.BigInteger)
    download_count = db.Column(db.BigInteger)
    author_id = db.Column(db.BigInteger)
    video_google_url = db.Column(db.Text)
    transcript = db.Column(db.Text)
    duration = db.Column(db.Integer)

    def __repr__(self):
        return f"Video('{self.video_id}', '{self.region}', '{self.title}', '{self.origin_cover}', '{self.play}', " \
               f"'{self.music_id}', '{self.play_count}', '{self.like_count}', '{self.comment_count}', " \
               f"'{self.share_count}', '{self.download_count}', '{self.author_id}', '{self.video_google_url}', " \
               f"'{self.transcript}') "


class Music(db.Model):
    __tablename__ = 'music'
    music_id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(255))
    album = db.Column(db.String(255))

    def __repr__(self):
        return f"Music('{self.music_id}', '{self.title}', '{self.album}', '{self.music_google_url}') "


class Author(db.Model):
    __tablename__ = 'author'
    author_id = db.Column(db.BigInteger, primary_key=True)
    unique_id = db.Column(db.String(255))
    avatar_url = db.Column(db.Text)

    def __repr__(self):
        return f"Author('{self.author_id}', '{self.unique_id}', '{self.avatar}') "