#! /bin/sh

# Wait for proxy to be available then get the first certificate

set -e

until nc -z proxy 80; do
    echo "Waiting for nginx to be available..."
    sleep 2s
done

echo "Trying to get a certificate..."
echo "- Domain: $DOMAIN"
echo "- Domain owner email: $ACME_DEFAULT_EMAIL"

certbot certonly \
    --webroot \
    --webroot-path "/vol/www/" \
    -d "$DOMAIN" \
    -d www."$DOMAIN" \
    --email $ACME_DEFAULT_EMAIL \
    --rsa-key-size 4096 \
    --agree-tos \
    --non-interactive


echo "Certificate obtained."
