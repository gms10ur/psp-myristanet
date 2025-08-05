import os
from datetime import datetime

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    send_from_directory,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# .env dosyasını yükle
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # python-dotenv yoksa varsayılan değerleri kullan
    pass

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key-change-this")

# Renk paleti konfigürasyonu (hardcoded)
COLOR_PALETTE = {
    "primary": "#112D4E",  # Ana renk (koyu gri-mavi)
    "secondary": "#3F72AF",  # İkincil renk (orta gri-mavi)
    "accent": "#DBE2EF",  # Vurgu rengi (açık gri-mavi)
    "light": "#F9F7F7",  # Açık renk (çok açık gri)
}

# Veritabanı dosyasının tam yolunu oluştur
db_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "instance", "psp_portal.db"
)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["DOWNLOAD_FOLDER"] = "downloads"
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # 500MB max file size

# Klasörleri oluştur
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["DOWNLOAD_FOLDER"], exist_ok=True)
os.makedirs(os.path.dirname(db_path), exist_ok=True)

db = SQLAlchemy(app)

# Dil çevirileri
TRANSLATIONS = {
    "tr": {
        "title": "PSP Portal",
        "home": "Ev",
        "firmware": "Firmware",
        "games": "Oyunlar",
        "plugins": "Eklentiler",
        "tools": "Araçlar",
        "extras": "Ekstralar",
        "rss": "RSS Beslemeleri",
        "demos": "Demo Merkezi",
        "wallpapers": "Duvar Kağıtları",
        "homebrew": "Homebrew Store",
        "admin": "Yönetim",
        "download": "İndir",
        "size": "Boyut",
        "description": "Açıklama",
        "icon": "İkon",
        "category": "Kategori",
        "add_entry": "Yeni Giriş Ekle",
        "edit_entry": "Girişi Düzenle",
        "delete": "Sil",
        "edit": "Düzenle",
        "save": "Kaydet",
        "cancel": "İptal",
        "upload_file": "Dosya Yükle",
        "file_uploaded": "Dosya başarıyla yüklendi",
        "entry_added": "Giriş başarıyla eklendi",
        "entry_updated": "Giriş başarıyla güncellendi",
        "entry_deleted": "Giriş başarıyla silindi",
        "language": "Dil",
        "import_legacy": "Eski Verileri İçe Aktar",
        "import_success": "Eski veriler başarıyla içe aktarıldı",
    },
    "en": {
        "title": "PSP Portal",
        "home": "home",
        "firmware": "Firmware",
        "games": "Games",
        "plugins": "Plugins",
        "tools": "Tools",
        "extras": "Extras",
        "rss": "RSS Feeds",
        "demos": "Demo Center",
        "wallpapers": "Wallpapers",
        "homebrew": "Homebrew Store",
        "admin": "Administration",
        "download": "Download",
        "size": "Size",
        "description": "Description",
        "icon": "Icon",
        "category": "Category",
        "add_entry": "Add New Entry",
        "edit_entry": "Edit Entry",
        "delete": "Delete",
        "edit": "Edit",
        "save": "Save",
        "cancel": "Cancel",
        "upload_file": "Upload File",
        "file_uploaded": "File uploaded successfully",
        "entry_added": "Entry added successfully",
        "entry_updated": "Entry updated successfully",
        "entry_deleted": "Entry deleted successfully",
        "language": "Language",
        "import_legacy": "Import Legacy Data",
        "import_success": "Legacy data imported successfully",
    },
}


# Veritabanı modelleri
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    icon = db.Column(db.String(200))
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    entries = db.relationship(
        "Entry", backref="category", lazy=True, cascade="all, delete-orphan"
    )


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.String(50))
    icon_path = db.Column(db.String(500))
    download_path = db.Column(db.String(500))  # PSP için özel download yolu
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


def get_translation(lang, key):
    return TRANSLATIONS.get(lang, TRANSLATIONS["tr"]).get(key, key)


def get_localized_icon(base_icon, lang):
    """Dil bazlı ikon döndür"""
    if lang == "tr":
        # _tr versiyonu olup olmadığını kontrol et
        base_name = base_icon.replace("/images/", "").replace(".png", "")
        tr_icon = f"/images/{base_name}_tr.png"
        # Dosya var mı kontrol et
        import os

        tr_path = os.path.join("images", f"{base_name}_tr.png")
        if os.path.exists(tr_path):
            return tr_icon
    return base_icon


