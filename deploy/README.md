## Инициализация на сервере
### Структура
```
├───app
│   └───.env
├───network
│   ├───dhparam.pem
│   └───nginx
│       └───nginx.conf.template
├───.env
├───docker-compose.yaml
```
- /app/.env - файл с переменными для django приложения (app/example.env)
- /.env - файл с общими переменными (deploy/example.env)
- /network/dhparam.pem - генерируется на сервере командой `openssl dhparam -out dhparam.pem 4096`

## Первый запуск
1) Создать папку project `mkdir project`, в ней описанную выше структуру, и переходим в неё `cd project`
2) Создать пустую бд `sqlite3 app/db.sqlite3 "VACUUM;"`
3) Применить миграции к БД<br/>`docker compose run --rm app .venv/bin/python app/manage.py migate`
5) Собрать статику<br/>`docker compose run --rm app .venv/bin/python app/manage.py collectstatic --no-input`
6) Закомментировать блок с ssl в /network/nginx/nginx.conf.template
7) Запустить nginx <br/>`docker compose up -d nginx`
8) Сгенерировать ssl сертификаты (вместо ${DOMAIN} подставить значение переменной из .env) <br/>`docker compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d ${DOMAIN},www.${DOMAIN}`
9) Разкомментировать блок с ssl в /network/nginx/nginx.conf.template
10) Пересоздать контейнеры <br/>`docker compose rm -s && docker compose up -d nginx app`
11) Вызвать `crontab -e` и добавить ежедневное задание на обновление сертификатов <br/>`0 0 * * * cd /home/$USER/project && docker compose run --rm certbot renew`
12) Создать суперпользователей для админки `docker compose exec -it app .venv/bin/python app/manage.py createsuperuser`

### Собрать образ и запушить на hub.
```shell
docker build -t makarovhouse/site:$VERSION -t makarovhouse/site:latest .
docker push makarovhouse/site:$VERSION
docker push makarovhouse/site:latest
```

### На сервере при обновлении версии.
Находясь в папке с проектом.
```shell
docker compose run --rm app .venv/bin/python app/manage.py migrate
docker compose run --rm app .venv/bin/python app/manage.py collectstatic --no-input
```
