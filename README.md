[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

# YAmDb group project
Проект представляет собой бэкенд и REST API для агрегатора отзывов YaMDb.

## Описание
Проект YaMDb собирает отзывы пользователей на различные произведения. Произведения делятся на категории (например «Книги», «Фильмы», «Музыка»). Список категорий может быть расширен администратором.  

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Братья Карамазовы» и «451 градус по Фаренгейту», а в категории «Музыка» — песня «Hey Jude» группы «Beatles» и восьмая симфония Чайковского.
Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.  

Пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти. Из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.  

## Технологии
- [Python 3](https://www.python.org/downloads/)
- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [Docker](https://www.docker.com/)
- [NGINX](https://nginx.org/)
- [Gunicorn](https://gunicorn.org/)
- [Git](https://github.com/)
- [Visual Studio Code](https://code.visualstudio.com/Download)

## Установка

1. Установите [Docker](https://www.docker.com/) на ваш компьютер  
2. Скачать необходимые образы с [Docker Hub](https://hub.docker.com/)
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
`DB_ENGINE` - база данных (используется PostgreSQL).  
`DB_NAME` - имя базы данных.  
`POSTGRES_USER` - логин для подключения к БД.  
`POSTGRES_PASSWORD` - пароль для подключения к БД.  
`DB_HOST` - название сервиса (контейнера).  
`DB_PORT` - порт для подключения к БД.  
`SECRET_KEY` - секретный ключ Django.  
`LOCAL` - локальный IP для запуска проекта.  
`HOST` - глобальный IP для запуска проета.  

##
Алгоритм регистрации пользователей

1. Пользователь отправляет запрос с параметром email на `/auth/email/`.
2. YaMDB отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес `email`.
3. Пользователь отправляет запрос с параметрами `email` и `confirmation_code` на `/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на `/users/me/` и заполняет поля в своём профайле.

## Примеры взаимодействия с API
Данный проект имеет широкий фунционал и поддерживает все CRUD-методы (Create, Read, Update, Delete) взаимодействия с базой данных. Ниже в качастве примера приведены запросы для взаимодействия с рецензиями.
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
Полный список всех запросов можно посмотреть по адресу http://127.0.0.1:8000/redoc/ при локально запущенном проекте.

## Планы по развитию проекта
1. Создание web-интерфейса, при помощи которого пользователи будут взаимодействавать с бекендом и БД.
2. Возможность поиска контента по тегам.
3. Разработка персональных подборок на основе рейтинга, который выставлял пользователь.
4. Более продвинутая система категорий с детальной информацией.

## Контакты
Артем Кутараев – [@artem_kutaraev](https://t.me/artem_kutaraev) – artem.kutaraev@gmail.com  
Ссылка на проект – [https://github.com/Kutaraev/YAmDB-group-project.git](https://github.com/Kutaraev/YAmDB-group-project.git)
