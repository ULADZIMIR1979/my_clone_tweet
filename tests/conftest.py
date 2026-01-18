import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from models.models import db
import os


@pytest.fixture
def app():
    """Create application for testing"""
    os.environ['TESTING'] = 'True'
    app = Flask(__name__)
    
    # Настройка тестовой базы данных
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Инициализация расширений
    db.init_app(app)
    migrate = Migrate()  # Не инициализируем с приложением для тестов
    migrate.init_app(app, db)
    
    # Создание папки для загрузки файлов
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Регистрация blueprint'ов
    from routes.api import api_bp
    app.register_blueprint(api_bp)
    
    # Регистрация статических маршрутов
    from routes.static import register_static_routes
    register_static_routes(app)
    
    # Настройка Swagger UI
    SWAGGER_URL = '/api/docs'
    API_URL = '/api/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'Twitter Clone API'
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    # Импорт и создание swagger.json
    try:
        from routes.swagger import swagger_spec
        @app.route('/api/swagger.json')
        def swagger_json():
            return swagger_spec
    except ImportError:
        @app.route('/api/swagger.json')
        def swagger_json():
            return {"error": "Swagger spec not available"}
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()