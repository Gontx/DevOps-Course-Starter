# Run Azure webhook
echo "About to run Azure webhook"
webhook_url=$(terraform output webhook_url)
echo $webhook_url
curl --globoff -dH -X POST $webhook_url
echo "Success"