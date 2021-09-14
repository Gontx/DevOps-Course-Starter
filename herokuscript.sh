# Get latest docker image from Docker Hub
echo "Login to docker & heroku"
docker login --username=_ --password=${HEROKU_API_KEY} registry.heroku.com
# Tag it for Heroku
echo "Tag image for heroku"
docker tag gontx/todo-app:latest registry.heroku.com/gontx-todo-app/web
# Push it to heroku registry
echo "Push image to heroku"
docker push registry.heroku.com/gontx-todo-app/web
echo "Release web"
heroku container:release web
echo "You made it"