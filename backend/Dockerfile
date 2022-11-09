FROM python:3.11.0-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


FROM python:3.11.0-slim

WORKDIR /app

COPY --from=builder  /app/wheels /wheels
COPY . ./

RUN pip install --no-cache /wheels/*
RUN pip install gunicorn
RUN pip install django-cors-headers

CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000"]

LABEL author='@anywindblows' version='0.1.0'