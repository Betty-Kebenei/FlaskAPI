release: python manage.py DB init && python manage.py DB migrate
web: waitress-serve --threads=8  --port=$PORT run:APP