from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from models.models import db, User, Tweet, Media, Like, Follow
from utils.auth import get_user_by_api_key
from utils.validators import validate_tweet_data
import uuid


api_bp = Blueprint('api', __name__)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api_bp.route('/api/tweets', methods=['POST'])
def create_tweet():
    try:
        api_key = request.headers.get('api-key')
        if not api_key:
            return jsonify({"result": False, "error_type": "Unauthorized", "error_message": "API key is required"}), 401

        user = get_user_by_api_key(api_key)
        if not user:
            return jsonify({"result": False, "error_type": "Unauthorized", "error_message": "Invalid API key"}), 401

        data = request.get_json()
        if not data:
            return jsonify({"result": False, "error_type": "BadRequest", "error_message": "No data provided"}), 400

        tweet_data = data.get('tweet_data', '')  # ✅ Делаем опциональным
        tweet_media_ids = data.get('tweet_media_ids', [])

        # ✅ ИСПРАВЛЕННАЯ ВАЛИДАЦИЯ: разрешаем либо текст, либо медиа
        if not tweet_data and not tweet_media_ids:
            return jsonify({
                "result": False,
                "error_type": "ValidationError",
                "error_message": "Either tweet text or media is required"
            }), 400

        # ✅ Проверяем длину текста если он есть
        if tweet_data and len(tweet_data) > 280:
            return jsonify({
                "result": False,
                "error_type": "ValidationError",
                "error_message": "Tweet text too long (max 280 characters)"
            }), 400

        # Создание твита
        tweet = Tweet(content=tweet_data, author_id=user.id)
        db.session.add(tweet)
        db.session.flush()  # Получаем ID твита без фиксации транзакции

        # Привязка медиафайлов к твиту
        for media_id in tweet_media_ids:
            media = Media.query.get(media_id)
            if media and media.owner_id == user.id:
                tweet.media.append(media)

        db.session.commit()

        return jsonify({"result": True, "tweet_id": tweet.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"result": False, "error_type": "InternalServerError", "error_message": str(e)}), 500


@api_bp.route('/api/medias', methods=['POST'])
def upload_media():
    try:
        api_key = request.headers.get('api-key')
        if not api_key:
            return jsonify({"result": False, "error_type": "Unauthorized", "error_message": "API key is required"}), 401

        user = get_user_by_api_key(api_key)
        if not user:
            return jsonify({"result": False, "error_type": "Unauthorized", "error_message": "Invalid API key"}), 401

        if 'file' not in request.files:
            return jsonify({"result": False, "error_type": "BadRequest", "error_message": "No file provided"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"result": False, "error_type": "BadRequest", "error_message": "No file selected"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            extension = filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{extension}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            
            file.save(filepath)

            media = Media(filename=unique_filename, owner_id=user.id)
            db.session.add(media)
            db.session.commit()

            return jsonify({"result": True, "media_id": media.id}), 201
        else:
            return jsonify({"result": False, "error_type": "ValidationError", "error_message": "File type not allowed"}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"result": False, "error_type": "InternalServerError", "error_message": str(e)}), 500


@api_bp.route('/api/tweets/<int:tweet_id>', methods=['DELETE'])
def delete_tweet(tweet_id):
    try:
        api_key = request.headers.get('api-key')
        if not api_key:
            return jsonify({"result": False, "error_type": "Unauthorized", "error_message": "API key is required"}), 401

        user = get_user_by_api_key(api_key)
        if not user:
            return jsonify({"result": False, "error_type": "Unauthorized", "error_message": "Invalid API key"}), 401

        tweet = Tweet.query.get(tweet_id)
        if not tweet:
            return jsonify({"result": False, "error_type": "NotFound", "error_message": "Tweet not found"}), 404

        if tweet.author_id != user.id:
            return jsonify({"result": False, "error_type": "Forbidden", "error_message": "You can only delete your own tweets"}), 403

        db.session.delete(tweet)
        db.session.commit()

        return jsonify({"result": True}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"result": False, "error_type": "InternalServerError", "error_message": str(e)}), 500


