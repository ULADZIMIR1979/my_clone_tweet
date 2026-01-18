-- Создание таблицы users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    api_key VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы tweets
CREATE TABLE IF NOT EXISTS tweets (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    author_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы media
CREATE TABLE IF NOT EXISTS media (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(120) NOT NULL,
    owner_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы likes
CREATE TABLE IF NOT EXISTS likes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    tweet_id INTEGER REFERENCES tweets(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, tweet_id)
);

-- Создание таблицы follows
CREATE TABLE IF NOT EXISTS follows (
    id SERIAL PRIMARY KEY,
    follower_id INTEGER REFERENCES users(id),
    following_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(follower_id, following_id)
);

-- Создание промежуточной таблицы для связи многие-ко-многим между твитами и медиа
CREATE TABLE IF NOT EXISTS tweet_media (
    tweet_id INTEGER REFERENCES tweets(id),
    media_id INTEGER REFERENCES media(id),
    PRIMARY KEY (tweet_id, media_id)
);

-- Создание тестовых пользователей для демонстрации
INSERT INTO users (name, api_key) VALUES 
('Иван Иванов', 'user1_api_key'),
('Мария Смирнова', 'user2_api_key'),
('Алексей Попов', 'user3_api_key'),
('Елена Кузнецова', 'user4_api_key'),
('Дмитрий Волков', 'user5_api_key'),
('Test User', 'test')
ON CONFLICT (api_key) DO NOTHING;

-- Создание тестовых твитов
INSERT INTO tweets (content, author_id) VALUES 
('Привет, это мой первый твит!', 1),
('Как проходит ваш день?', 2),
('Отличная погода сегодня!', 1),
('Работаю над интересным проектом', 3),
('Вечером встречаюсь с друзьями', 4)
ON CONFLICT DO NOTHING;

-- Создание тестовых подписок
INSERT INTO follows (follower_id, following_id) VALUES
(2, 1), -- Мария подписана на Ивана
(3, 1), -- Алексей подписан на Ивана
(4, 2), -- Елена подписана на Марию
(1, 3), -- Иван подписан на Алексея
(5, 1) -- Дмитрий подписан на Ивана
ON CONFLICT (follower_id, following_id) DO NOTHING;

-- Создание тестовых лайков
INSERT INTO likes (user_id, tweet_id) VALUES
(2, 1), -- Мария лайкнула твит Ивана
(3, 1), -- Алексей лайкнул твит Ивана
(4, 2), -- Елена лайкнула твит Марии
(5, 1) -- Дмитрий лайкнул твит Ивана
ON CONFLICT (user_id, tweet_id) DO NOTHING;
