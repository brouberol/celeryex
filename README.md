This tiny project reproduces the bug/misconfiguration I detailed in the [flower issue tracker](https://github.com/mher/flower/issues/200#issuecomment-43313124).

## Starting the celery worker

```bash
$ celery worker --app=celeryex.tasks --loglevel=INFO -E -n w1

 -------------- celery@w1 v3.1.12 (Cipater)
---- **** -----
--- * ***  * -- Linux-3.11.10-11-desktop-x86_64-with-SuSE-13.1-x86_64
-- * - **** ---
- ** ---------- [config]
- ** ---------- .> app:         tasks:0x212c590
- ** ---------- .> transport:   amqp://guest:**@localhost:5672//
- ** ---------- .> results:     amqp
- *** --- * --- .> concurrency: 4 (prefork)
-- ******* ----
--- ***** ----- [queues]
 -------------- .> celery           exchange=celery(direct) key=celery


[tasks]
  . celeryex.tasks.image.crop
  . celeryex.tasks.time.sleep

[2014-06-23 20:59:13,234: INFO/MainProcess] Connected to amqp://guest:**@127.0.0.1:5672//
[2014-06-23 20:59:13,244: INFO/MainProcess] mingle: searching for neighbors
[2014-06-23 20:59:14,252: INFO/MainProcess] mingle: all alone
[2014-06-23 20:59:14,269: WARNING/MainProcess] celery@w1 ready.
```

## Starting the flower server

```bash
$ celery flower -A celeryex.tasks --debug
[I 140623 21:00:11 command:87] Visit me at http://localhost:5555
[I 140623 21:00:11 command:88] Broker: amqp://guest:**@localhost:5672//
[D 140623 21:00:11 command:90] Registered tasks:
    ['celery.backend_cleanup',
     'celery.chain',
     'celery.chord',
     'celery.chord_unlock',
     'celery.chunks',
     'celery.group',
     'celery.map',
     'celery.starmap']  <--- AHA, so that's where the problem is coming from!
...
```

## Start a task from a python shell

```python
In [1]: from celeryex.tasks.image import crop

In [2]: from celeryex.tasks.time import sleep

In [3]: res = crop.delay()

In [4]: res
Out[4]: <AsyncResult: b8e1b4ea-038b-4a9c-a520-3bf9916cfaa0>

In [5]: res.result
Out[5]: [1440, 900]

In [6]: res2 = sleep.delay()

In [7]: res
Out[7]: <AsyncResult: b8e1b4ea-038b-4a9c-a520-3bf9916cfaa0>

In [8]: res2.result
Out[8]: 1
```

So that works.


## Start a task through the flower REST API

```python
In [14]: requests.post('http://localhost:5555/api/task/async-apply/celeryex.tasks.image.crop', data=json.dumps({}))
Out[14]: <Response [404]>
```

On the server side:

```python
[I 140623 21:03:32 command:87] Visit me at http://localhost:5555
[I 140623 21:03:32 command:88] Broker: amqp://guest:**@localhost:5672//
[W 140623 21:03:32 state:71] Broker info is not available if --broker_api option is not configured. Also make sure RabbitMQ Management Plugin is enabled (rabbitmq-plugins enable rabbitmq_management)
[I 140623 21:03:32 mixins:225] Connected to amqp://guest:**@127.0.0.1:5672//
[I 140623 21:03:47 tasks:96] Invoking a task 'celeryex.tasks.image.crop' with '[]' and '{}'
[W 140623 21:03:47 web:1430] 404 POST /api/task/async-apply/celeryex.tasks.image.crop (::1): Unknown task 'celeryex.tasks.image.crop'
[W 140623 21:03:47 web:1856] 404 POST /api/task/async-apply/celeryex.tasks.image.crop (::1) 1.62ms
```

So that does not work...