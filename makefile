serve:
	python manage.py runserver
migrate:
	python manage.py makemigrations && python manage.py migrate 
test:
	python test.py
scrape:
	python scrape.py
	 