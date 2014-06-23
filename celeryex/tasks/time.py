from __future__ import absolute_import

import time
import random

from celeryex.tasks.celery import app


@app.task()
def sleep():
    """Sleep for a random time and return the sleep time."""
    sleeptime = random.randint(1, 5)
    time.sleep(sleeptime)
    return sleeptime
