# Get latest docker image from Docker Hub
echo "Login to docker & heroku"
docker login --username=_ --password=${HEROKU_API_KEY} registry.heroku.com

# Tag it for Heroku
echo "Tag image for heroku"
docker tag gontx/todo-app:latest registry.heroku.com/gontx-todo-app/web

# Push it to heroku registry
echo "push image to heroku"
docker push registry.heroku.com/gontx-todo-app/web

heroku container:release web