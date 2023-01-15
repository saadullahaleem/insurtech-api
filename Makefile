setup:
	docker-compose build
	docker-compose up -d
	docker exec -it test_api python manage.py makemigrations
	docker exec -it test_api python manage.py migrate
	docker exec -it test_api python manage.py createsuperuser --noinput --email admin@admin.com --username admin

up:
	docker-compose up

django_shell:
	docker exec -it test_api python manage.py shell_plus

shell:
	docker exec -it test_api /bin/sh
