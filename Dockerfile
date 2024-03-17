FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN useradd -m appuser

WORKDIR /opt/app

COPY requirements.txt /opt/app/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /opt/app/
RUN chown -R appuser:appuser /opt/app
USER appuser

RUN chmod +x /opt/app/entrypoint.sh