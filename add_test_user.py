from app import create_app
from models.models import db, User

app = create_app()

with app.app_context():
    # Создаем пользователя с API ключом "test"
    test_user = User(
        name="Test User",
        api_key="test"
    )

    db.session.add(test_user)
    db.session.commit()

    print(f"Создан тестовый пользователь:")
    print(f"ID: {test_user.id}")
    print(f"Name: {test_user.name}")
    print(f"API Key: {test_user.api_key}")