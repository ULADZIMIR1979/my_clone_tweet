from models.models import User


def get_user_by_api_key(api_key):
    """
    Получает пользователя по API ключу
    """
    return User.query.filter_by(api_key=api_key).first()