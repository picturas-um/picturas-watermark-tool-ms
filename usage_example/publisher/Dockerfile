FROM python:3.13-slim

RUN pip install pika

COPY publisher.py ./

ENTRYPOINT ["python", "publisher.py"]
