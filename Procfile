web: daphne chat_project.asgi:application --port $PORT ==bind 0.0.0.0 -v2
chatworker: python manage.py runworker --settings=chat_project.settings -v2