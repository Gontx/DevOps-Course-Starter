# Run Azure webhook
echo "About to run Azure webhook"

webhook_url=$(terraform output webhook_url)
webhook_url_stripped=$(echo $webhook_url | tr -d '"')
curl --globoff -dH -X POST $webhook_url_stripped
echo "Success"