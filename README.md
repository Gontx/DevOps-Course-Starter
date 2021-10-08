# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.tempalate` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

### TRELLO
This app uses a web service called trello to manage the to-do items. You will therefore need to set up the Trello API authentification for it to work properly:

### AUTHENTIFICATION
Add API key, token and Trello board id .env file

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


## Testing
A number of unit tests have been added in /tests folder. This tests make use of items_pickle file to load a hardcoded set of items.

### Requirements:
Add chromedriver.exe to your project path

### How to run the tests
Using VSCode add [Test Explorer UI extension](https://marketplace.visualstudio.com/items?itemName=hbenl.vscode-test-explorer) and [Python Test Explorer for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=LittleFoxTeam.vscode-python-test-adapter). Navigate to extension GUI and execute tests.

To run from command line:
```bash
$ poetry run pytest
```

## Vagrant
Navigate to repository root directory and run:
```bash
$ vagrant up
```
This command will provision a VM with the requirements needed for the To-Do app and start it automatically.

The app is accessible on http://127.0.0.1:5000/ 

## Docker

A production and a development container are available.

### Production:
To build the production container:

```bash
$ docker build --target production  --tag todo-app:prod .
```

To run the app within the production container:

```bash 
$ docker run --env-file .env -p 8000:8000 todo-app:prod
```
Docker will pick your environment variables from your local .env file. Make sure to have it up to date.

The app is accesible locally on: http://localhost:8000/ 


### Development:
To build the development container:

```bash
$ docker build --target development  --tag todo-app:dev .
```
To run the development application with the local repository binded to the container:

```bash
$ docker run --env-file ./.env -p 5000:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/usr/DevOps-Course-Starter/todo_app todo-app:dev
```

Docker will pick your environment variables from your local .env file. Make sure to have it up to date.

The app is accesible locally on: http://localhost:5000/ 


### Testing:
To build the testing container: 


```bash
$ docker build --target test --tag todo-app:test .
```

To run the testing container:

```bash
$ docker run --env-file ./.env todo-app:test
```

## Travis CI
Travis will build each push and run the dockerized tests.

Check build status at [Travis](https://app.travis-ci.com/github/Gontx/DevOps-Course-Starter)

## Heroku CD
Travis will take care of deployment to Heroku.

To run your Heroku app, go to [gontx-todo-app](https://gontx-todo-app.herokuapp.com/)

In case you want to locally push your application to Heroku manually, run on Heroku CLI:
```bash
# Log in
$ heroku login
$ heroku container:login
# Build production latest image and push it
$ docker login
$ docker build --target production --tag gontx/todo-app:latest .
$ docker push gontx/todo-app:latest
# Pull latest image
$ docker pull gontx/todo-app:latest
# Tag the image 
$ docker tag gontx/todo-app:latest registry.heroku.com/gontx-todo-app/web
# Push the image to heroku
$ docker push registry.heroku.com/gontx-todo-app/web
# Release the Container
$ heroku container:release web
# Open web 
$ heroku open
```
### MONGO DB
To connect to MongoDB Atlas:
```bash
$ client = pymongo.MongoClient("mongodb+srv://<USER_NAME>:<PASSWORD>@<MONGO_URL>/<DEFAULT_DATABASE>?w=majority")
$ client.list_database_names()['admin', 'local']
```