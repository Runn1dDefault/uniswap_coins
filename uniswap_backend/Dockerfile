FROM python:3.8.3-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

COPY ./ /app/uniswap_backend/
# CMD ['ls']
RUN pip install --upgrade pip
RUN ["chmod", "+x", "/app/uniswap_backend/maker-entrypoint.sh"]

RUN pip install -r /app/uniswap_backend/requirements.txt
RUN pip install gunicorn
