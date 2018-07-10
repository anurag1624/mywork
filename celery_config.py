from celery import Celery

app = Celery('celery_config', broker='amqp://localhost:5672', backend='rpc://localhost:5672'
             , include=['celery_worker_1'],CELERY_ROUTES={"app.my_task": {"queue": "app.my_task"}} )
