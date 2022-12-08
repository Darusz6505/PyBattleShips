FROM python:3.10.9-slim

COPY . /app

RUN pip3 install -r /app/requirements.txt

EXPOSE 8765

CMD python3 -u /app/main.py

