Ссылка на постановку тех. задания: https://buildin.ai/share/58227fd1-f5b5-4125-9936-2a6d08d314bd?code=1N7GCX


**Запуск проекта**


*Сборка:*

```
docker-compose up -d --build

```

**Примеры запросов**

@@ ENDPOINT: /reviews

Методы: GET, POST


1. Создать отзыв:

Body: 

```javascript

{
    "text": "что-то странное",
}
```

POST /reviews

JSON-Response:

```javascript
    {
        "id": 1
        "text": "что-то странное",
        "sentiment": "neutral",
        "created_at": "2025-07-15T00:12:46.513611"
    }
```

2. Получить отзывы по `sentiment`

Parameters:

```javascript

{
    "sentiment": ['negative', 'neutral'],
}
```

GET /reviews?sentiment=negative&sentiment=neutral

JSON-Response:

```javascript
{
    "limit": 10,
    "offset": 10,
    "items": [
        {
            "id": 1
            "text": "что-то странное",
            "sentiment": "neutral",
            "created_at": "2025-07-15T00:12:46.513611"
        }, 
        {
            "id": 2
            "text": "что-то плохое",
            "sentiment": "negative",
            "created_at": "2025-07-15T04:41:37.447509"
        }, 
    ]
}
```