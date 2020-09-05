import json
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from celery import Celery
from .models import Submission,Question
'''
websocket api
legal message received:
{'command':'sample_test', 'solution':solution_code, 'question_id':q_id}
{'command':'full_test', 'solution':solution_code, 'question_id':q_id}

legal message to send:
{'command':'display','message':msg}
{'command':'pass_sample_test'}
{'command':'fail_sample_test'}
{'command':'submission_redirect','message':submission_id}

'''




celery_app = Celery('test_celery',broker='amqp://rabbit:rabbit@rabbit:5672',backend='rpc://',include=[])

class PuzzleConsumer(WebsocketConsumer):
    '''
    deal with the websocket created by the user.
    the solution code is sent through the websocket. the server would send the test results, then close the connection
    the 'submission' command also send through the socket.
    one user can only have one connection.
    '''
    def connect(self):
        self.accept()
        if self.scope["user"].is_anonymous:
            self.send_msg('display','Please sign in!')
            self.close()
            return
        self.scope['session']['task_in_running']=False
        task_in_running=False if 'task_in_running' not in self.scope['session'] else self.scope['session']['task_in_running']
        if task_in_running:
            self.send_msg('display','You have task in running!')
            self.close(code=1) # task_in_running
            return
        self.user = self.scope["user"]
        self.scope['session']['task_in_running']=True
        self.scope['session'].save()

    def disconnect(self, close_code):
        if close_code!=1:
            self.scope['session']['task_in_running']=False
            self.scope['session'].save()
    def send_msg(self,cmd,msg,target='client'):
        '''
        if target = 'client', send the msg to the client
        else, if target = a list, add the msg to the list
        '''
        if target=='client':
            self.send(json.dumps({'command':cmd,'message':msg}))
        else:
            target.append(msg)
    def receive(self, text_data):
        message=json.loads(text_data)
        if message['command'] in ['sample_test','full_test','question_test']:
            self.send_msg('display','pending...')
            sol=message['solution']
            q_id = message['question_id']
            if message['command']=='sample_test':
                a_res=celery_app.send_task(message['command'],[sol,q_id])
                m=a_res.get(on_message=self.process_celery_message,propagate=False)
                if m:
                    self.send_msg('pass_sample_test',None)
                else:
                    self.send_msg('fail_sample_test',None)

            elif message['command']=='full_test':
                log=[]
                a_res=celery_app.send_task(message['command'],[sol,q_id])
                m=a_res.get(on_message=lambda x:self.process_celery_message(x,log),propagate=False)
                status,pass_num,tot_num=m
                score=pass_num/tot_num if status=='Succeed.' else 0
                result=status+' {p:d}/{t:d} passed.'.format(p=pass_num,t=tot_num)
                sub=Submission(
                creator=self.user,
                question=Question.objects.get(id=q_id),
                code=sol,
                log=''.join(log),
                result=result,
                score=score
                )
                sub.save()
                if status=='ExceedTimeLimit':
                    self.send_msg('display','Exceeded time limit!')
                elif status=='Error':
                    self.send_msg('display','Error exists!')
                self.send_msg('submission_redirect',str(sub.id))
            self.close()

    def process_celery_message(self,message,log=None):
        '''
        process the message received from the cellery tasks
        message:
        {
        'status': 'TEST_PASS' or 'TEST_FAIL' or 'SUCCESS'
        'result': {'message':msg}
        }

        '''
        if message['status'] in ['TEST_PASS','TEST_FAIL']:
            self.send_msg('display',message['result']['stdout'])
            self.send_msg('display',message['result']['message'])
            if log!=None:
                self.send_msg('display',message['result']['stdout'])
                self.send_msg('display',message['result']['message'],log)
