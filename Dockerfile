
FROM python:3.7-alpine
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
RUN ["echo", "Container UP and RUNNING"]