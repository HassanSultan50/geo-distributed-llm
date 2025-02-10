FROM python:3.8

WORKDIR /app
COPY . .

RUN pip install torch transformers grpcio grpcio-tools protobuf pymongo kafka-python

CMD ["python", "server.py"]

