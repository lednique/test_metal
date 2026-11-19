#!/usr/bin/env python3
# Собирает один самодостаточный metal.html из index.html + textures/
# Использование:  python3 embed.py
# Результат: ../metal.html  (можно открыть двойным кликом, без сервера)
import base64, io, re, os
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))

def b64(b): return base64.b64encode(b).decode()

def normal_data_uri(path):
    im = Image.open(path).convert("RGB")
    w = 1800
    h = int(im.height * w / im.width)
    buf = io.BytesIO()
    im.resize((w, h), Image.LANCZOS).save(buf, format="JPEG", quality=92, optimize=True)
    return "data:image/jpeg;base64," + b64(buf.getvalue())

def file_data_uri(path, mime="image/jpeg"):
    return f"data:{mime};base64," + b64(open(path, "rb").read())

html = open(os.path.join(BASE, "index.html"), encoding="utf-8").read()
html = re.sub(r'(NORMAL_DATA=")[^"]+(")', r'\g<1>' + normal_data_uri(os.path.join(BASE, "textures/normal.png")) + r'\g<2>', html)
html = re.sub(r'(HDRI_DATA=")[^"]+(")', r'\g<1>' + file_data_uri(os.path.join(BASE, "textures/hdri.jpg")) + r'\g<2>', html)
html = re.sub(r'(ALU_DATA=")[^"]+(")', r'\g<1>' + file_data_uri(os.path.join(BASE, "textures/aluminum.jpg")) + r'\g<2>', html)

out = os.path.join(BASE, "..", "metal.html")
open(out, "w", encoding="utf-8").write(html)
print(f"OK: {out} ({os.path.getsize(out)//1024} KB)")