def init_db():
    """Veritabanını başlat ve örnek veriler ekle"""
    db.create_all()

    if Category.query.count() == 0:
        # Kategorileri oluştur
        categories = [
            {
                "name": "Firmware",
                "slug": "firmware",
                "icon": "/images/cfw.png",
                "order_index": 1,
            },
            {
                "name": "Games",
                "slug": "games",
                "icon": "/images/games.png",
                "order_index": 2,
            },
            {
                "name": "Plugins",
                "slug": "plugins",
                "icon": "/images/plugins.png",
                "order_index": 3,
            },
            {
                "name": "Tools",
                "slug": "tools",
                "icon": "/images/tools.png",
                "order_index": 4,
            },
            {
                "name": "Extras",
                "slug": "extras",
                "icon": "/images/xmbxtras.png",
                "order_index": 5,
            },
            {
                "name": "RSS",
                "slug": "rss",
                "icon": "/images/rss.png",
                "order_index": 6,
            },
            {
                "name": "Demos",
                "slug": "demos",
                "icon": "/images/demos.png",
                "order_index": 7,
            },
            {
                "name": "Wallpapers",
                "slug": "wallpapers",
                "icon": "/images/psnwallpapers.png",
                "order_index": 8,
            },
            {
                "name": "Homebrew",
                "slug": "homebrew",
                "icon": "/images/HomeBrewStore.png",
                "order_index": 9,
            },
        ]

        for cat_data in categories:
            category = Category(**cat_data)
            db.session.add(category)

        db.session.commit()


@app.before_request
def before_request():
    # Dil seçimi
    if "lang" not in request.args and "lang" not in request.cookies:
        lang = "tr"  # Varsayılan Türkçe
    else:
        lang = request.args.get("lang", request.cookies.get("lang", "tr"))

    request.lang = lang if lang in ["tr", "en"] else "tr"


@app.context_processor
def inject_globals():
    """Template'lere global değişkenleri enjekte et"""
    return {
        "colors": COLOR_PALETTE,
        "t": lambda k: get_translation(request.lang, k),
        "lang": request.lang,
        "get_localized_icon": lambda icon: get_localized_icon(icon, request.lang),
    }


# Ana rotalar
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/header")
def header_frame():
    return render_template("header.html")


@app.route("/footer")
def footer_frame():
    return render_template("footer.html")


@app.route("/main")
def main():
    categories = Category.query.order_by(Category.order_index).all()
    return render_template("main.html", categories=categories)


@app.route("/category/<slug>")
def category_detail(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    entries = Entry.query.filter_by(category_id=category.id).all()
    return render_template("category.html", category=category, entries=entries)


@app.route("/download/<int:entry_id>")
def download_file(entry_id):
    import glob

    entry = Entry.query.get_or_404(entry_id)

    # Dosyayı bulmak için sırayla farklı konumları dene
    possible_paths = [
        # 1. Downloads klasöründe (yeni yüklenen dosyalar)
        os.path.join(app.config["DOWNLOAD_FOLDER"], entry.file_path),
        # 2. CFW klasöründe recursive ara
        *glob.glob(os.path.join("cfw", "**", entry.file_path), recursive=True),
        # 3. OFW klasöründe ara
        os.path.join("xpd", "ofw", entry.file_path),
        # 4. Seplugins klasöründe recursive ara
        *glob.glob(os.path.join("seplugins", "**", entry.file_path), recursive=True),
        # 5. Extras klasöründe ara
        os.path.join("extras", entry.file_path),
        # 6. PDC klasöründe ara
        os.path.join("pdc", entry.file_path),
    ]

    # İlk bulunan dosyayı kullan
    file_path = None
    for path in possible_paths:
        if path and os.path.exists(path):
            file_path = path
            break

    if file_path and os.path.exists(file_path):
        # Games kategorisi için özel download path
        if entry.category.slug == "games":
            download_name = f"ISO/{entry.title}.iso"
        else:
            download_name = entry.file_path

        return send_file(file_path, as_attachment=True, download_name=download_name)
    else:
        flash(f"Dosya bulunamadı: {entry.file_path}", "error")
        return redirect(url_for("category_detail", slug=entry.category.slug))


# Admin rotalar
@app.route("/admin")
def admin():
    categories = Category.query.order_by(Category.order_index).all()
    return render_template("admin/index.html", categories=categories)


@app.route("/admin/entries")
def admin_entries():
    category_id = request.args.get("category_id")
    if category_id:
        entries = Entry.query.filter_by(category_id=category_id).all()
        category = Category.query.get(category_id)
    else:
        entries = Entry.query.all()
        category = None

    categories = Category.query.all()
    return render_template(
        "admin/entries.html",
        entries=entries,
        categories=categories,
        selected_category=category,
    )


@app.route("/admin/entry/add", methods=["GET", "POST"])
def admin_add_entry():
    if request.method == "POST":
        # Dosya yükleme işlemi
        if "file" in request.files:
            file = request.files["file"]
            if file and file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config["DOWNLOAD_FOLDER"], filename)
                file.save(file_path)

                # Dosya boyutunu hesapla
                file_size = os.path.getsize(file_path)
                file_size_mb = f"{file_size / (1024 * 1024):.1f}MB"

                # Entry oluştur
                entry = Entry(
                    title=request.form["title"],
                    description=request.form.get("description", ""),
                    file_path=filename,
                    file_size=file_size_mb,
                    category_id=request.form["category_id"],
                )

                db.session.add(entry)
                db.session.commit()

                flash(get_translation(request.lang, "entry_added"), "success")
                return redirect(url_for("admin_entries"))

    categories = Category.query.all()
    return render_template("admin/add_entry.html", categories=categories)


