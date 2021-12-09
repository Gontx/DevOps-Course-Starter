# Run Azure webhook
echo "About to run Azure webhook"
curl --globoff -dH -X POST '$(terraform output -raw webhook_url)'
echo "Success"