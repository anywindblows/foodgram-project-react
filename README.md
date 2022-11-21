[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

#### IP: 178.154.203.237

#### users:
```
admin@mail.ru  |   admin2@mail.ru
admin          |   admin
```

# Foodgram

Платформа для публикации рецептов. Пользователи публикуют рецепты, подписываются
на авторов, добавляют рецепты в избранное, а так могут скачать список ингредиентов,
необходимых для готовки с помощью корзины продуктов.

#### Добавьте в Secrets GitHub переменные окружения для работы:

    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<postgres>
    DB_USER=<user>
    DB_PASSWORD=<password>
    DB_HOST=<db>
    DB_PORT=<5432>
    
    DOCKER_USERNAME=<username>
    DOCKER_PASSWORD=<password>
    
    SECRET_KEY=<secret key>
    DEBUG=0

    USER=<username>
    HOST=<ip>
    PASSPHRASE=<passphrase>
    SSH_KEY=<private ssh key (cat ~/.ssh/id_rsa)>

    TELEGRAM_TO=<chat id>
    TELEGRAM_TOKEN=<bot token (@BotFather)>
  
#### На сервере соберите docker-compose:

    sudo docker-compose up -d

#### После сборки выполните команды):
    
    sudo docker-compose exec -it backend bash
    
    python manage.py collectstatic --noinput
    
    python manage.py migrate --noinput

    python manage.py upload_ingredients

    python manage.py createsuperuser