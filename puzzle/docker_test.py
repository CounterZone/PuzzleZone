import docker
def test_code(solution,test,testcase):
    pass
def atest():
    c=docker.from_env()
    container=c.containers.run('python:3','echo heee',detach=True,tty=True,stream=True)
    a=(container.logs())
    return a
