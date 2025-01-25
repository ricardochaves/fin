FROM python:3-alpine

RUN pip install requests Flask Flask-Caching finnhub-python

WORKDIR /app

COPY app.py .

ENV FLASK_APP=app.py

ENTRYPOINT ["python", "app.py"]