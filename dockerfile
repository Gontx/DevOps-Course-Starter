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

# Set Workdir
WORKDIR /usr/DevOps-Course-Starter

# Copy code accross
COPY . /usr/DevOps-Course-Starter

WORKDIR /usr/DevOps-Course-Starter

# Install poetry dependencies 
RUN poetry config virtualenvs.create false --local && poetry install

# To-do app entrypoint

#ENTRYPOINT ["poetry","run","gunicorn", "-w", "4","--bind","0.0.0.0", "todo_app.app:create_app()"]

CMD /usr/DevOps-Course-Starter/entrypoint.sh

#########################
# Local Development stage
FROM base as development

# Set Workdir
WORKDIR /usr/DevOps-Course-Starter
# Copy requirements
COPY pyproject.toml /usr/DevOps-Course-Starter
COPY poetry.lock /usr/DevOps-Course-Starter

# Install poetry dependencies 

RUN poetry config virtualenvs.create false --local && poetry install

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
RUN poetry config virtualenvs.create false --local && poetry install

# Flask Server env
ENV FLASK_APP =todo_app.app
ENV FLASK_ENV=development

# Install Chrome
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb &&\
    apt-get install ./chrome.deb -y &&\
    rm ./chrome.deb

# Install Chromium WebDriver
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` &&\
    echo "Installing chromium webdriver version ${LATEST}" &&\
    curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip &&\
    apt-get install unzip -y &&\
    unzip ./chromedriver_linux64.zip

# Copy tests and mock items
COPY tests /usr/DevOps-Course-Starter/
COPY items_pickle /usr/DevOps-Course-Starter/

# Copy app code
COPY todo_app /usr/DevOps-Course-Starter/todo_app

# Copy fake env
COPY .env.test /usr/DevOps-Course-Starter/

ENTRYPOINT [ "poetry" , "run" , "pytest" ]