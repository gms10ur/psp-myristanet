# 🔧 Environment Variables Kılavuzu

## 📋 Hızlı Başlangıç

### 1. Environment Dosyalarını Hazırlayın

```bash
# .env.example dosyasını kopyalayın
cp .env.example .env

# Güvenli SECRET_KEY üretin
python3 scripts/generate_secret.py
```

### 2. Docker ile Çalıştırın

```bash
# Geliştirme ortamı
docker-compose up -d

# Üretim ortamı
FLASK_ENV=production docker-compose up -d
```

## 🔑 Environment Variables Açıklamaları

### 🛡️ Güvenlik Ayarları

| Değişken     | Açıklama                                 | Varsayılan         | Zorunlu  |
| ------------ | ---------------------------------------- | ------------------ | -------- |
| `SECRET_KEY` | Flask oturum şifreleme anahtarı          | your-secret-key... | ✅ Evet  |
| `FLASK_ENV`  | Uygulama ortamı (development/production) | production         | ❌ Hayır |

**SECRET_KEY Gereksinimleri:**

- En az 32 karakter uzunluğunda
- Büyük/küçük harf, rakam ve özel karakterler içermeli
- Her ortam için farklı olmalı
- Asla Git'e eklenmemeli

### 🎨 Görsel Tema Ayarları

| Değişken          | Açıklama                         | Varsayılan |
| ----------------- | -------------------------------- | ---------- |
| `COLOR_PRIMARY`   | Ana renk (arka plan, çerçeveler) | #252A34    |
| `COLOR_SECONDARY` | İkincil renk (linkler, vurgu)    | #08D9D6    |
| `COLOR_ACCENT`    | Accent renk (butonlar)           | #FF2E63    |
| `COLOR_LIGHT`     | Açık renk (metin)                | #EAEAEA    |

**Popüler Tema Örnekleri:**

```bash
# Klasik PSP Siyah
COLOR_PRIMARY=#000000
COLOR_SECONDARY=#0080FF
COLOR_ACCENT=#FF8000
COLOR_LIGHT=#FFFFFF

# Yeşil Doğa
COLOR_PRIMARY=#1B2624
COLOR_SECONDARY=#4ECDC4
COLOR_ACCENT=#45B7AF
COLOR_LIGHT=#F7FFF7

# Mavi Profesyonel
COLOR_PRIMARY=#2C3E50
COLOR_SECONDARY=#3498DB
COLOR_ACCENT=#E74C3C
COLOR_LIGHT=#ECF0F1
```

### ⚙️ Uygulama Ayarları

| Değişken             | Açıklama               | Varsayılan |
| -------------------- | ---------------------- | ---------- |
| `PORT`               | Sunucu portu           | 5001       |
| `DEFAULT_LANGUAGE`   | Varsayılan dil (tr/en) | tr         |
| `LOG_LEVEL`          | Log seviyesi           | INFO       |
| `MAX_CONTENT_LENGTH` | Max dosya boyutu (MB)  | 500        |

### 📱 PSP Optimizasyon

| Değişken                | Açıklama             | Varsayılan |
| ----------------------- | -------------------- | ---------- |
| `PSP_RESOLUTION_WIDTH`  | PSP ekran genişliği  | 480        |
| `PSP_RESOLUTION_HEIGHT` | PSP ekran yüksekliği | 272        |

## 🚀 Dağıtım Senaryoları

### 💻 Geliştirme Ortamı

```bash
# .env dosyası
SECRET_KEY=dev-only-key-not-for-production
FLASK_ENV=development
LOG_LEVEL=DEBUG
DEFAULT_LANGUAGE=tr
```

### 🏭 Üretim Ortamı

```bash
# .env dosyası
SECRET_KEY=super-secure-64-char-production-key-with-special-chars-123!@#
FLASK_ENV=production
LOG_LEVEL=INFO
DEFAULT_LANGUAGE=tr

# Özel renk teması
COLOR_PRIMARY=#1a1a1a
COLOR_SECONDARY=#00ff88
COLOR_ACCENT=#ff3366
COLOR_LIGHT=#f5f5f5
```

### 🐳 Docker Swarm / Kubernetes

```yaml
# Docker secrets kullanımı
version: "3.8"
services:
  psp-portal:
    image: gms10ur/psp-myristanet:latest
    environment:
      - SECRET_KEY_FILE=/run/secrets/secret_key
      - COLOR_PRIMARY=${COLOR_PRIMARY:-#252A34}
    secrets:
      - secret_key

secrets:
  secret_key:
    external: true
```

## 🔍 Sorun Giderme

### ❌ Yaygın Hatalar

**1. SECRET_KEY çok kısa**

```
Error: SECRET_KEY must be at least 32 characters
```

**Çözüm:** `python3 scripts/generate_secret.py` çalıştırın

**2. Renk formatı yanlış**

```
Warning: Invalid color format for COLOR_PRIMARY
```

**Çözüm:** Hex formatı kullanın: `#252A34`

**3. Port çakışması**

```
Error: Port 5001 already in use
```

**Çözüm:** Farklı port kullanın: `PORT=5002`

### 📝 Loglama

```bash
# Log seviyelerini ayarlayın
LOG_LEVEL=DEBUG    # Tüm detaylar
LOG_LEVEL=INFO     # Genel bilgiler (önerilen)
LOG_LEVEL=WARNING  # Sadece uyarılar
LOG_LEVEL=ERROR    # Sadece hatalar
```

### 🔄 Environment Değişikliklerini Uygulama

```bash
# Docker container'ı yeniden başlatın
docker-compose restart

# Veya tamamen yeniden oluşturun
docker-compose down && docker-compose up -d
```

## 🔒 Güvenlik En İyi Uygulamaları

1. **SECRET_KEY'i asla paylaşmayın**
2. **Her ortam için farklı SECRET_KEY kullanın**
3. **Environment dosyalarını Git'e eklemeyin**
4. **Üretimde mutlaka `FLASK_ENV=production` kullanın**
5. **Düzenli olarak SECRET_KEY'i değiştirin**
6. **Log seviyesini üretimde `INFO` veya üstü yapın**

## 📞 Destek

Environment variables ile ilgili sorunlarınız için:

- 📝 Logs'u kontrol edin: `docker-compose logs`
- 🔧 Script çalıştırın: `python3 scripts/generate_secret.py`
- 🆘 GitHub Issues'da soru sorun