@app.route("/admin/entry/edit/<int:entry_id>", methods=["GET", "POST"])
def admin_edit_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)

    if request.method == "POST":
        entry.title = request.form["title"]
        entry.description = request.form.get("description", "")
        entry.category_id = request.form["category_id"]

        # Yeni dosya yüklendiyse
        if "file" in request.files:
            file = request.files["file"]
            if file and file.filename:
                # Eski dosyayı sil
                old_file_path = os.path.join(
                    app.config["DOWNLOAD_FOLDER"], entry.file_path
                )
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

                # Yeni dosyayı kaydet
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config["DOWNLOAD_FOLDER"], filename)
                file.save(file_path)

                entry.file_path = filename
                file_size = os.path.getsize(file_path)
                entry.file_size = f"{file_size / (1024 * 1024):.1f}MB"

        db.session.commit()
        flash(get_translation(request.lang, "entry_updated"), "success")
        return redirect(url_for("admin_entries"))

    categories = Category.query.all()
    return render_template("admin/edit_entry.html", entry=entry, categories=categories)


@app.route("/admin/entry/delete/<int:entry_id>", methods=["POST"])
def admin_delete_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)

    # Dosyayı sil
    file_path = os.path.join(app.config["DOWNLOAD_FOLDER"], entry.file_path)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(entry)
    db.session.commit()

    flash(get_translation(request.lang, "entry_deleted"), "success")
    return redirect(url_for("admin_entries"))


@app.route("/admin/import-legacy", methods=["POST"])
def admin_import_legacy():
    """XPD dosyalarından verileri içe aktar"""
    try:
        import_count = 0

        # Firmware kategorisi için CFW ve OFW dosyalarını XPD'lerden al
        firmware_category = Category.query.filter_by(slug="firmware").first()
        if firmware_category:
            # CFW klasöründeki XPD dosyalarını işle
            import_count += import_from_xpd_directory(
                "cfw", firmware_category.id, "CFW"
            )

            # OFW klasöründeki XPD dosyalarını işle (xpd/ofw altında)
            import_count += import_from_xpd_directory(
                "xpd/ofw", firmware_category.id, "OFW"
            )

        # Demos kategorisi için PDC'den veri al (eski sistem)
        demos_category = Category.query.filter_by(slug="demos").first()
        if demos_category:
            pdc_file = os.path.join("pdc", "main.html")
            if os.path.exists(pdc_file):
                import_count += import_from_pdc_html(pdc_file, demos_category.id)

        # Plugins kategorisi için seplugins'den veri al (eski sistem)
        plugins_category = Category.query.filter_by(slug="plugins").first()
        if plugins_category:
            plugins_file = os.path.join("seplugins", "main.html")
            if os.path.exists(plugins_file):
                import_count += import_from_plugins_html(
                    plugins_file, plugins_category.id
                )

        # Extras kategorisi için extras'dan veri al (eski sistem)
        extras_category = Category.query.filter_by(slug="extras").first()
        if extras_category:
            extras_file = os.path.join("extras", "main.html")
            if os.path.exists(extras_file):
                import_count += import_from_extras_html(extras_file, extras_category.id)

        db.session.commit()
        flash(
            f"{get_translation(request.lang, 'import_success')} ({import_count} giriş)",
            "success",
        )

    except Exception as e:
        db.session.rollback()
        flash(f"Import hatası: {str(e)}", "error")

    return redirect(url_for("admin"))


