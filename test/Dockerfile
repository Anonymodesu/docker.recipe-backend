ARG BASE_IMAGE
FROM ${BASE_IMAGE}

COPY . /test/

RUN pip install -r /test/requirements.txt --no-cache-dir 

CMD ["pytest", "-rA", "/test"]
