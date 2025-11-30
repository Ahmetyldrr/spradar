FROM python:3.11-slim

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizini
WORKDIR /app

# Python bağımlılıkları
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# .env dosyasını kopyala (Docker Compose override edecek)
COPY .env.docker /app/.env

# Uygulama dosyaları
COPY . .

# Dizinleri oluştur
RUN mkdir -p /app/logs /app/media /app/staticfiles

# Static files (ilk build'de)
RUN python manage.py collectstatic --noinput || true

# Port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Gunicorn başlat
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "--timeout", "300", "--access-logfile", "/app/logs/gunicorn-access.log", "--error-logfile", "/app/logs/gunicorn-error.log", "spradar_api.wsgi:application"]
