setup:
	docker-compose build
	docker-compose up -d
	docker exec -it test_api python manage.py makemigrations
	docker exec -it test_api python manage.py migrate
	docker exec -it test_api python manage.py createsuperuser --noinput --email admin@admin.com --username admin

rebuild:
	docker-compose down
	docker-compose build

up:
	docker-compose up

django_shell:
	docker exec -it test_api python manage.py shell_plus

test:
	docker-compose up -d
	docker exec -it test_api coverage run --source='.' manage.py test --keepdb
	docker exec -it test_api coverage report

shell:
	docker exec -it test_api /bin/sh
