# pull official base image
FROM python:3.8.18-slim-bullseye

# add tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

# add app
COPY . /src

# set working directory
WORKDIR /src

# install app dependencies
RUN pip install -r requirements.txt --no-cache-dir

CMD ["./docker-entrypoint.sh"]

