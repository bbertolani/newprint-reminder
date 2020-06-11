
FROM python:3.7-alpine
ENV TZ America/Montreal
WORKDIR /app
COPY ./app requirements.txt ./
RUN pip install -r requirements.txt
RUN ["echo", "Container UP and RUNNING"]