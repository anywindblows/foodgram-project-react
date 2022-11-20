FROM python:3.7.0-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


FROM python:3.7.0-slim

WORKDIR /app

COPY --from=builder  /app/wheels /wheels
COPY . ./

RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*
RUN pip install gunicorn

RUN mkdir -p /usr/share/fonts/truetype/
RUN install -m644 ./fonts/DejaVuSerif.ttf /usr/share/fonts/truetype/
RUN rm ./fonts/DejaVuSerif.ttf

LABEL author='@anywindblows' version='0.1.0'