def import_from_cfw_html(file_path, category_id):
    """CFW HTML dosyasından verileri içe aktar"""
    # Bu fonksiyon eski CFW main.html dosyasını parse edecek
    # Şu an basit bir örnek implementasyon
    count = 0
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Basit regex ile download linklerini bul
            import re

            downloads = re.findall(r'<a href="([^"]+\.xpd)"[^>]*>([^<]+)</a>', content)
            for download_url, title in downloads:
                # Dosya zaten var mı kontrol et
                existing = Entry.query.filter_by(title=title.strip()).first()
                if not existing:
                    entry = Entry(
                        title=title.strip(),
                        description=f"CFW dosyası: {title}",
                        file_path=download_url.split("/")[-1],
                        file_size="N/A",
                        category_id=category_id,
                    )
                    db.session.add(entry)
                    count += 1
    except Exception as e:
        print(f"CFW import error: {e}")

    return count


def import_from_ofw_html(file_path, category_id):
    """OFW HTML dosyasından verileri içe aktar"""
    count = 0
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            import re

            downloads = re.findall(r'<a href="([^"]+\.xpd)"[^>]*>([^<]+)</a>', content)
            for download_url, title in downloads:
                existing = Entry.query.filter_by(title=title.strip()).first()
                if not existing:
                    entry = Entry(
                        title=title.strip(),
                        description=f"OFW dosyası: {title}",
                        file_path=download_url.split("/")[-1],
                        file_size="N/A",
                        category_id=category_id,
                    )
                    db.session.add(entry)
                    count += 1
    except Exception as e:
        print(f"OFW import error: {e}")

    return count


def import_from_pdc_html(file_path, category_id):
    """PDC HTML dosyasından demo verilerini içe aktar"""
    count = 0
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            import re

            # PDC formatında tablo verilerini parse et
            table_rows = re.findall(
                r'<tr[^>]*>.*?<td[^>]*><img[^>]+></td>.*?<td[^>]*>([^<]+)</td>.*?<td[^>]*>([^<]+)</td>.*?<td[^>]*><a href="([^"]+)"[^>]*>',
                content,
                re.DOTALL,
            )
            for title, size, download_url in table_rows:
                existing = Entry.query.filter_by(title=title.strip()).first()
                if not existing:
                    entry = Entry(
                        title=title.strip(),
                        description=f"PSP Demo: {title}",
                        file_path=download_url.split("/")[-1],
                        file_size=size.strip(),
                        category_id=category_id,
                    )
                    db.session.add(entry)
                    count += 1
    except Exception as e:
        print(f"PDC import error: {e}")

    return count


def import_from_plugins_html(file_path, category_id):
    """Plugins HTML dosyasından verileri içe aktar"""
    count = 0
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            import re

            downloads = re.findall(r'<a href="([^"]+\.xpd)"[^>]*>([^<]+)</a>', content)
            for download_url, title in downloads:
                existing = Entry.query.filter_by(title=title.strip()).first()
                if not existing:
                    entry = Entry(
                        title=title.strip(),
                        description=f"PSP Plugin: {title}",
                        file_path=download_url.split("/")[-1],
                        file_size="N/A",
                        category_id=category_id,
                    )
                    db.session.add(entry)
                    count += 1
    except Exception as e:
        print(f"Plugins import error: {e}")

    return count


def import_from_seplugins_html(file_path, category_id):
    """Seplugins HTML dosyasından verileri içe aktar"""
    count = 0
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            import re

            # Plugin indirme linklerini bul
            downloads = re.findall(
                r'href="([^"]+\.(?:xpd|prx))"[^>]*>([^<]+)</a>', content
            )
            for download_url, title in downloads:
                existing = Entry.query.filter_by(title=title.strip()).first()
                if not existing:
                    entry = Entry(
                        title=title.strip(),
                        description=f"PSP Plugin: {title}",
                        file_path=download_url.split("/")[-1],
                        file_size="N/A",
                        category_id=category_id,
                    )
                    db.session.add(entry)
                    count += 1
    except Exception as e:
        print(f"Seplugins import error: {e}")

    return count


