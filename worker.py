from celery import Celery

import requests

from db_models import Task

celery_app = Celery('task', broker='amqp://guest@localhost//')
api_key = '6e0b94be8236cf4c7c3dd0935f91952e3056c7f6948cede7e796a2cf'

@celery_app.task
def get_data(ip, task_id):
    url = f"https://api.ipdata.co/{ip}?api-key={api_key}"
    result = requests.get(url)
    
    updated_task = Task.get_by_id(task_id)
    data = result.json()

    updated_task.city = data['city']
    updated_task.country = data['country_name']

    updated_task.save()


    