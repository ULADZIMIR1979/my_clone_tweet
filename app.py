from flask import Flask, send_from_directory
import os
from flask_swagger_ui import get_swaggerui_blueprint

# Импортируем db из models
from models.models import db
from flask_migrate import Migrate

migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Конфигурация приложения
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                           'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)

    # Создание папки для загрузки файлов
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # ✅ ПЕРЕМЕСТИТЕ ЭТОТ МАРШРУТ СЮДА - ПЕРЕД статическими маршрутами
    @app.route('/uploads/<filename>')
    def serve_uploaded_file(filename):
        print(f"📁 Serving uploaded file: {filename}")
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # Регистрация статических маршрутов
    from routes.static import register_static_routes
    register_static_routes(app)

    # Регистрация blueprint'ов
    from routes.api import api_bp
    app.register_blueprint(api_bp)

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
        print("=== ЗАРЕГИСТРИРОВАННЫЕ МАРШРУТЫ ===")
        for rule in app.url_map.iter_rules():
            print(f"{rule.endpoint}: {rule.rule} {rule.methods}")
        print("===================================")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)