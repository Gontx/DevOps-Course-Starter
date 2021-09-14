# Get latest docker image from Docker Hub

docker login --username=_ --password=$(HEROKU_API_KEY) registry.heroku.com

# Tag it for Heroku

docker tag gontx/todo-app:latest registry.heroku.com/gontx-todo-app/web

# Push it to heroku registry

docker push registry.heroku.com/gontx-todo-app/web

container:release