from flask import Blueprint, send_from_directory
import os

# Создаем blueprint для статических файлов
static_bp = Blueprint('static', __name__)

@static_bp.route('/')
def serve_index():
    # ✅ Правильный путь к dist от корня проекта
    dist_path = os.path.join(os.path.dirname(__file__), '..', 'dist')
    abs_dist_path = os.path.abspath(dist_path)
    print(f"📁 Serving index from: {abs_dist_path}")  # Для отладки
    return send_from_directory(abs_dist_path, 'index.html')

@static_bp.route('/<path:path>')
def serve_static(path):
    # ✅ Правильный путь к dist от корня проекта
    dist_path = os.path.join(os.path.dirname(__file__), '..', 'dist')
    abs_dist_path = os.path.abspath(dist_path)
    return send_from_directory(abs_dist_path, path)

def register_static_routes(app):
    app.register_blueprint(static_bp)