# Run Azure webhook
echo "About to run Azure webhook"
curl -dH -X POST "$WEBHOOK_URL"
curl -dH -X POST "$(terraform output webhook_url)"
echo "Success"