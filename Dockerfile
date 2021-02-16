FROM python:3.8

WORKDIR /code

COPY hello_world.py /src/

CMD [ "python", "/src/hello_world.py" ]