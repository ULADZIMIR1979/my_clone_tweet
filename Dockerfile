FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей для сборки и PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей и установка
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary

# Копирование исходного кода
COPY . .

# Создание директории для загрузки файлов
RUN mkdir -p uploads

# Установка переменных окружения
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Открытие порта
EXPOSE 5000

# Команда запуска
#CMD ["flask", "run", "--host=0.0.0.0"] - раскоментировать
