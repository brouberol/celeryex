from __future__ import absolute_import

import time
import random

from celeryex.tasks.celery import app


@app.task()
def crop():
    """Perform from fictive work."""
    time.sleep(random.randint(1, 5))
    return random.choice([(640, 480), (1024, 768), (1440, 900)])
