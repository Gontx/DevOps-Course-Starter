# Run Azure webhook
echo "About to run Azure webhook"
curl -dH -X POST ${WEBHOOK_URL}
echo "Success"