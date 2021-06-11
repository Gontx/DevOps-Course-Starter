# Use python:buster image as base
FROM python:buster as base

# Update pip
RUN apt-get update && pip install --upgrade pip
RUN apt-get install -y curl

# Install Poetry and add to path
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH = "${PATH}:/root/.poetry/bin"

# Expose Port 8000
EXPOSE 8000

FROM base as production
# Copy code accross
COPY . /usr/DevOps-Course-Starter

WORKDIR /usr/DevOps-Course-Starter

# Install poetry dependencies and create .env
RUN poetry install

# To-do app entrypoint

ENTRYPOINT ["poetry","run","gunicorn", "-w", "4","--bind","0.0.0.0", "todo_app.app:create_app()"]

FROM base as development
