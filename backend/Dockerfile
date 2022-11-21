FROM python:3.7.0-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


FROM python:3.7.0-slim

WORKDIR /app

COPY --from=builder  /app/wheels /wheels
COPY . ./

RUN pip install --upgrade pip && pip install --no-cache /wheels/* && \
    pip install gunicorn && \
    mkdir -p /usr/share/fonts/truetype/ && \
    install -m644 ./fonts/DejaVuSerif.ttf /usr/share/fonts/truetype/ && \
    rm -Rf ./fonts

LABEL author='@anywindblows' version='0.1.1'