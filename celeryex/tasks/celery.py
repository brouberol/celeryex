from __future__ import absolute_import

from celery import Celery


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

app = Celery(
    'tasks',
    include=[
        'celeryex.tasks.time',
        'celeryex.tasks.image',
    ]
)
app.config_from_object(Config)


if __name__ == '__main__':
    app.start()
