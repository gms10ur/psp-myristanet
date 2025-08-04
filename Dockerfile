FROM python:3.11-slim

WORKDIR /app

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# SQLite veritabanı ve upload dizinlerini oluştur
RUN mkdir -p /app/instance /app/uploads /app/downloads

# Port 5001'i aç
EXPOSE 5001

# Uygulamayı başlat
CMD ["python", "app.py"]
