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

## Запуск и использование приложения

### Запуск приложения

Из директории infra/ (через консоль bash), выполните команду для запуска приложения:

```
docker-compose up --build
```

Далее смотрим список контейнеров и узнаём id необходимого контейнера:

```
docker container ls
```

В списке контейнеров находим контейнер, со строчкой включающей в себя слово "backend" в столбце "IMAGE"

Заходим в нужный контейнер с помощью команды:

```
docker exec -it <CONTAINER ID> sh
```

Выполняем миграцию базы данных, сбор статики, загрузку начальных данных:

```
python manage.py migrate

python manage.py collectstatic

python manage.py upload_csv
```


## Технологии

- [Django](https://www.djangoproject.com/)
- [Postgresql](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
