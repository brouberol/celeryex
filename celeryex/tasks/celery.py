from __future__ import absolute_import

from celery import Celery
from kombu import Exchange, Queue


class Config(object):
    BROKER_URL = 'amqp://'
    CELERY_RESULT_BACKEND = 'amqp'
    CELERY_TIMEZONE = 'Europe/Paris'
    CELERY_ENABLE_UTC = True
    CELERY_TASK_RESULT_EXPIRES = None
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    ADMINS = (
        ('Balthazar Rouberol', 'brouberol@imap.cc'),
    )
    CELERY_DEFAULT_QUEUE = 'celeryex'
    CELERY_QUEUES = (
        Queue('celeryex', Exchange('celeryex'), routing_key='celeryex'),
    )

app = Celery(
    'tasks',
    include=[
        'celeryex.tasks.time',
        'celeryex.tasks.image',
        'celeryex.tasks.chain'
    ]
)
app.config_from_object(Config)
