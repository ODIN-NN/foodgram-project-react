![Deploy badge](https://github.com/ODIN-NN/foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg)
# FOODGRAM

## Адрес сайта

http://62.84.117.39/

## Документация API

http://62.84.117.39/api/docs/

## Описание проекта

Проект Foodgram представляет собой продуктовый помощник. 
На этом сервисе пользователи смогут публиковать рецепты, 
подписываться на публикации других пользователей, 
добавлять понравившиеся рецепты в список «Избранное», 
а перед походом в магазин скачивать сводный список продуктов, 
необходимых для приготовления одного или нескольких выбранных блюд.

## Установка необходимых компонентов

Установка Docker - https://docs.docker.com/engine/install/

Установка Docker-compose - https://docs.docker.com/compose/install/

## Запуск

### Запуск приложения

В директории infra/ создаём файл .env и наполняем его следующими данными:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

Из директории infra/ (через консоль bash), выполняем команду для запуска приложения:

```
sudo docker-compose up -d
```

Далее смотрим список контейнеров и узнаём id необходимого контейнера:

```
sudo docker container ls
```

В списке контейнеров находим контейнер, со строчкой включающей в себя слово "backend" в столбце "IMAGE"

Запускаем консоль в нужном контейнере с помощью команды:

```
sudo docker exec -it <CONTAINER ID> bash
```

Выполняем миграцию базы данных, сбор статики, загрузку начальных данных:

```
python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic

python manage.py upload_info
```


## Технологии

- [Django](https://www.djangoproject.com/)
- [Postgresql](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
