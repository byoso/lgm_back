server {
    listen 80;

    server_name ${DOMAIN} www.${DOMAIN};

    location /static {
        alias /vol/static/static;
    }

    location /admin {
        uwsgi_pass                  ${APP_HOST}:${APP_PORT};
        include                     /etc/nginx/uwsgi_params;
        client_max_body_size        ${MAX_UPLOAD_SIZE}M;
    }

    location /dsap {
        uwsgi_pass                  ${APP_HOST}:${APP_PORT};
        include                     /etc/nginx/uwsgi_params;
        client_max_body_size        ${MAX_UPLOAD_SIZE}M;
    }

    location /auth {
        uwsgi_pass                  ${APP_HOST}:${APP_PORT};
        include                     /etc/nginx/uwsgi_params;
        client_max_body_size        ${MAX_UPLOAD_SIZE}M;
    }

    location /dss {
        uwsgi_pass                  ${APP_HOST}:${APP_PORT};
        include                     /etc/nginx/uwsgi_params;
        client_max_body_size        ${MAX_UPLOAD_SIZE}M;
    }

    location /campains {
        uwsgi_pass                  ${APP_HOST}:${APP_PORT};
        include                     /etc/nginx/uwsgi_params;
        client_max_body_size        ${MAX_UPLOAD_SIZE}M;
    }

    location /home {
        uwsgi_pass                  ${APP_HOST}:${APP_PORT};
        include                     /etc/nginx/uwsgi_params;
        client_max_body_size        ${MAX_UPLOAD_SIZE}M;
    }

    location /users {
        uwsgi_pass                  ${APP_HOST}:${APP_PORT};
        include                     /etc/nginx/uwsgi_params;
        client_max_body_size        ${MAX_UPLOAD_SIZE}M;
    }

    location / {
        root /vol/static/static/dist;
        index index.html;
    }
}
