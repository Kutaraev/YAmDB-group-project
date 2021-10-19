![example workflow](https://github.com/Kutaraev/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# api_yamdb
Проект представляет собой бэкенд и REST API для агрегатора отзывов YaMDb.

Ссылка на проект - `http://84.201.138.107`

## Описание
Проект YaMDb собирает отзывы пользователь на произведения. Произведения делятся на категории (например «Книги», «Фильмы», «Музыка»). Список категорий может быть расширен администратором.  

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Братья Карамазовы» и «451 градус по Фаренгейту», а в категории «Музыка» — песня «Hey Jude» группы «Beatles» и восьмая симфония Чайковского.
Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.  

Пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.  

## Перечень технологий, используемых в проекте

1. Python 3.8.4
2. django 2.2.6
3. djangorestframework
4. djangorestframework-simplejwt
5. django-filter 2.4.0
6. Visual Studio Code
7. Docker
8. nginx
9. Gunicorn


## Установка

1. Установите Docker на ваш компьютер.

2. Скачать необходимые образы с Docker Hub
   (Внимание: Docker должен быть установлен на вашем компьютере)
 ```
    docker pull kutaraev/db:v1.0
    docker pull kutaraev/web:v1.0
    docker pull kutaraev/nginx:v1.0
```
3. Запустить Docker-compose
 ```
    docker docker-compose up
```

## Создание суперпользователя
Для создания суперпользователя нужно ввести в терминале комнду
```
docker-compose exec web python manage.py createsuperuser
```
и ввести следующие данные:
- адрес электонной почты
- вашу роль (admin)
- пароль
Теперь можно запустить docker-compose, зайти на адрес `http://127.0.0.1/admin/`, залогиниться и работать с админкой Django.

## Зполнение файла .env
Для работы проекта необходимо создать локально файл .env,
в котором будут храниться секреты и другие данные.
Список переменных:
`DB_ENGINE` - база данных (используется PostgreSQL)
`DB_NAME` имя юазы данных
`POSTGRES_USER` - логин для подключения ук БД
`POSTGRES_PASSWORD` - пароль для подключения к БД
`DB_HOST` - название сервиса (контейнера)
`DB_PORT` - порт для подключения к БД
`SECRET_KEY` - секретный ключ Django
`LOCAL` - логальный IP для запуска проекта
`HOST` - глобальный IP для запуска проета

##
Алгоритм решистрации пользователей

1. Пользователь отправляет запрос с параметром email на `/auth/email/`.
2. YaMDB отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес `email`.
3. Пользователь отправляет запрос с параметрами `email` и `confirmation_code` на `/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на `/users/me/` и заполняет поля в своём профайле.


## Примеры

В данном разделе находятся примеры взаимаодействия с API

### Reviews
1. Получить список всех отзывов:
```
(GET) http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
2. Создать новый отзыв:
```
(POST) http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
3. Получить отзыв по id:
```
(GET) http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```
4. Частично обновить отзыв по id:
```
(PATCH) http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```
5. Удалить отзыв:
```
(DELETE) http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```

### Comments
1. Получить список всех комментариев к отзыву по id:
```
(GET) http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
2. Создать новый комментарий для отзыва:
```
(POST) http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
3. Получить комментарий для отзыва по id:
```
(GET) http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
4. Частично обновить комментарий к отзыву по id:
```
(PATCH) http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
5. Удалить комментарий к отзыву по id:
```
(DELETE) http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

### Categories
1. Получить список всех категорий:
```
(GET) http://127.0.0.1:8000/api/v1/categories/
```
2. Создать категорию:
```
(POST) http://127.0.0.1:8000/api/v1/categories/
```
3. Удалить категорию:
```
(DELETE) http://127.0.0.1:8000/api/v1/categories/{slug}/
```

### Genres
1. Получить список всех жанров:
```
(GET) http://127.0.0.1:8000/api/v1/genres/
```
2. Создать жанр:
```
(POST) http://127.0.0.1:8000/api/v1/genres/
```
3. Удалить жанр:
```
(DELETE) http://127.0.0.1:8000/api/v1/genres/{slug}/
```

### Titles
1. Получить список всех произведений:
```
(GET) http://127.0.0.1:8000/api/v1/titles/
```
2. Создать произведение для отзывов:
```
(POST) http://127.0.0.1:8000/api/v1/titles/
```
3. Информация о произведении:
```
(GET) http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```
4. Обновить информацию об объекте:
```
(PATCH) http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```
5. Удалить произведение:
```
(DELETE) http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```
