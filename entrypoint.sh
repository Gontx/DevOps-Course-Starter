SHELL=/bin/bash


# Start application

poetry run gunicorn -w 4 --bind 0.0.0.0:"${PORT:-8000}" "todo_app.app:create_app()"
