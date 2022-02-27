
up:
	docker-compose up -d

build: perms
	docker-compose build

perms:
	sudo chown -R $(USER) .