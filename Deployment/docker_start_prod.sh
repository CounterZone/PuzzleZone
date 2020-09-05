echo "SECRET_KEY='${PUZZLE_KEY}'" > ../PuzzleZone/secret_key.py
sh webpack_build.sh
docker volume create puzzlezone_user_test

docker-compose -f docker-compose-prod.yml build

docker build ../puzzle/Docker_test -t test_image

docker-compose -f docker-compose-prod.yml -d  up
