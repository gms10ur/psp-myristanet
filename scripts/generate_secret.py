#!/usr/bin/env python3
"""
PSP Portal - Güvenli SECRET_KEY Üretici
Bu script güvenli SECRET_KEY üretir ve .env dosyasını günceller
"""

import os
import secrets
import string


def generate_secret_key(length=64):
    """Güvenli SECRET_KEY üret"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def update_env_file(secret_key):
    """Mevcut .env dosyasını güncelle veya yeni oluştur"""
    env_path = ".env"

    if os.path.exists(env_path):
        # Mevcut .env dosyasını oku
        with open(env_path, "r") as f:
            lines = f.readlines()

        # SECRET_KEY satırını güncelle
        updated = False
        for i, line in enumerate(lines):
            if line.startswith("SECRET_KEY="):
                lines[i] = f"SECRET_KEY={secret_key}\n"
                updated = True
                break

        # Eğer SECRET_KEY yoksa ekle
        if not updated:
            lines.append(f"SECRET_KEY={secret_key}\n")

        # Dosyayı yaz
        with open(env_path, "w") as f:
            f.writelines(lines)
    else:
        # Yeni .env dosyası oluştur
        with open(env_path, "w") as f:
            f.write(f"SECRET_KEY={secret_key}\n")

    print("✅ .env dosyası güncellendi!")
    print(f"🔐 Yeni SECRET_KEY: {secret_key[:20]}...")


if __name__ == "__main__":
    print("🔧 PSP Portal - SECRET_KEY Üretici")
    print("=" * 40)

    # Yeni key üret
    new_key = generate_secret_key()

    print(f"📝 Oluşturulan SECRET_KEY ({len(new_key)} karakter)")
    print(f"🔐 Key: {new_key}")
    print()

    # .env dosyasını güncelle
    update_env_file(new_key)

    print()
    print("💡 İpuçları:")
    print("- Bu anahtarı güvenli bir yerde saklayın")
    print("- Üretim ortamında farklı bir anahtar kullanın")
    print("- .env dosyasını asla Git'e eklemeyin")
    print("- Anahtar sızdığında yeni bir tane üretin")
