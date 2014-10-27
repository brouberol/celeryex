from __future__ import absolute_import

from celery import Task

from celeryex.tasks.celery import app

retried = False


class LoggerTask(Task):
    def __call__(self, *args, **kwargs):
        print "args=%r, kwargs=%r" % (args, kwargs)
        return super(LoggerTask, self).__call__(*args, **kwargs)


class ChainMember(LoggerTask):

    abstract = True

    def __call__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], list):
            args = args[0]
        return super(ChainMember, self).__call__(*args, **kwargs)


@app.task(base=ChainMember, bind=True)
def task1(self, x, y):
    global retried
    if x == 1 and not retried:
        retried = True
        self.retry(countdown=10)
    return x * 2, y * 2, x * y


@app.task(base=ChainMember)
def task2(x, y, z):
    return x * 3, y * 3, z * 2
