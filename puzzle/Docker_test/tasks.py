from .celery import app
import sys,os,json,io
import docker
sys.path.insert(0,'/')
from . import SetDjangoORM
from puzzle.models import Question

from celery.exceptions import SoftTimeLimitExceeded




HOST_NAME=os.getenv('HOSTNAME')

USER_PATH='/puzzle/Docker_test/user/'

CONTAINER_NAME='user_test'
VOLUME_NAME='puzzlezone_user_test'

# settings
MEM_LIMIT='1g'

FULL_TIME_LIMIT=120 # second
SAMPLE_TIME_LIMIT=30

SAMPLE_SIZE=10
FAIL_MESSAGE='test case {test_case_id}:failed!\nfailed case: {test_args}\nexpected result:{test_result}\nyour result:{user_result}\n'
PASS_MESSAGE='test case {test_case_id}:passed!\n'

SETTING_ITEMS=['SAMPLE_SIZE','FAIL_MESSAGE','PASS_MESSAGE']


client=docker.from_env()
try:
    container=client.containers.get(CONTAINER_NAME)
except docker.errors.NotFound:
    container=client.containers.create('python:3.8.3-buster',
    tty=True,detach=True,
    mem_limit=MEM_LIMIT,
    volumes={VOLUME_NAME:{'bind':'/user','mode':'ro'}},
    read_only=True,
    working_dir='/user',
    name=CONTAINER_NAME,
    )
container.start()




@app.task(bind=True,name='sample_test',soft_time_limit=SAMPLE_TIME_LIMIT)
def sample_test(self,solution,question_id):
    '''
    run the test on the sample test test_cases
    if a case is not passed, break.
    '''
    try:
        q=docker_prepare(solution,question_id)
        test_cases=io.StringIO(json.loads(q.test_cases))
        for i in range(SAMPLE_SIZE):
            test_case=test_cases.readline().rstrip('\n')
            if test_case[0]=='#': # ignore lines start with #
                i=i-1
                continue
            test_args,test_result=test_case.split(':')
            result=docker_test(test_args,test_result)
            if result['status']=='PASS':
                self.update_state(state="TEST_PASS", meta={'stdout':result['stdout'],'message':PASS_MESSAGE.format(test_case_id=i,test_args=test_args,test_result=test_result,user_result=result['result'])})
            else:
                self.update_state(state='TEST_FAIL',meta={'stdout':result['stdout'],'message':FAIL_MESSAGE.format(test_case_id=i,test_args=test_args,test_result=test_result,user_result=result['result'])})
                return False
        return True
    except SoftTimeLimitExceeded:
        pass



@app.task(bind=True,name='full_test',soft_time_limit=FULL_TIME_LIMIT)
def full_test(self,solution,question_id):
    '''
    run the test on all test test_cases.
    even a case is not passed, the test still continues.
    '''
    try:
        q=docker_prepare(solution,question_id)
        test_cases=io.StringIO(json.loads(q.test_cases))
        test_count=0
        pass_count=0
        for test_case in test_cases.readlines():
            test_case=test_case.rstrip('\n')
            if test_case[0]=='#': # ignore lines start with #
                continue
            test_args,test_result=test_case.split(':')
            test_count+=1
            result=docker_test(test_args,test_result)
            if result['status']=='PASS':
                self.update_state(state="TEST_PASS", meta={'stdout':result['stdout'],'message':PASS_MESSAGE.format(test_case_id=test_count,test_args=test_args,test_result=test_result,user_result=result['result'])})
                pass_count+=1
            else:
                self.update_state(state='TEST_FAIL',meta={'stdout':result['stdout'],'message':FAIL_MESSAGE.format(test_case_id=test_count,test_args=test_args,test_result=test_result,user_result=result['result'])})
        return 'Succeed.',test_count,pass_count
    except SoftTimeLimitExceeded:
        return 'ExceedTimeLimit',test_count,pass_count


@app.task(bind=True,name='question_test',soft_time_limit=FULL_TIME_LIMIT)
def question_test(self,question_id):
    '''
    test the question
    solution is the solution field of question object
    '''
    try:
        q=docker_prepare(solution,question_id)
        solution=json.loads(q.solution_code)
        test_cases=io.StringIO(json.loads(q.test_cases))
        test_count=0
        pass_count=0
        for test_case in test_cases.readlines():
            test_case=test_case.rstrip('\n')
            if test_case[0]=='#': # ignore lines start with #
                continue
            test_args,test_result=test_case.split(':')
            test_count+=1
            result=docker_test(test_args,test_result)
            if result['status']=='PASS':
                self.update_state(state="TEST_PASS", meta={'stdout':result['stdout'],'message':PASS_MESSAGE.format(test_case_id=test_count,test_args=test_args,test_result=test_result,user_result=result['result'])})
                pass_count+=1
            else:
                self.update_state(state='TEST_FAIL',meta={'stdout':result['stdout'],'message':FAIL_MESSAGE.format(test_case_id=test_count,test_args=test_args,test_result=test_result,user_result=result['result'])})
        return 'Succeed.',test_count,pass_count
    except SoftTimeLimitExceeded:
        return 'ExceedTimeLimit',test_count,pass_count




def docker_prepare(solution,question_id):
    '''
    prepare the files for the test in docker,and get the settings
    /user
        solution.py - contains the solution code in the message
        test.py - contains the test code defined in the question
    return the question object
    if solution is not specified, then use question's solution code
    '''
    global SAMPLE_SIZE,PASS_MESSAGE,FAIL_MESSAGE
    q=Question.objects.get(id=question_id)
    if solution==None:
        solution=q.solution_code
    sol_file=open(os.path.join(USER_PATH,'solution.py'),'w')
    sol_file.write(json.loads(solution))
    test_file=open(os.path.join(USER_PATH,'test.py'),'w')
    test_file.write(json.loads(q.test_code))
    sol_file.close()
    test_file.close()
    setting=json.loads(container.exec_run('python /user/run_test.py --get_settings').output)
    for item in SETTING_ITEMS:
        if item in setting:
            exec(item+'='+json.dumps(setting[item]))
    return q

def docker_test(test_args,test_result):
    '''
    run a single test_case in docker container
    the comparison is done outside the container
    parse the logs, then return the result
    '''
    c=container.exec_run('python /user/run_test.py --test_args "{test_args}"'.format(test_args=test_args))
    if c.exit_code==0:
        result=c.output.decode('utf8').split('\n')
        stdout='\n'.join(result[:-2]).strip('\n')
        result=result[-1]
        if result==test_result:
            status='PASS'
        else:
            status='FAIL'
        return {'status':status,'result':result,'stdout':stdout}
    else:
        return {'status':'ERROR','result':c.output,'stdout':''}
