FROM tiangolo/uwsgi-nginx-flask:python3.6

ENV NGINX_WORKER_PROCESSES auto

COPY ./app /app