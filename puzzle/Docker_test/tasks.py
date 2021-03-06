from .celery import app
import sys,os,json,io
import docker
sys.path.insert(0,'/')
from . import SetDjangoORM
from puzzle.models import Question
import tarfile

from celery.exceptions import SoftTimeLimitExceeded




HOST_NAME=os.getenv('HOSTNAME')

USER_PATH='/puzzle/Docker_test/user/'

CONTAINER_NAME='puzzlezone_user_test_'+HOST_NAME
HELPER_CONTAINER_NAME='puzzlezone_user_test_helper'+HOST_NAME
VOLUME_NAME=CONTAINER_NAME+'_vol'

# settings
MEM_LIMIT='1g'

FULL_TIME_LIMIT=120 # second
SAMPLE_TIME_LIMIT=30
SETTINGS={
'SAMPLE_SIZE':10,
'FAIL_MESSAGE':'test case {test_case_id}:failed!\nfailed case: {test_args}\nexpected result:{test_result}\nyour result:{user_result}\n',
'PASS_MESSAGE':'test case {test_case_id}:passed!\n',
}


client=docker.from_env()
client.volumes.create(name=VOLUME_NAME, driver='local')

try:
    container=client.containers.get(CONTAINER_NAME)
except docker.errors.NotFound:
    image=client.images.get('test_image')
    container=client.containers.create(image,
    tty=True,detach=True,
    mem_limit=MEM_LIMIT,
    volumes={VOLUME_NAME:{'bind':'/user','mode':'ro'}},
    read_only=True,
    working_dir='/user',
    name=CONTAINER_NAME,
    network_disabled=True
    )
try:
    helper=client.containers.get(HELPER_CONTAINER_NAME)
except docker.errors.NotFound:
    image=client.images.get('test_image')
    helper=client.containers.create(image,detach=True,
    volumes={VOLUME_NAME:{'bind':'/user','mode':'rw'}},
    working_dir='/user',
    name=HELPER_CONTAINER_NAME,
    network_disabled=True
    )
container.start()

class CompileError(Exception):
    def __init__(self, message):
        self.message = message



@app.task(bind=True,name='sample_test',soft_time_limit=SAMPLE_TIME_LIMIT)
def sample_test(self,solution,question_id):
    '''
    run the test on the sample test test_cases
    if a case is not passed, break.
    '''
    try:
        q=docker_prepare(solution,question_id)
        SAMPLE_SIZE=SETTINGS['SAMPLE_SIZE']
        PASS_MESSAGE=SETTINGS['PASS_MESSAGE']
        FAIL_MESSAGE=SETTINGS['FAIL_MESSAGE']
        test_cases=io.StringIO(json.loads(q.test_cases))
        for i in range(SAMPLE_SIZE):
            test_case=test_cases.readline().rstrip('\n')
            if not test_case:
                break
            if  test_case[0]=='#': # ignore lines start with #
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
        docker_clean_up()
        self.update_state(state='TEST_FAIL',meta={'stdout':'','message':"ExceedTimeLimit"})
        return False
    except CompileError as e:
        self.update_state(state='TEST_FAIL',meta={'stdout':"",'message':e.message})
        return False


@app.task(bind=True,name='full_test',soft_time_limit=FULL_TIME_LIMIT)
def full_test(self,solution,question_id):
    '''
    run the test on all test test_cases.
    even a case is not passed, the test still continues.
    '''
    test_count=0
    pass_count=0
    try:
        q=docker_prepare(solution,question_id)
        PASS_MESSAGE=SETTINGS['PASS_MESSAGE']
        FAIL_MESSAGE=SETTINGS['FAIL_MESSAGE']
        test_cases=io.StringIO(json.loads(q.test_cases))
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
        docker_clean_up()
        return 'ExceedTimeLimit',test_count,pass_count
    except CompileError as e:
        self.update_state(state='TEST_FAIL',meta={'stdout':"",'message':e.message})
        return 'Error',0,0
    except:
        return 'Error',test_count,pass_count


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
    container.start()
    q=Question.objects.get(id=question_id)
    if solution==None:
        solution=q.solution_code
    sol_file=open(os.path.join(USER_PATH,'solution.py'),'w')
    sol_file.write(json.loads(solution))
    test_file=open(os.path.join(USER_PATH,'test.py'),'w')
    test_file.write(json.loads(q.test_code))
    sol_file.close()
    test_file.close()
    tar = tarfile.open(os.path.join(USER_PATH,'temp.tar'),'w')
    tar.add(os.path.join(USER_PATH,'solution.py'),arcname='solution.py')
    tar.add(os.path.join(USER_PATH,'test.py'),arcname='test.py')
    tar.add(os.path.join(USER_PATH,'run_test.py'),arcname='run_test.py')
    tar.close()
    data = open(os.path.join(USER_PATH,'temp.tar'), 'rb').read()
    helper.put_archive('/user', data)
    prepare_output=container.exec_run('python /user/run_test.py --get_settings')
    if prepare_output.exit_code==0:
        setting=json.loads(prepare_output.output)
    else:
        raise CompileError(prepare_output.output.decode('utf8'))
    for item in SETTINGS:
        if item in setting:
            SETTINGS[item]=setting[item]
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
        return {'status':'ERROR','result':c.output.decode('utf8'),'stdout':''}

def docker_clean_up():
    '''
    when time limit exceed, clean the container
    '''
    container.kill()
