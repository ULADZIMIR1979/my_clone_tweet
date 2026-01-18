import pytest
from models.models import User, db
from utils.auth import get_user_by_api_key


def test_get_user_by_api_key(app, client):
    """Тестирование функции get_user_by_api_key"""
    with app.app_context():
        # Создание пользователя
        user = User(name='Test User', api_key='test_api_key')
        db.session.add(user)
        db.session.commit()
        
        # Поиск пользователя по API ключу
        found_user = get_user_by_api_key('test_api_key')
        
        # Проверка, что пользователь найден
        assert found_user is not None
        assert found_user.name == 'Test User'
        assert found_user.api_key == 'test_api_key'
        
        # Проверка поиска несуществующего пользователя
        not_found_user = get_user_by_api_key('non_existent_key')
        assert not_found_user is None