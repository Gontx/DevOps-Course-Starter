SHELL=/bin/bash
PORT=8000
# Start application

poetry run gunicorn -w 4 --bind "0.0.0.0:${PORT}" todo_app.app:create_app
