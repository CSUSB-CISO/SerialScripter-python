FROM python:3.10.0-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN ["apk", "add", "nmap"]
WORKDIR /app
ENTRYPOINT git reset --hard staging && python main.py
