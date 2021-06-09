# Use python:3.7 image as base
FROM python:buster

# Update pip
RUN apt-get update && pip install --upgrade pip
RUN apt-get install -y curl

# Install Poetry and add to path
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH = "${PATH}:/root/.poetry/bin"

# Install Gunicorn
RUN pip install gunicorn

# Expose Port 80
EXPOSE 80

# Copy code accross
COPY . /usr/DevOps-Course-Starter

WORKDIR /usr/DevOps-Course-Starter

# Install poetry dependencies and create .env
RUN poetry install

RUN cp .env.template .env

# To-do app entrypoint
CMD ["ls"]
#CMD ["ls"]

ENTRYPOINT [""]