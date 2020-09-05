echo "SECRET_KEY='${PUZZLE_KEY}'" > ../PuzzleZone/secret_key.py
sh webpack_build.sh
docker volume create puzzlezone_user_test

docker-compose -f docker-compose-prod.yml build
docker-compose -f docker-compose-prod.yml  up
