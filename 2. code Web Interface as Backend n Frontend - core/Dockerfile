from python:3.8-slim

COPY . /app
WORKDIR /app/bigdatadigitalent

RUN pip install -q Django sqlparse
CMD python manage.py runserver 0.0.0.0:8000
EXPOSE 8000
