"""conftest.py для всего проекта.

Поднимает контейнеры с БД и redis в фикстурах с scope='session'.
"""
from datetime import datetime, timedelta
from random import randint

import docker
import pytest
import pytest_django
import redis
from django.db import connections
from pytest_asyncio.plugin import _unused_tcp_port

from exrest.apps.crews.enums import OrderTypeChoices
from exrest.apps.shifts.enums import (
    ShiftStateChoicesEnum, ShiftStepChoicesEnum)
from tests import factories


SHIFT_CREWS_COUNT = 5
ORDERS_PER_CREW = 5


def check_db_connection(db_alias='default') -> bool:
    """Проверяет наличие подключения к БД.

    :return: результат проверки
    """
    # временно отключаем блокировку БД
    pytest_django.plugin._blocking_manager.unblock()

    db_conn = connections[db_alias]
    try:
        db_conn.cursor()
    except Exception:
        connected = False
    else:
        connected = True

    # возвращаем блокировку БД обратно
    pytest_django.plugin._blocking_manager.block()

    return connected


def check_redis_connection(host='redis', port=6379):
    """Проверяет возможность подключения к redis."""
    try:
        redis.Redis(host=host, port=port).flushall()
    except Exception:
        connected = False
    else:
        connected = True

    return connected


def get_postgres_container(host, port, user, password, db_name):
    """Запускает docker-контейнер с postgresql."""
    client = docker.from_env()

    if not client.ping():
        raise Exception('Нет возможности использовать docker.')

    con_id = client.containers.run(
        image='postgres:11-alpine',
        name='exrest-postgres-test',
        detach=True,
        environment={
            'POSTGRES_DB': db_name,
            'POSTGRES_PASSWORD': password,
            'POSTGRES_USER': user,
            'POSTGRES_PORT': '5432',
            'PGDATA': '/pgtmpfs'
        },
        remove=True,
        ports={'5432/tcp': port},
        tmpfs={
            '/pgtmpfs': '',
        }
    )
    time_start = datetime.now()
    delta = timedelta(seconds=15)
    while True:
        if check_db_connection():
            return con_id

        if time_start + delta < datetime.now():
            break

    con_id.kill()
    raise Exception('Не удалось подключиться к БД внутри контейнера.')


def get_redis_container(host, port):
    """Запускает docker-контейнер с redis."""
    client = docker.from_env()

    if not client.ping():
        raise Exception('Нет возможности использовать docker.')

    con_id = client.containers.run(
        image='redis:5-alpine',
        name='exrest-redis-test',
        detach=True,
        remove=True,
        ports={'6379/tcp': port},
    )

    time_start = datetime.now()
    delta = timedelta(seconds=15)
    while True:
        if check_redis_connection(host, port):
            return con_id

        if time_start + delta < datetime.now():
            break

    con_id.kill()
    raise Exception('Не удалось подключиться к Redis внутри контейнера.')


@pytest.fixture(scope='session', autouse=True)
def db_init():
    """Создание тестовой базы данных."""
    from django.conf import settings

    postgres_con_id = None
    if not check_db_connection():
        db_port = _unused_tcp_port()
        settings.DATABASES['default']['PORT'] = f'{db_port}'
        settings.DATABASES['default']['HOST'] = 'localhost'

        postgres_con_id = get_postgres_container(
            host='localhost',
            port=db_port,
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            db_name=settings.DATABASES['default']['NAME']
        )

    yield

    postgres_con_id and postgres_con_id.kill()


@pytest.fixture(scope='session', autouse=True)
def redis_init():
    """Инициализирует redis для тестов.

    Проверяет наличие подключения к redis и, если подключение отсутствует,
    поднимает docker-контейнер.
    """
    from django.conf import settings

    redis_con_id = None
    if not check_redis_connection():
        redis_port = _unused_tcp_port()

        settings.REDIS_PORT = f'{redis_port}'
        settings.REDIS_HOST = 'localhost'
        settings.CHANNEL_LAYERS = {
            'default': {
                'BACKEND': 'channels_redis.core.RedisChannelLayer',
                'CONFIG': {
                    'hosts': [('localhost', redis_port)]
                }
            }
        }

        redis_con_id = get_redis_container(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT
        )

    yield

    redis_con_id and redis_con_id.kill()


def get_time_windows(time_begin: datetime, time_end: datetime, tw_count: int):
    """Генерирует tw_count временных окон для равномерно по интервалу смены.

    :param time_begin: Начало интервала
    :param time_end: Конец интервала
    :param tw_count: количество окон
    :return: Лист временных интервалов
    """
    assert time_begin < time_end

    tw_delta = (time_end - time_begin) / tw_count
    start = time_begin
    for index in range(tw_count):
        start = start + index * tw_delta
        end = start + tw_delta
        yield (start, end)


def create_merman_relations(objects, model_class):
    model_class.objects.bulk_create(
        (model_class(
            relation=obj,
            external_id=randint(1000000000, 9999999999)
        ) for obj in objects)
    )


@pytest.fixture()
def fake_accepted_shift():
    """Создает полную фейковую смену. Экипажи заявки и т.д."""
    shift = factories.ShiftFactory.create(
        state=ShiftStateChoicesEnum.ACCEPTED,
        step=ShiftStepChoicesEnum.ACCEPTED,
    )
    stock = factories.StockFactory.create()
    cars = factories.CarFactory.create_batch(SHIFT_CREWS_COUNT)
    drivers = factories.EmployeeFactory.create_batch(SHIFT_CREWS_COUNT)
    forwarders = factories.EmployeeFactory.create_batch(SHIFT_CREWS_COUNT)
    crews = []

    start_tw, *time_windows, finish_tw = list(get_time_windows(
        time_begin=shift.begin,
        time_end=shift.end,
        tw_count=ORDERS_PER_CREW + 2
    ))

    for car, driver, forwarder in zip(cars, drivers, forwarders):
        crews.append(factories.CrewFactory.create(
            car=car,
            driver=driver,
            forwarder=forwarder,
            shift=shift
        ))

    orders = []

    for index, crew in enumerate(crews):
        factories.PointFactory.create(
            order=None,
            stock=stock,
            address=stock.address,
            crew=crew,
            type=OrderTypeChoices.STOCK,
            time_from=start_tw[0],
            time_to=start_tw[1],
            index=0
        )

        for order_index, (t_begin, t_end) in enumerate(time_windows, start=1):
            order = factories.OrderFactory.create(
                shift=shift,
                time_from=t_begin,
                time_to=t_end
            )
            orders.append(order)

            factories.PointFactory.create(
                order=order,
                address=order.address,
                crew=crew,
                time_from=order.time_from,
                time_to=order.time_to,
                index=order_index
            )

        factories.PointFactory.create(
            order=None,
            stock=stock,
            address=stock.address,
            crew=crew,
            type=OrderTypeChoices.STOCK,
            time_from=finish_tw[0],
            time_to=finish_tw[1],
            index=ORDERS_PER_CREW + 1
        )

    return shift
