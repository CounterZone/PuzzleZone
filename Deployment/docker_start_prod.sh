


echo "SECRET_KEY='${PUZZLE_KEY}'" > ../PuzzleZone/secret_key.py

docker-compose -f docker-compose-prod.yml build

docker build ../puzzle/Docker_test -t test_image

docker-compose -f docker-compose-prod.yml up --scale worker=5
