# Common setup stage
# Use python:buster image as base
FROM python:3.7.10-buster as base

# Update pip
RUN apt-get update && pip install --upgrade pip
RUN apt-get install -y curl

# Install Poetry and add to path
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH = "${PATH}:/root/.poetry/bin"

########################
# Production build stage
FROM base as production

# Expose Port 8000
EXPOSE 8000
EXPOSE 5000

# Set Workdir
WORKDIR /usr/DevOps-Course-Starter

# Copy code accross
COPY . /usr/DevOps-Course-Starter

WORKDIR /usr/DevOps-Course-Starter

# Install poetry dependencies 
RUN poetry install --no-dev

# To-do app entrypoint

ENTRYPOINT ["poetry","run","gunicorn", "-w", "4","--bind","0.0.0.0", "todo_app.app:create_app()"]

#########################
# Local Development stage
FROM base as development

# Set Workdir
WORKDIR /usr/DevOps-Course-Starter
# Copy requirements
COPY pyproject.toml /usr/DevOps-Course-Starter
COPY poetry.lock /usr/DevOps-Course-Starter

# Install poetry dependencies 

RUN poetry install

# Flask Server env
ENV FLASK_APP =todo_app.app
ENV FLASK_ENV=development

# App entrypoint
ENTRYPOINT ["poetry","run","flask","run","--host","0.0.0.0"]

###############
# Testing stage
FROM base as test

# Set Workdir
WORKDIR /usr/DevOps-Course-Starter

# Copy requirements
COPY pyproject.toml /usr/DevOps-Course-Starter
COPY poetry.lock /usr/DevOps-Course-Starter

# Install poetry dependencies 

RUN poetry install

ENTRYPOINT [ "poetry" , "run" , "pytest" ]