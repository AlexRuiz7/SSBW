
up:
	docker-compose up -d

stop:
	docker-compose stop

build: perms
	docker-compose build

populate:
	docker-compose exec web python populate.py

perms:
	sudo chown -R $(USER) .