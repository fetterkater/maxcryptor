# MaxCryptor – Der magische QR-Verschlüssler
print("✨ Willkommen bei MaxCryptor ✨")
# QR-Verschlüsselungslogik kommt hier hin
# MaxCryptor – Der magische QR-Verschlüssler und Entschlüssler
# Benötigt: qrcode, pyzbar, pillow, cryptography

import qrcode
from cryptography.fernet import Fernet
from PIL import Image
from pyzbar.pyzbar import decode
import base64
import os

# Schlüssel generieren oder verwenden (in realer Nutzung: speichern!)
def get_key():
    if os.path.exists("secret.key"):
        with open("secret.key", "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open("secret.key", "wb") as f:
            f.write(key)
        return key

fernet = Fernet(get_key())

def encrypt_and_generate_qr(text, filename):
    encrypted = fernet.encrypt(text.encode())
    b64 = base64.urlsafe_b64encode(encrypted).decode()
    img = qrcode.make(b64)
    img.save(filename)
    print(f"QR-Code gespeichert als {filename}")

def scan_and_decrypt_qr(image_path):
    img = Image.open(image_path)
    decoded = decode(img)
    if not decoded:
        print("Kein QR-Code gefunden.")
        return
    data = decoded[0].data.decode()
    try:
        decrypted = fernet.decrypt(base64.urlsafe_b64decode(data)).decode()
        print("Entschlüsselt:", decrypted)
    except Exception as e:
        print("Fehler bei der Entschlüsselung:", e)

# Beispielnutzung:
if __name__ == "__main__":
    while True:
        mode = input("[E]ncrypt oder [D]ecrypt? (q zum Beenden): ").lower()
        if mode == "q":
            break
        elif mode == "e":
            klartext = input("Text zum Verschlüsseln: ")
            datei = input("Dateiname für QR-Code (z. B. geheim.png): ")
            encrypt_and_generate_qr(klartext, datei)
        elif mode == "d":
            pfad = input("Pfad zur QR-Bilddatei: ")
            scan_and_decrypt_qr(pfad)
        else:
            print("Ungültige Eingabe.")
