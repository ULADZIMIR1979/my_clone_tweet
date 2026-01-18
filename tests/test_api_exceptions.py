import pytest
import json
from models.models import User, Tweet, Media, Like, Follow, db
from unittest.mock import patch


def test_create_tweet_exception(app, client):
    """Тестирование обработки исключения при создании твита"""
    with app.app_context():
        # Создание пользователя
        user = User(name='Test User', api_key='test_api_key')
        db.session.add(user)
        db.session.commit()
        
        # Мокирование исключения в обработчике
        with patch('routes.api.db.session.commit', side_effect=Exception("Database error")):
            response = client.post(
                '/api/tweets',
                headers={'api-key': 'test_api_key'},
                json={'tweet_data': 'Test tweet content'}
            )
        
        # Проверяем, что возвращается ошибка 500
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['result'] is False


def test_upload_media_exception(app, client):
    """Тестирование обработки исключения при загрузке медиа"""
    import tempfile
    import os
    
    with app.app_context():
        # Создание пользователя
        user = User(name='Test User', api_key='test_api_key')
        db.session.add(user)
        db.session.commit()
        
        # Создание временного файла для теста
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_file.write(b'test image content')
            temp_file_path = temp_file.name
        
        try:
            # Мокирование исключения в обработчике
            with patch('routes.api.db.session.commit', side_effect=Exception("Database error")):
                with open(temp_file_path, 'rb') as img_file:
                    response = client.post(
                        '/api/medias',
                        headers={'api-key': 'test_api_key'},
                        data={'file': (img_file, 'test.jpg')},
                        content_type='multipart/form-data'
                    )
                
                # Проверяем, что возвращается ошибка 500
                assert response.status_code == 500
                data = json.loads(response.data)
                assert data['result'] is False
        finally:
            # Удаление временного файла
            os.unlink(temp_file_path)


def test_delete_tweet_exception(app, client):
    """Тестирование обработки исключения при удалении твита"""
    with app.app_context():
        # Создание пользователя
        user = User(name='Test User', api_key='test_api_key')
        db.session.add(user)
        db.session.commit()
        
        # Создание твита
        tweet = Tweet(content='Test tweet to delete', author=user)
        db.session.add(tweet)
        db.session.commit()
        
        # Мокирование исключения в обработчике
        with patch('routes.api.db.session.commit', side_effect=Exception("Database error")):
            response = client.delete(
                f'/api/tweets/{tweet.id}',
                headers={'api-key': 'test_api_key'}
            )
        
        # Проверяем, что возвращается ошибка 500
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['result'] is False


def test_like_tweet_exception(app, client):
    """Тестирование обработки исключения при лайке твита"""
    with app.app_context():
        # Создание пользователей
        user1 = User(name='User 1', api_key='user1_api_key')
        user2 = User(name='User 2', api_key='user2_api_key')
        db.session.add_all([user1, user2])
        db.session.commit()
        
        # Создание твита
        tweet = Tweet(content='Test tweet to like', author=user1)
        db.session.add(tweet)
        db.session.commit()
        
        # Мокирование исключения в обработчике
        with patch('routes.api.db.session.commit', side_effect=Exception("Database error")):
            response = client.post(
                f'/api/tweets/{tweet.id}/likes',
                headers={'api-key': 'user2_api_key'}
            )
        
        # Проверяем, что возвращается ошибка 500
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['result'] is False


def test_unlike_tweet_exception(app, client):
    """Тестирование обработки исключения при анлайке твита"""
    with app.app_context():
        # Создание пользователей
        user1 = User(name='User 1', api_key='user1_api_key')
        user2 = User(name='User 2', api_key='user2_api_key')
        db.session.add_all([user1, user2])
        db.session.commit()
        
        # Создание твита
        tweet = Tweet(content='Test tweet to unlike', author=user1)
        db.session.add(tweet)
        db.session.commit()
        
        # Создание лайка
        like = Like(user=user2, tweet=tweet)
        db.session.add(like)
        db.session.commit()
        
        # Мокирование исключения в обработчике
        with patch('routes.api.db.session.commit', side_effect=Exception("Database error")):
            response = client.delete(
                f'/api/tweets/{tweet.id}/likes',
                headers={'api-key': 'user2_api_key'}
            )
        
        # Проверяем, что возвращается ошибка 500
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['result'] is False


def test_follow_user_exception(app, client):
    """Тестирование обработки исключения при подписке"""
    with app.app_context():
        # Создание пользователей
        user1 = User(name='User 1', api_key='user1_api_key')
        user2 = User(name='User 2', api_key='user2_api_key')
        db.session.add_all([user1, user2])
        db.session.commit()
        
        # Мокирование исключения в обработчике
        with patch('routes.api.db.session.commit', side_effect=Exception("Database error")):
            response = client.post(
                f'/api/users/{user2.id}/follow',
                headers={'api-key': 'user1_api_key'}
            )
        
        # Проверяем, что возвращается ошибка 500
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['result'] is False


def test_unfollow_user_exception(app, client):
    """Тестирование обработки исключения при отписке"""
    with app.app_context():
        # Создание пользователей
        user1 = User(name='User 1', api_key='user1_api_key')
        user2 = User(name='User 2', api_key='user2_api_key')
        db.session.add_all([user1, user2])
        db.session.commit()
        
        # Создание подписки
        follow = Follow(follower=user1, following=user2)
        db.session.add(follow)
        db.session.commit()
        
        # Мокирование исключения в обработчике
        with patch('routes.api.db.session.commit', side_effect=Exception("Database error")):
            response = client.delete(
                f'/api/users/{user2.id}/follow',
                headers={'api-key': 'user1_api_key'}
            )
        
        # Проверяем, что возвращается ошибка 500
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['result'] is False


def test_get_tweets_exception(app, client):
    """Тестирование обработки исключения при получении твитов"""
    with app.app_context():
        # Создание пользователя
        user = User(name='Test User', api_key='test_api_key')
        db.session.add(user)
        db.session.commit()
        
        # Мокирование исключения в обработчике
        with patch('routes.api.db.session.query', side_effect=Exception("Database error")):
            response = client.get(
                '/api/tweets',
                headers={'api-key': 'test_api_key'}
            )
        
        # Проверяем, что возвращается ошибка 500
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['result'] is False

