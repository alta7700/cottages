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
