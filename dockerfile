# Use python:3.7 image as base
FROM python:3.7

# Update pip
RUN apt-get update && pip install --upgrade pip

# Install Poetry
RUN pip install poetry

# Expose Port 80
EXPOSE 80

RUN mkdir /todo_app
# Copy code accross
COPY /todo_app /todo_app
COPY /pyproject.toml /todo_app

WORKDIR /todo_app

# To-do app entrypoint
ENTRYPOINT ["poetry run flask run"]