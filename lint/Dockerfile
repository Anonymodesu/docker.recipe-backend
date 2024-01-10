FROM python:3.8.18-slim-bullseye

COPY . ./
RUN pip install -r requirements.txt --no-cache-dir

ENTRYPOINT ["./docker-entrypoint.sh"]