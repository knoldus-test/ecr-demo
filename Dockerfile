FROM python:3.8-alpine

WORKDIR /code

COPY hello_world.py /src/

RUN  \
  apk update \
&& \
  apk add --no-cache py3-pip \
&& \  
  apk add --no-cache --virtual .build-deps \
    docker

CMD [ "python", "/src/hello_world.py" ]