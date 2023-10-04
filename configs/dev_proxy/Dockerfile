FROM nginxinc/nginx-unprivileged:1.23.2-alpine

COPY ./nginx/* /etc/nginx/
COPY ./run.sh /run.sh

USER root

RUN apk add --no-cache openssl bash && \
    mkdir -p /vol/static && \
    chmod -R 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown -R nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME /vol/static
VOLUME /vol/www

# USER nginx  # <- script fails if not root

CMD ["/run.sh"]
