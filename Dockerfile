FROM python:3.8

WORKDIR /code

COPY hello_world.py .

CMD [ "python", "hello_world.py" ]