build:
	# Build image locally.
	docker-compose up -d --build

clean:
	docker-compose down --remove-orphans

run:
	docker-compose up -d

logs:
	docker logs -f bmd-micro_api_1

test:
	# Run unit tests.
	docker-compose exec api pytest "project/tests" -p no:warnings --cov="project" --cov-report html
	open htmlcov/index.html
	docker-compose exec api flake8 project
	docker-compose exec api black project --check
	docker-compose exec api /bin/sh -c "isort project/*/*.py --check-only"
