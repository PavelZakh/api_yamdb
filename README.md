## Проект api_yamdb

С помощью этого API вы сможете оставлять отзывы с оценками на различные произведения. А также комментировать эти отзывы. Для этого необходимо зарегестрироватьсяв нашем api.

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/PavelZakh/api_yamdb.git
```
```
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
```
source env/bin/activate
```
```
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```
### Примеры запросов к API:

Регистрация:
```
POST http://127.0.0.1:8000/api/v1/auth/signup/
```
Запрос:
```
{
    "email": "email@mail.ru",
    "username": "new_user"
}
```
Ответ:
```
{
    "email": "email@mail.ru",
    "username": "new_user"
}
```
После этого на почту придет код подтверждения, который необходимо использовать для аунтификации на нашем сервисе
```
POST http://127.0.0.1:8000/api/v1/auth/token/
```
Запрос:
```
{
    "username": "new_user",
    "confirmation_code": "сode_from_email"
}
```
Ответ:
```
{
  "token": "string"
}
```
После успешной авторизации вы получить Bearer Token, Который необходимо добалять в header любого запроса.
Теперь можно оставлять рейтинг и давать ревью для произведений

Получить список доступных жанров:
```
GET http://127.0.0.1:8000/api/v1/genres/
```
Ответ:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```
Получить список доступных произведений:
```
GET http://127.0.0.1:8000/api/v1/titles/
```
Ответ:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {}
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
       }
    ]
  }
]
```
Оставить отзыв:
```
POST http://127.0.0.1:8000/api/v1/follow/
```
```
{
  "text": "string",
  "score": 5
}
```
Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

Получить полную документацию со всеми запросами можно запустив сервер и перейти по ссылке: 
```
http://127.0.0.1:8000/redoc/
```
