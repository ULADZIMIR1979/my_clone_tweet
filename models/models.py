from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    api_key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    tweets = db.relationship('Tweet', backref='author', lazy=True, cascade='all, delete-orphan')
    media = db.relationship('Media', backref='owner', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='user', lazy=True, cascade='all, delete-orphan')
    
    # Followers и Following через промежуточную таблицу Follow
    followers = db.relationship(
        'Follow',
        foreign_keys='Follow.following_id',
        backref='following',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    following = db.relationship(
        'Follow',
        foreign_keys='Follow.follower_id',
        backref='follower',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<User {self.name}>'


class Tweet(db.Model):
    __tablename__ = 'tweets'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    media = db.relationship('Media', secondary='tweet_media', backref='tweets')
    likes = db.relationship('Like', backref='tweet', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Tweet {self.id}>'


class Media(db.Model):
    __tablename__ = 'media'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_url(self):
        return f'/uploads/{self.filename}'

    def __repr__(self):
        return f'<Media {self.filename}>'


class Like(db.Model):
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Уникальное ограничение, чтобы пользователь не мог лайкнуть один и тот же твит дважды
    __table_args__ = (db.UniqueConstraint('user_id', 'tweet_id', name='unique_user_tweet_like'),)

    def __repr__(self):
        return f'<Like user_id={self.user_id}, tweet_id={self.tweet_id}>'


class Follow(db.Model):
    __tablename__ = 'follows'
    
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    following_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Уникальное ограничение, чтобы пользователь не мог подписаться на одного и того же пользователя дважды
    __table_args__ = (db.UniqueConstraint('follower_id', 'following_id', name='unique_follower_following'),)

    def __repr__(self):
        return f'<Follow follower_id={self.follower_id}, following_id={self.following_id}>'


# Промежуточная таблица для связи многие-ко-многим между твитами и медиа
tweet_media = db.Table('tweet_media',
    db.Column('tweet_id', db.Integer, db.ForeignKey('tweets.id'), primary_key=True),
    db.Column('media_id', db.Integer, db.ForeignKey('media.id'), primary_key=True)
)