import pytest
from models.models import User, Tweet, Media, Like, Follow, db
from datetime import datetime


def test_user_model(app, client):
    """Тестирование модели User"""
    with app.app_context():
        # Создание пользователя
        user = User(name='Test User', api_key='test_api_key')
        db.session.add(user)
        db.session.commit()
        
        # Проверка атрибутов
        assert user.name == 'Test User'
        assert user.api_key == 'test_api_key'
        assert user.created_at is not None
        assert isinstance(user.created_at, datetime)
        
        # Проверка строкового представления
        assert repr(user) == '<User Test User>'


def test_tweet_model(app, client):
    """Тестирование модели Tweet"""
    with app.app_context():
        # Создание пользователя
        user = User(name='Test User', api_key='test_api_key')
        db.session.add(user)
        db.session.commit()
        
        # Создание твита
        tweet = Tweet(content='Test tweet content', author=user)
        db.session.add(tweet)
        db.session.commit()
        
        # Проверка атрибутов
        assert tweet.content == 'Test tweet content'
        assert tweet.author == user
        assert tweet.author_id == user.id
        assert tweet.created_at is not None
        assert isinstance(tweet.created_at, datetime)
        
        # Проверка строкового представления
        assert repr(tweet) == f'<Tweet {tweet.id}>'


def test_media_model(app, client):
    """Тестирование модели Media"""
    with app.app_context():
        # Создание пользователя
        user = User(name='Test User', api_key='test_api_key')
        db.session.add(user)
        db.session.commit()
        
        # Создание медиа
        media = Media(filename='test_image.jpg', owner=user)
        db.session.add(media)
        db.session.commit()
        
        # Проверка атрибутов
        assert media.filename == 'test_image.jpg'
        assert media.owner == user
        assert media.owner_id == user.id
        assert media.created_at is not None
        assert isinstance(media.created_at, datetime)
        
        # Проверка URL
        assert media.get_url() == '/uploads/test_image.jpg'
        
        # Проверка строкового представления
        assert repr(media) == '<Media test_image.jpg>'


def test_like_model(app, client):
    """Тестирование модели Like"""
    with app.app_context():
        # Создание пользователей
        user1 = User(name='User 1', api_key='user1_api_key')
        user2 = User(name='User 2', api_key='user2_api_key')
        db.session.add_all([user1, user2])
        db.session.commit()
        
        # Создание твита
        tweet = Tweet(content='Test tweet', author=user1)
        db.session.add(tweet)
        db.session.commit()
        
        # Создание лайка
        like = Like(user=user2, tweet=tweet)
        db.session.add(like)
        db.session.commit()
        
        # Проверка атрибутов
        assert like.user == user2
        assert like.tweet == tweet
        assert like.user_id == user2.id
        assert like.tweet_id == tweet.id
        assert like.created_at is not None
        assert isinstance(like.created_at, datetime)
        
        # Проверка строкового представления
        assert repr(like) == f'<Like user_id={like.user_id}, tweet_id={like.tweet_id}>'


def test_follow_model(app, client):
    """Тестирование модели Follow"""
    with app.app_context():
        # Создание пользователей
        follower = User(name='Follower', api_key='follower_api_key')
        following = User(name='Following', api_key='following_api_key')
        db.session.add_all([follower, following])
        db.session.commit()
        
        # Создание подписки
        follow = Follow(follower=follower, following=following)
        db.session.add(follow)
        db.session.commit()
        
        # Проверка атрибутов
        assert follow.follower == follower
        assert follow.following == following
        assert follow.follower_id == follower.id
        assert follow.following_id == following.id
        assert follow.created_at is not None
        assert isinstance(follow.created_at, datetime)
        
        # Проверка строкового представления
        assert repr(follow) == f'<Follow follower_id={follow.follower_id}, following_id={follow.following_id}>'