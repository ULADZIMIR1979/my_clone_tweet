import pytest
from utils.validators import validate_tweet_data


def test_validate_tweet_data_valid():
    """Тестирование валидации корректных данных твита"""
    # Корректный твит
    assert validate_tweet_data("Пример твита") == True
    
    # Твит с длиной в пределах лимита
    assert validate_tweet_data("A" * 280) == True


def test_validate_tweet_data_invalid():
    """Тестирование валидации некорректных данных твита"""
    # Пустой твит
    assert validate_tweet_data("") == False
    
    # Твит с только пробелами
    assert validate_tweet_data("   ") == False
    
    # Твит с длиной превышающей лимит
    assert validate_tweet_data("A" * 281) == False
    
    # Некорректный тип данных
    assert validate_tweet_data(None) == False
    assert validate_tweet_data(123) == False
    assert validate_tweet_data([]) == False
    assert validate_tweet_data({}) == False