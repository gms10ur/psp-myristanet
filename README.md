# PSP Portal - Modern Web Portal for PlayStation Portable

PSP cihazları için modern, yönetilebilir web portalı. Bu proje, PSP'nin kendi tarayıcısında çalışabilen hafif bir portal ile desktop üzerinden kolay yönetim imkanı sunar.

## 🚀 Özellikler

- **PSP Uyumlu**: PSP'nin dahili tarayıcısında mükemmel çalışır
- **Modern Yönetim**: Web tabanlı admin paneli ile kolay içerik yönetimi
- **Çoklu Dil**: Türkçe ve İngilizce dil desteği
- **Kategorize İçerik**: Firmware, Oyunlar, Eklentiler, Araçlar, Ekstralar ve RSS
- **Özel Oyun İndirme**: Oyunlar otomatik olarak `/ISO/{oyunAdı}.iso` formatında indirilir
- **Docker Desteği**: CasaOS ve diğer containerized ortamlarda kolayca çalışır
- **SQLite Veritabanı**: Hafif ve taşınabilir veritabanı

## 📋 Gereksinimler

- Python 3.11+
- Docker (opsiyonel)
- SQLite3

## 🛠️ Kurulum

### Docker ile Kurulum (Önerilen)

1. Repoyu klonlayın:

```bash
git clone https://github.com/gms10ur/psp-myristanet.git
cd psp-myristanet
```

2. Docker Compose ile başlatın:

```bash
docker-compose up -d
```

3. Portal `http://localhost:5001` adresinde çalışacaktır

### Manuel Kurulum

1. Python bağımlılıklarını yükleyin:

```bash
pip install -r requirements.txt
```

2. Uygulamayı başlatın:

```bash
python app.py
```

## 🎮 Kullanım

### PSP'de Kullanım

1. PSP'nizin ağ ayarlarını yapılandırın
2. Tarayıcıyı açın ve portal adresinize gidin
3. İstediğiniz kategoriden dosyaları indirin

### Yönetim Paneli

1. Web tarayıcısında `http://your-server:5000/admin` adresine gidin
2. Kategoriler arasında geçiş yapın
3. Yeni içerik ekleyin, düzenleyin veya silin
4. Dosya yükleyin ve otomatik boyut hesaplama özelliğinden yararlanın

## 📁 Proje Yapısı

```
psp-myristanet/
├── app.py              # Ana Flask uygulaması
├── requirements.txt    # Python bağımlılıkları
├── Dockerfile         # Docker yapılandırması
├── docker-compose.yml # Docker Compose yapılandırması
├── templates/         # HTML şablonları
│   ├── base.html     # Ana şablon
│   ├── index.html    # Ana sayfa (frame)
│   ├── main.html     # Portal ana sayfası
│   ├── category.html # Kategori detay sayfası
│   └── admin/        # Admin şablonları
├── images/           # PSP görsel dosyaları
├── downloads/        # İndirilebilir dosyalar
├── uploads/          # Yüklenen dosyalar
├── instance/         # SQLite veritabanı
└── static/          # Statik dosyalar
```

## 🔧 Yapılandırma

### Ortam Değişkenleri

- `SECRET_KEY`: Flask güvenlik anahtarı
- `FLASK_ENV`: production/development modu

### CasaOS Entegrasyonu

Docker Compose dosyasında CasaOS etiketleri bulunur. CasaOS'ta otomatik olarak tanınacaktır.

## 🌐 Kategori Sistemi

1. **Firmware**: Custom ve Original firmware dosyaları
2. **Games**: PSP oyun ISO'ları (otomatik `/ISO/` formatında)
3. **Plugins**: PSP eklentileri
4. **Tools**: Yardımcı araçlar
5. **Extras**: XMB ekstraları
6. **RSS**: RSS beslemeleri

## 🔒 Güvenlik

- Dosya yüklemeleri güvenli dosya adları ile yapılır
- Maksimum dosya boyutu 500MB ile sınırlıdır
- SQLite injection koruması vardır

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun
3. Commit yapın
4. Push edin
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🙏 Teşekkürler

Bu proje, orijinal Lusid's PSP Portal projesinden esinlenmiştir.

---

### Orijinal Proje Hakkında

Bu proje basit PSP portal sistemi üzerine geliştirilmiştir:

- Orijinal site: http://psp.lusidgames.com
