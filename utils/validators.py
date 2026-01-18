def validate_tweet_data(tweet_data):
    """
    Валидирует данные твита
    """
    if not tweet_data or not isinstance(tweet_data, str):
        return False
    
    # Проверяем длину твита (например, не более 280 символов как в Twitter)
    if len(tweet_data) > 280:
        return False
    
    # Проверяем, что твит не пустой или не состоит только из пробелов
    if not tweet_data.strip():
        return False
    
    return True