FROM python:3.8

WORKDIR /app

COPY . /app
RUN pip install -r /app/requirements/dist.txt

EXPOSE 8080

CMD ["docker/production/run_production.sh"]