@api_bp.route('/api/tweets/<int:tweet_id>/likes', methods=['POST'])
def like_tweet(tweet_id):
    try:
        api_key = request.headers.get('api-key')
        if not api_key:
            return jsonify({"result": False, "error_type": "Unauthorized", "error_message": "API key is required"}), 401

        user = get_user_by_api_key(api_key)
        if not user:
            return jsonify({"result": False, "error_type": "Unauthorized", "error_message": "Invalid API key"}), 401

        tweet = Tweet.query.get(tweet_id)
        if not tweet:
            return jsonify({"result": False, "error_type": "NotFound", "error_message": "Tweet not found"}), 404

        # Проверяем, что лайк еще не существует
        existing_like = Like.query.filter_by(user_id=user.id, tweet_id=tweet_id).first()
        if existing_like:
            return jsonify({"result": False, "error_type": "Conflict", "error_message": "Tweet already liked"}), 409

        like = Like(user_id=user.id, tweet_id=tweet_id)
        db.session.add(like)
        db.session.commit()

        return jsonify({"result": True}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"result": False, "error_type": "InternalServerError", "error_message": str(e)}), 500


@api_bp.route('/api/tweets/<int:tweet_id>/likes', methods=['DELETE'])
def unlike_tweet(tweet_id):
    try:
        api_key = request.headers.get('api-key')
        if not api_key:
            return jsonify({"result": False, "error_type": "Unauthorized", "error_message": "API key is required"}), 401

        user = get_user_by_api_key(api_key)
        if not user:
            return jsonify({"result": False, "error_type": "Unauthorized", "error_message": "Invalid API key"}), 401

        tweet = Tweet.query.get(tweet_id)
        if not tweet:
            return jsonify({"result": False, "error_type": "NotFound", "error_message": "Tweet not found"}), 404

        like = Like.query.filter_by(user_id=user.id, tweet_id=tweet_id).first()
        if not like:
            return jsonify({"result": False, "error_type": "NotFound", "error_message": "Like not found"}), 404

        db.session.delete(like)
        db.session.commit()

        return jsonify({"result": True}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"result": False, "error_type": "InternalServerError", "error_message": str(e)}), 500


@api_bp.route('/api/users/<int:user_id>/follow', methods=['POST'])
def follow_user(user_id):
    try:
        api_key = request.headers.get('api-key')
        if not api_key:
            return jsonify({"result": False, "error_type": "Unauthorized", "error_message": "API key is required"}), 401

        user = get_user_by_api_key(api_key)
        if not user:
            return jsonify({"result": False, "error_type": "Unauthorized", "error_message": "Invalid API key"}), 401

        target_user = User.query.get(user_id)
        if not target_user:
            return jsonify({"result": False, "error_type": "NotFound", "error_message": "User not found"}), 404

        if user.id == target_user.id:
            return jsonify({"result": False, "error_type": "BadRequest", "error_message": "You cannot follow yourself"}), 400

        # Проверяем, что подписка еще не существует
        existing_follow = Follow.query.filter_by(follower_id=user.id, following_id=target_user.id).first()
        if existing_follow:
            return jsonify({"result": False, "error_type": "Conflict", "error_message": "Already following this user"}), 409

        follow = Follow(follower_id=user.id, following_id=target_user.id)
        db.session.add(follow)
        db.session.commit()

        return jsonify({"result": True}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"result": False, "error_type": "InternalServerError", "error_message": str(e)}), 500


