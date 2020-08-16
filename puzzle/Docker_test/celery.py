from celery import Celery
MAX_TIME=20
MAX_MEM=1000000000
MAX_SWAP=2000000000
app = Celery('test_celery',broker='amqp://rabbit:rabbit@rabbit:5672',backend='rpc://',include=['Docker_test.tasks'])
