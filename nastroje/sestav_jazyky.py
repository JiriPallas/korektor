"""Vytvoří jazykové verze KOREKTORU: de/ (KORREKTOR), en/ (PROOFREADER), sv/ (KORREKTUR)
a ikony s vlajkou pro všechny čtyři. Spustit ze složky KOREKTOR_WEB:  python nastroje/sestav_jazyky.py
Upravuje se jen index.html a jazyky.js v kořeni – tento skript pak vyrobí podsložky."""
import json, re
from pathlib import Path
from PIL import Image, ImageDraw

KOREN = Path(__file__).resolve().parent.parent
JAZYKY = {
    "cs": ("KOREKTOR", "KOREKTOR web", "cs"),
    "de": ("KORREKTOR", "KORREKTOR web", "de"),
    "en": ("PROOFREADER", "PROOFREADER web", "en"),
    "sv": ("KORREKTUR", "KORREKTUR web", "sv"),
}

def vlajka(kod, w, h):
    v = Image.new("RGB", (w, h), "white"); d = ImageDraw.Draw(v)
    if kod == "cs":
        d.rectangle([0, h // 2, w, h], fill="#D7141A")
        d.polygon([(0, 0), (w // 2, h // 2), (0, h)], fill="#11457E")
    elif kod == "de":
        for i, c in enumerate(["#000000", "#DD0000", "#FFCE00"]):
            d.rectangle([0, i * h // 3, w, (i + 1) * h // 3], fill=c)
    elif kod == "sv":
        d.rectangle([0, 0, w, h], fill="#006AA7")
        t = h // 5
        d.rectangle([0, h // 2 - t // 2, w, h // 2 + t // 2], fill="#FECC00")
        x = w * 5 // 16
        d.rectangle([x - t // 2, 0, x + t // 2, h], fill="#FECC00")
    elif kod == "en":
        d.rectangle([0, 0, w, h], fill="#012169")
        s = h // 5
        d.line([(0, 0), (w, h)], fill="white", width=s); d.line([(0, h), (w, 0)], fill="white", width=s)
        d.line([(0, 0), (w, h)], fill="#C8102E", width=s // 3); d.line([(0, h), (w, 0)], fill="#C8102E", width=s // 3)
        d.rectangle([w // 2 - s * 5 // 6, 0, w // 2 + s * 5 // 6, h], fill="white")
        d.rectangle([0, h // 2 - s * 5 // 6, w, h // 2 + s * 5 // 6], fill="white")
        d.rectangle([w // 2 - s // 2, 0, w // 2 + s // 2, h], fill="#C8102E")
        d.rectangle([0, h // 2 - s // 2, w, h // 2 + s // 2], fill="#C8102E")
    return v

def ikona(kod, cil):
    zaklad = Image.open(KOREN / "nastroje" / "ikona-zaklad-512.png").convert("RGBA")
    w, h = 250, 160                                  # vlajka vpravo dole, s bílým okrajem
    f = vlajka(kod, w, h)
    ram = Image.new("RGBA", (w + 24, h + 24), "white")
    ram.paste(f, (12, 12))
    zaklad.paste(ram, (512 - w - 24 - 18, 512 - h - 24 - 18))
    cil.mkdir(parents=True, exist_ok=True)
    zaklad.save(cil / "ikona-512.png")
    zaklad.resize((192, 192), Image.LANCZOS).save(cil / "ikona-192.png")

def manifest(kod, cil):
    nazev, dlouhy, lang = JAZYKY[kod]
    m = {"name": dlouhy, "short_name": nazev, "id": "./", "start_url": "./", "scope": "./", "lang": lang,
         "display": "standalone", "background_color": "#0B2A66", "theme_color": "#0B2A66",
         "icons": [{"src": "ikona-192.png", "sizes": "192x192", "type": "image/png"},
                   {"src": "ikona-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"}]}
    (cil / "manifest.webmanifest").write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")

sablona = (KOREN / "index.html").read_text(encoding="utf-8")
for kod in JAZYKY:
    cil = KOREN if kod == "cs" else KOREN / kod
    ikona(kod, cil); manifest(kod, cil)
    if kod == "cs":
        continue
    s = re.sub(r"/\*JAZYK\*/.*?/\*/JAZYK\*/", f'/*JAZYK*/const JAZYK = "{kod}", ZAKLAD = "../";/*/JAZYK*/', sablona, flags=re.S)
    s = s.replace('<script src="jazyky.js">', '<script src="../jazyky.js">').replace('<script src="hunspell.js">', '<script src="../hunspell.js">')
    s = s.replace('<html lang="cs">', f'<html lang="{kod}">')
    (cil / "index.html").write_text(s, encoding="utf-8")
    print("hotovo:", kod)
print("hotovo: cs (ikona + manifest)")