def import_from_extras_html(file_path, category_id):
    """Extras HTML dosyasından verileri içe aktar"""
    count = 0
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            import re

            downloads = re.findall(r'<a href="([^"]+\.xpd)"[^>]*>([^<]+)</a>', content)
            for download_url, title in downloads:
                existing = Entry.query.filter_by(title=title.strip()).first()
                if not existing:
                    entry = Entry(
                        title=title.strip(),
                        description=f"PSP Extra: {title}",
                        file_path=download_url.split("/")[-1],
                        file_size="N/A",
                        category_id=category_id,
                    )
                    db.session.add(entry)
                    count += 1
    except Exception as e:
        print(f"Extras import error: {e}")

    return count


def parse_xpd_file(file_path):
    """XPD dosyasını parse eder ve içindeki bilgileri döndürür"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        xpd_data = {}
        current_section = None

        for line in content.split("\n"):
            line = line.strip()
            if not line:
                continue

            if line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1]
                continue

            if "=" in line and current_section:
                key, value = line.split("=", 1)
                if current_section not in xpd_data:
                    xpd_data[current_section] = {}
                xpd_data[current_section][key] = value

        return xpd_data
    except Exception as e:
        print(f"XPD parse error for {file_path}: {e}")
        return None


def import_from_xpd_directory(directory_path, category_id, prefix):
    """Belirtilen klasördeki tüm XPD dosyalarını içe aktarır"""
    import glob

    count = 0

    try:
        # XPD dosyalarını recursive olarak bul
        xpd_pattern = os.path.join(directory_path, "**", "*.xpd")
        xpd_files = glob.glob(xpd_pattern, recursive=True)

        for xpd_file in xpd_files:
            xpd_data = parse_xpd_file(xpd_file)
            if not xpd_data or "Info" not in xpd_data:
                continue

            info = xpd_data["Info"]
            desc = info.get("Desc", "Unknown")
            size = info.get("Size", "N/A")
            code = info.get("Code", "")

            # Dosya yolunu belirle (XPD dosyasının kendisi)
            file_name = os.path.basename(xpd_file)

            # Başlığı düzenle
            title = f"{prefix}: {desc}"

            # Açıklama oluştur
            description = f"{prefix} - {desc}"
            if code:
                description += f" (Kod: {code})"

            # XPD dosyasındaki gerçek download linkini de açıklamaya ekle
            if "File" in xpd_data and "C" in xpd_data["File"]:
                real_download_url = xpd_data["File"]["C"]
                description += f"\nGerçek dosya: {real_download_url}"

            # Size bilgisini düzenle
            if size != "N/A" and size.isdigit():
                size_kb = int(size)
                if size_kb > 1024:
                    size_display = f"{size_kb / 1024:.1f} MB"
                else:
                    size_display = f"{size_kb} KB"
            else:
                size_display = size

            # Zaten var mı kontrol et
            existing = Entry.query.filter_by(title=title).first()
            if not existing:
                entry = Entry(
                    title=title,
                    description=description,
                    file_path=file_name,  # XPD dosyası artık downloads klasöründe
                    file_size=size_display,
                    category_id=category_id,
                )
                db.session.add(entry)
                count += 1
                print(f"Added: {title}")
            else:
                print(f"Skipped (exists): {title}")

    except Exception as e:
        print(f"XPD directory import error for {directory_path}: {e}")

    return count


@app.route("/set_language/<lang>")
def set_language(lang):
    response = redirect(request.referrer or url_for("index"))
    response.set_cookie("lang", lang, max_age=60 * 60 * 24 * 365)  # 1 yıl
    return response


# Static dosyalar için route
@app.route("/images/<path:filename>")
def serve_images(filename):
    return send_from_directory("images", filename)


@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)


if __name__ == "__main__":
    with app.app_context():
        init_db()
    port = int(os.environ.get("PORT", 5001))  # Default port 5001
    app.run(host="0.0.0.0", port=port, debug=True)
