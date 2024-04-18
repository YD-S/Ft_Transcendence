
DB_VOL = ~/data/database
CACHE_VOL = ~/data/redis

run:
	mkdir -p $(DB_VOL)
	mkdir -p $(CACHE_VOL)
	docker-compose up --build

stop:
	docker-compose down

re: stop run

.PHONY: re stop