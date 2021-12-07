# Run Azure webhook
echo "About to run Azure webhook"
#curl -dH -X POST "$WEBHOOK_URL"
terraform apply -var client_id=$CLIENT_ID -var client_secret=$CLIENT_SECRET -var secret_key=$SECRET_KEY
curl -dH -X POST "$(terraform output webhook_url)"
echo "Success"