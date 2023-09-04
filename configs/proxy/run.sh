#! /bin/bash

set -e

if [ "$USE_SSL_CERTIFICATE" == "1" ]; then

    echo "checking for dhparams.pem"
    if [ ! -f "/vol/proxy/ssl-dhparams.pem" ]; then
        echo "dhparams.pem does not exist, creating it"
        openssl dhparam -out /vol/proxy/ssl-dhparams.pem 2048
    fi

    # Avoid replacing this with envsubst
    export host=\$host
    export request_uri=\$request_uri

    echo "Checking for fullchain.pem"
    if [ ! -f "/etc/letsencrypt/live/${DOMAIN}/fullchain.pem" ]; then
        echo "No SSL certificate found, enabling HTTP only"
        envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
    else
        echo "SSL certificate found, enabling HTTPS"
        envsubst < /etc/nginx/default-ssl.conf.tpl > /etc/nginx/conf.d/default.conf
    fi
else
    echo "SSL disabled, enabling HTTP only"
    envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
fi

nginx -g "daemon off;"
