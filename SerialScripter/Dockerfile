FROM python:3.10.0-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN apk update
RUN apk add nmap openssh
RUN mkdir /var/log/rsyslog
WORKDIR /app
ENTRYPOINT python main.py