@api_bp.route('/api/users/<int:user_id>/follow', methods=['DELETE'])
def unfollow_user(user_id):
    try:
        api_key = request.headers.get('api-key')
        if not api_key:
            return jsonify({"result": False, "error_type": "Unauthorized", "error_message": "API key is required"}), 401

        user = get_user_by_api_key(api_key)
        if not user:
            return jsonify({"result": False, "error_type": "Unauthorized", "error_message": "Invalid API key"}), 401

        target_user = User.query.get(user_id)
        if not target_user:
            return jsonify({"result": False, "error_type": "NotFound", "error_message": "User not found"}), 404

        follow = Follow.query.filter_by(follower_id=user.id, following_id=target_user.id).first()
        if not follow:
            return jsonify({"result": False, "error_type": "NotFound", "error_message": "Not following this user"}), 404

        db.session.delete(follow)
        db.session.commit()

        return jsonify({"result": True}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"result": False, "error_type": "InternalServerError", "error_message": str(e)}), 500


@api_bp.route('/api/tweets', methods=['GET'])
def get_tweets():
    try:
        api_key = request.headers.get('api-key')
        if not api_key:
            return jsonify({"result": False, "error_type": "Unauthorized", "error_message": "API key is required"}), 401

        user = get_user_by_api_key(api_key)
        if not user:
            return jsonify({"result": False, "error_type": "Unauthorized", "error_message": "Invalid API key"}), 401

        # Получаем ID пользователей, на которых подписан текущий пользователь
        following_ids = [follow.following_id for follow in Follow.query.filter_by(follower_id=user.id).all()]
        # Добавляем собственный ID, чтобы показывать и свои твиты тоже
        following_ids.append(user.id)

        # Сортировка по дате создания (новые твиты сначала)
        tweets = db.session.query(Tweet).filter(
            Tweet.author_id.in_(following_ids)
        ).order_by(Tweet.created_at.desc()).all()

        result_tweets = []
        for tweet in tweets:
            tweet_data = {
                "id": tweet.id,
                "content": tweet.content,
                "attachments": [media.get_url() for media in tweet.media],
                "author": {
                    "id": tweet.author.id,
                    "name": tweet.author.name
                },
                "likes": [
                    {
                        "user_id": like.user.id,
                        "name": like.user.name
                    } for like in tweet.likes
                ]
            }
            result_tweets.append(tweet_data)

        return jsonify({"result": True, "tweets": result_tweets}), 200

    except Exception as e:
        return jsonify({"result": False, "error_type": "InternalServerError", "error_message": str(e)}), 500


@api_bp.route('/api/users/me', methods=['GET'])
def get_current_user():
    try:
        api_key = request.headers.get('api-key')
        if not api_key:
            return jsonify({"result": False, "error_type": "Unauthorized", "error_message": "API key is required"}), 401

        user = get_user_by_api_key(api_key)
        if not user:
            return jsonify({"result": False, "error_type": "Unauthorized", "error_message": "Invalid API key"}), 401

        followers = [
            {
                "id": follower.follower.id,
                "name": follower.follower.name
            } for follower in user.followers
        ]

        following = [
            {
                "id": followed.following.id,
                "name": followed.following.name
            } for followed in user.following
        ]

        user_data = {
            "id": user.id,
            "name": user.name,
            "followers": followers,
            "following": following
        }

        return jsonify({"result": True, "user": user_data}), 200

    except Exception as e:
        return jsonify({"result": False, "error_type": "InternalServerError", "error_message": str(e)}), 500


@api_bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"result": False, "error_type": "NotFound", "error_message": "User not found"}), 404

        followers = [
            {
                "id": follower.follower.id,
                "name": follower.follower.name
            } for follower in user.followers
        ]

        following = [
            {
                "id": followed.following.id,
                "name": followed.following.name
            } for followed in user.following
        ]

        user_data = {
            "id": user.id,
            "name": user.name,
            "followers": followers,
            "following": following
        }

        return jsonify({"result": True, "user": user_data}), 200

    except Exception as e:
        return jsonify({"result": False, "error_type": "InternalServerError", "error_message": str(e)}), 500