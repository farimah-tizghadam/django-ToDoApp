from celery import shared_task
from time import sleep
from todo.models import Task


@shared_task
def completeTask():
    tasks = Task.objects.filter(complete=True)
    for task in tasks:
        task.delete()
