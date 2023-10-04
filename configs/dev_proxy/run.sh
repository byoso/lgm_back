#! /bin/bash

set -e

echo "SSL disabled, enabling HTTP only"
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

nginx -g "daemon off;"
