FROM python:3.7-alpine3.9

# USR_LOCAL_BIN - путь до пользовательских скриптов
# PROJECT_ROOT - путь до каталога внутри контейнера, в который будет
# копироваться приложение
ENV USR_LOCAL_BIN=/usr/local/bin  \
    PROJECT_ROOT=/application

# путь до исходников
ENV PYTHONPATH=$PYTHONPATH:$PROJECT_ROOT

# пакеты, которые необходимы для работы в runtime
ENV RUNTIME_PACKAGES \
    libev \
    pcre \
    postgresql-dev \
    docker \
    jpeg-dev \
    zlib-dev \
    libressl-dev \
    libffi-dev \
    openssh

# Пакеты, которые необходимы для установки зависимостей.
# Не останутся в итоговом образе.
ENV BUILD_PACKAGES \
    libev-dev \
    git \
    build-base \
    pcre-dev \
    gcc \
    linux-headers

# Установка пакетов в систему
RUN apk update && \
    apk upgrade && \
    pip install --upgrade pip && \
    pip install wheel pipenv
RUN apk --no-cache add --virtual build-deps $BUILD_PACKAGES && \
    apk --no-cache add $RUNTIME_PACKAGES

# Создание директорий
RUN mkdir $PROJECT_ROOT/ && \
    mkdir $PROJECT_ROOT/run && \
    mkdir $PROJECT_ROOT/wsgi && \
    mkdir $PROJECT_ROOT/logs && \
    mkdir $PROJECT_ROOT/tests && \
    mkdir $PROJECT_ROOT/static && \
    mkdir $PROJECT_ROOT/media

COPY ./Pipfile $PROJECT_ROOT/
COPY ./Pipfile.lock $PROJECT_ROOT/

WORKDIR $PROJECT_ROOT

# Установка зависимостей через pipenv
RUN set -ex && pipenv install --deploy --system --dev
# Удаление ненужных пакетов
RUN apk del build-deps

COPY ./compose/app/start_celery $USR_LOCAL_BIN/
COPY ./compose/app/start_celery_beat $USR_LOCAL_BIN/
COPY ./compose/app/start_daphne $USR_LOCAL_BIN/
COPY ./compose/app/start_broker $USR_LOCAL_BIN/
COPY ./compose/app/start_uwsgi $USR_LOCAL_BIN/
COPY ./compose/app/start_sshd $USR_LOCAL_BIN/
COPY ./compose/app/entrypoint.sh $USR_LOCAL_BIN/

COPY ./compose/app/uwsgi.ini $PROJECT_ROOT/wsgi

RUN sed -i 's/\r//' $USR_LOCAL_BIN/start_daphne \
    && chmod +x $USR_LOCAL_BIN/start_daphne \
    && sed -i 's/\r//' $USR_LOCAL_BIN/start_celery \
    && chmod +x $USR_LOCAL_BIN/start_celery \
    && sed -i 's/\r//' $USR_LOCAL_BIN/start_celery_beat \
    && chmod +x $USR_LOCAL_BIN/start_celery_beat \
    && sed -i 's/\r//' $USR_LOCAL_BIN/start_broker \
    && chmod +x $USR_LOCAL_BIN/start_broker \
    && sed -i 's/\r//' $USR_LOCAL_BIN/start_uwsgi \
    && chmod +x $USR_LOCAL_BIN/start_uwsgi \
    && sed -i 's/\r//' $USR_LOCAL_BIN/entrypoint.sh \
    && chmod +x $USR_LOCAL_BIN/entrypoint.sh \
    && sed -i 's/\r//' $USR_LOCAL_BIN/start_sshd \
    && chmod +x $USR_LOCAL_BIN/start_sshd

# копирование непосредственно проекта и тестов
ADD ./src $PROJECT_ROOT

# ssh для дебага
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/AllowTcpForwarding no/AllowTcpForwarding yes/' /etc/ssh/sshd_config
RUN echo "root:xAGXA5j38TPL8Jwm" | chpasswd

EXPOSE 8000

ENTRYPOINT ["entrypoint.sh"]

CMD start_uwsgi