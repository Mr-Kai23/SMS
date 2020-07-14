from celery import Celery


def make_celery():
    celery = Celery(
        'tasks',
        backend='amqp',
        broker='amqp://guest:guest@127.0.0.1:15672//'
    )

    return celery


celery = make_celery()


@celery.task
def add(a, b):

    return a+b
