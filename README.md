[![.github/workflows/main.yml](https://github.com/Sterlyadkin/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/Sterlyadkin/foodgram-project-react/actions/workflows/main.yml)

доменное имя: http://vsfoodgram.hopto.org
логин администратора: admin
пароль администратора: admin
e-mail администратора: admin@yandex.ru

## Описание проекта

Сайт "Foodgram" - это онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список избранных или список покупок и скачивать список продуктов в виде PDF файла, необходимых для приготовления одного или нескольких выбранных блюд.

## Запуск проекта из образов с Docker hub 

Установить на сервере docker и docker-compose.
Скопировать на сервер файлы docker-compose.yaml и default.conf:

```
scp docker-compose.yml <логин_на_сервере>@<IP_сервера>:/home/<логин_на_сервере>/docker-compose.yml
scp nginx.conf <логин_на_сервере>@<IP_сервера>:/home/<логин_на_сервере>/nginx.conf

```

## Добавить в Secrets на Github следующие данные:

```
DOCKER_PASSWORD= # Пароль от аккаунта на DockerHub
DOCKER_USERNAME= # Username в аккаунте на DockerHub
HOST= # IP удалённого сервера
USER= # Логин на удалённом сервере
SSH_KEY= # SSH-key компьютера, с которого будет происходить подключение к удалённому серверу
PASSPHRASE= #Если для ssh используется фраза-пароль
TELEGRAM_TO= #ID пользователя в Telegram
TELEGRAM_TOKEN= #ID бота в Telegram

```

Выполняем запуск:

```bash
sudo docker compose up -d
```

Произойдет скачивание образов, создание и включение контейнеров, создание томов и сети.

## Запуск проекта из исходников GitHub

Клонируем себе репозиторий: 

```bash 
git clone git@github.com:Sterlyadkin/foodgram-project-react.git
```

Выполняем запуск:

```bash
sudo docker compose up
```

## После запуска: Миграции, сбор статистики

После запуска необходимо выполнить сбор статистики и миграции бэкенда. Статистика фронтенда собирается во время запуска контейнера, после чего он останавливается. 

```bash
sudo docker compose exec backend python manage.py migrate

sudo docker compose exec backend python manage.py collectstatic --no-input 

sudo docker compose exec backend python manage.py load_data
```

И далее проект доступен на: 

```
http://localhost:8000/
```
## Необходимые переменные окружения

```bash
POSTGRES_USER= <Желаемое_имя_пользователя_базы_данных>
POSTGRES_PASSWORD= <Желаемый_пароль_пользователя_базы_данных>
POSTGRES_DB= <Желаемое_имя_базы_данных>
DB_HOST=
DB_PORT= 
SECRET_KEY = 
DEBUG = 
```

## Остановка оркестра контейнеров

В окне, где был запуск **Ctrl+С** или в другом окне:

```bash
sudo docker compose down
```

## Автор

Стерлядкин Владимир https://github.com/Sterlyadkin/
