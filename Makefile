
up:
	docker compose up -d

logs:
	docker compose logs -f

dev: up logs

down:
	docker compose down

restart:
	docker compose restart