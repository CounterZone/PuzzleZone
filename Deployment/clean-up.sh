docker container stop $(docker ps -a -q --filter="name=puzzlezone_*")
docker container rm $(docker ps -a -q --filter="name=puzzlezone_user_test_*")
docker volume rm $(docker volume ls -q --filter="name=puzzlezone_user_test_*")
