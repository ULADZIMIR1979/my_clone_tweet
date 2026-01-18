swagger_spec = {
    "openapi": "3.0.0",
    "info": {
        "title": "Twitter Clone API",
        "description": "API для сервиса микроблогов",
        "version": "1.0.0"
    },
    "servers": [
        {
            "url": "/",
            "description": "Local server"
        }
    ],
    "paths": {
        "/api/tweets": {
            "post": {
                "summary": "Создать новый твит",
                "description": "Позволяет пользователю создать новый твит",
                "parameters": [
                    {
                        "name": "api-key",
                        "in": "header",
                        "required": True,
                        "type": "string",
                        "description": "API ключ пользователя"
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "tweet_data": {
                                        "type": "string",
                                        "example": "Пример твита"
                                    },
                                    "tweet_media_ids": {
                                        "type": "array",
                                        "items": {
                                            "type": "integer"
                                        },
                                        "example": [1, 2]
                                    }
                                },
                                "required": ["tweet_data"]
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Твит успешно создан",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "result": {
                                            "type": "boolean"
                                        },
                                        "tweet_id": {
                                            "type": "integer"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "get": {
                "summary": "Получить ленту твитов",
                "description": "Получает ленту твитов от пользователей, на которых подписан текущий пользователь",
                "parameters": [
                    {
                        "name": "api-key",
                        "in": "header",
                        "required": True,
                        "type": "string",
                        "description": "API ключ пользователя"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Список твитов",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "result": {
                                            "type": "boolean"
                                        },
                                        "tweets": {
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/components/schemas/Tweet"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/medias": {
            "post": {
                "summary": "Загрузить медиафайл",
                "description": "Загружает медиафайл для последующего использования в твите",
                "parameters": [
                    {
                        "name": "api-key",
                        "in": "header",
                        "required": True,
                        "type": "string",
                        "description": "API ключ пользователя"
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "file": {
                                        "type": "string",
                                        "format": "binary"
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Файл успешно загружен",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "result": {
                                            "type": "boolean"
                                        },
                                        "media_id": {
                                            "type": "integer"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/tweets/{id}": {
            "delete": {
                "summary": "Удалить твит",
                "description": "Удаляет твит, если он принадлежит пользователю",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "type": "integer",
                        "description": "ID твита"
                    },
                    {
                        "name": "api-key",
                        "in": "header",
                        "required": True,
                        "type": "string",
                        "description": "API ключ пользователя"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Твит успешно удален",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "result": {
                                            "type": "boolean"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/tweets/{id}/likes": {
            "post": {
                "summary": "Поставить лайк твиту",
                "description": "Позволяет пользователю поставить лайк твиту",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "type": "integer",
                        "description": "ID твита"
                    },
                    {
                        "name": "api-key",
                        "in": "header",
                        "required": True,
                        "type": "string",
                        "description": "API ключ пользователя"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Лайк успешно поставлен",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "result": {
                                            "type": "boolean"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "delete": {
                "summary": "Убрать лайк с твита",
                "description": "Позволяет пользователю убрать лайк с твита",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "type": "integer",
                        "description": "ID твита"
                    },
                    {
                        "name": "api-key",
                        "in": "header",
                        "required": True,
                        "type": "string",
                        "description": "API ключ пользователя"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Лайк успешно убран",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "result": {
                                            "type": "boolean"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/users/{id}/follow": {
            "post": {
                "summary": "Подписаться на пользователя",
                "description": "Позволяет пользователю подписаться на другого пользователя",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "type": "integer",
                        "description": "ID пользователя, на которого подписываемся"
                    },
                    {
                        "name": "api-key",
                        "in": "header",
                        "required": True,
                        "type": "string",
                        "description": "API ключ пользователя"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Успешная подписка",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "result": {
                                            "type": "boolean"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "delete": {
                "summary": "Отписаться от пользователя",
                "description": "Позволяет пользователю отписаться от другого пользователя",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "type": "integer",
                        "description": "ID пользователя, от которого отписываемся"
                    },
                    {
                        "name": "api-key",
                        "in": "header",
                        "required": True,
                        "type": "string",
                        "description": "API ключ пользователя"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Успешная отписка",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "result": {
                                            "type": "boolean"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/users/me": {
            "get": {
                "summary": "Получить информацию о текущем пользователе",
                "description": "Позволяет пользователю получить информацию о себе",
                "parameters": [
                    {
                        "name": "api-key",
                        "in": "header",
                        "required": True,
                        "type": "string",
                        "description": "API ключ пользователя"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Информация о пользователе",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "result": {
                                            "type": "boolean"
                                        },
                                        "user": {
                                            "$ref": "#/components/schemas/User"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/users/{id}": {
            "get": {
                "summary": "Получить информацию о пользователе",
                "description": "Позволяет получить информацию о произвольном пользователе",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "type": "integer",
                        "description": "ID пользователя"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Информация о пользователе",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "result": {
                                            "type": "boolean"
                                        },
                                        "user": {
                                            "$ref": "#/components/schemas/User"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "Tweet": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "content": {
                        "type": "string"
                    },
                    "attachments": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "author": {
                        "$ref": "#/components/schemas/UserShort"
                    },
                    "likes": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/UserShort"
                        }
                    }
                }
            },
            "User": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "string"
                    },
                    "followers": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/UserShort"
                        }
                    },
                    "following": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/UserShort"
                        }
                    }
                }
            },
            "UserShort": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "string"
                    }
                }
            }
        }
    }
}