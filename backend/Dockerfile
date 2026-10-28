FROM python:3.13.9-slim-bookworm

ARG APP_VERSION=0.2
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_VERSION=${APP_VERSION}

WORKDIR /app

RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home --uid 10001 appuser
COPY app.py .
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000
CMD ["python", "app.py"]