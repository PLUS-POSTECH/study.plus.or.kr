# study.plus.or.kr
This repository contains the source code of the [https://study.plus.or.kr](https://study.plus.or.kr) website.

## Wiki
For more information, please visit https://github.com/PLUS-POSTECH/study.plus.or.kr/wiki

## Dev Installation
```
$ git clone https://github.com/PLUS-POSTECH/study.plus.or.kr.git
$ mv study.plus.or.kr dev.study.plus.or.kr
$ cd dev.study.plus.or.kr
$ cp docker-compose.override.dev.yml docker-compose.override.yml
$ `your_favorite_editor` docker-compose.override.yml  # set your django secret key
$ docker-compose up -d
```

## Production Installation
```
$ git clone https://github.com/PLUS-POSTECH/study.plus.or.kr.git
$ mkdir static
$ cd study.plus.or.kr
$ cp docker-compose.override.production.yml docker-compose.override.yml
$ `your_favorite_editor` docker-compose.override.yml  # set your secret key and hosts
$ docker-compose up -d
```

The server is running at `localhost:8000`. Use nginx or other proxy to your server.

## Production Installation (reverse proxy)
```
$ git clone https://github.com/PLUS-POSTECH/study.plus.or.kr.git
$ mkdir static
$ cd study.plus.or.kr
$ cp docker-compose.override.production.reverse-proxy.yml docker-compose.override.yml
$ `your_favorite_editor` docker-compose.override.yml  # set your secret key and hosts
$ docker-compose up -d
```

`docker-compose.override.production.reverse-proxy.yml` is an example configuration for reverse proxy.

## Update
```
$ docker-compose up -d --no-deps --build web
```

## Creating Super User
```
$ docker-compose exec web python manage.py createsuperuser
```
