# init_db.py
from app import create_app
from models.models import db, User, Tweet, Follow, Like
from datetime import datetime

app = create_app()


def init_database():
    with app.app_context():
        # Очищаем и создаем все таблицы заново
        print("Создание таблиц...")
        db.drop_all()
        db.create_all()

        # Проверяем созданные таблицы
        print("Таблицы в базе данных:")
        for table in db.metadata.tables.keys():
            print(f" - {table}")

        # Создаем тестовых пользователей
        print("Создание пользователей...")
        users = [
            User(name='Иван Иванов', api_key='user1_api_key'),
            User(name='Мария Смирнова', api_key='user2_api_key'),
            User(name='Алексей Попов', api_key='user3_api_key'),
            User(name='Елена Кузнецова', api_key='user4_api_key'),
            User(name='Дмитрий Волков', api_key='user5_api_key')
        ]

        for user in users:
            db.session.add(user)

        db.session.commit()
        print("✓ Пользователи созданы")

        # Создаем твиты
        print("Создание твитов...")
        tweets = [
            Tweet(content='Привет, это мой первый твит!', author_id=1),
            Tweet(content='Как проходит ваш день?', author_id=2),
            Tweet(content='Отличная погода сегодня!', author_id=1),
            Tweet(content='Работаю над интересным проектом', author_id=3),
            Tweet(content='Вечером встречаюсь с друзьями', author_id=4)
        ]

        for tweet in tweets:
            db.session.add(tweet)

        db.session.commit()
        print("✓ Твиты созданы")

        # Создаем подписки
        print("Создание подписок...")
        follows = [
            Follow(follower_id=2, following_id=1),  # Мария подписана на Ивана
            Follow(follower_id=3, following_id=1),  # Алексей подписан на Ивана
            Follow(follower_id=4, following_id=2),  # Елена подписана на Марию
            Follow(follower_id=1, following_id=3),  # Иван подписан на Алексея
            Follow(follower_id=5, following_id=1)  # Дмитрий подписан на Ивана
        ]

        for follow in follows:
            db.session.add(follow)

        db.session.commit()
        print("✓ Подписки созданы")

        # Создаем лайки
        print("Создание лайков...")
        likes = [
            Like(user_id=2, tweet_id=1),  # Мария лайкнула твит Ивана
            Like(user_id=3, tweet_id=1),  # Алексей лайкнул твит Ивана
            Like(user_id=4, tweet_id=2),  # Елена лайкнула твит Марии
            Like(user_id=5, tweet_id=1)  # Дмитрий лайкнул твит Ивана
        ]

        for like in likes:
            db.session.add(like)

        db.session.commit()
        print("✓ Лайки созданы")

        print("\n🎉 База данных успешно инициализирована с тестовыми данными!")
        print("\nТестовые API ключи:")
        print("user1_api_key - Иван Иванов")
        print("user2_api_key - Мария Смирнова")
        print("user3_api_key - Алексей Попов")
        print("user4_api_key - Елена Кузнецова")
        print("user5_api_key - Дмитрий Волков")


if __name__ == '__main__':
    init_database()