echo "SECRET_KEY='dsfasdf'" > ../PuzzleZone/secret_key.py

docker volume create puzzlezone_user_test

docker-compose -f docker-compose-prod.yml build

docker build ../puzzle/Docker_test -t test_image

docker-compose -f docker-compose-prod.yml   up
