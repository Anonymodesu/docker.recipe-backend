# pull official base image
FROM python:3.8.18-slim-bullseye

# add tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

# install app dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

# add app
COPY src /src

# set working directory
WORKDIR /src

CMD ["./docker-entrypoint.sh"]

