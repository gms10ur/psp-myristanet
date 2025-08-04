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

# SQLite veritabanı dizinini oluştur
RUN mkdir -p /app/instance

# Port 5000'i aç
EXPOSE 5000

# Uygulamayı başlat
CMD ["python", "app.py"]
