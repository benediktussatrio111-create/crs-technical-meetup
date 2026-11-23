#!/usr/bin/env python3
"""Cari diksi berkonotasi negatif di catatan notulensi.

Pemakaian:
    python3 cek_diksi.py data.json            # cek semua slide notulensi di data deck
    python3 cek_diksi.py catatan.txt          # cek teks biasa

Menampilkan setiap temuan beserta kalimatnya dan opsi diksi yang lebih positif
(dari references/diksi.json). Skrip ini TIDAK mengubah apa pun: hasilnya harus
dikonfirmasi ke pengguna dulu. Daftar kata hanya bantuan; tetap baca catatan
secara utuh karena nada negatif juga bisa muncul tanpa kata-kata di daftar.
"""
import json
import re
import sys
from pathlib import Path

KAMUS = json.loads((Path(__file__).resolve().parent.parent / "references" / "diksi.json").read_text(encoding="utf-8"))
KAMUS.pop("_catatan", None)
# frasa netral yang memuat kata di daftar (mis. batas waktu "paling lambat")
PENGECUALIAN = re.compile(r"\b(paling lambat|selambat-lambatnya|tidak lupa|tidak masalah|bukan masalah|tanpa masalah)\b", re.IGNORECASE)
# frasa panjang dulu agar "tidak mampu" menang atas kata tunggal
POLA = sorted(KAMUS, key=len, reverse=True)
RE = re.compile(r"\b(" + "|".join(re.escape(k) for k in POLA) + r")\b", re.IGNORECASE)


def teks_dari_data(data):
    for s in data.get("slides", []):
        if s.get("type") != "notulensi":
            continue
        nama = s.get("nama", s.get("bidang", "?"))
        for tp in s.get("catatan") or []:
            h = tp.get("heading", "")
            yield f"{nama} › {h}", h
            for t in tp.get("poin") or []:
                yield f"{nama} › {h}", t
            for sb in tp.get("sub") or []:
                yield f"{nama} › {h} › {sb.get('judul', '')}", sb.get("judul", "")
                for t in sb.get("poin") or []:
                    yield f"{nama} › {h} › {sb.get('judul', '')}", t


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = Path(sys.argv[1])
    raw = path.read_text(encoding="utf-8")
    try:
        items = list(teks_dari_data(json.loads(raw)))
    except json.JSONDecodeError:
        items = [(f"baris {i}", ln) for i, ln in enumerate(raw.splitlines(), 1) if ln.strip()]
    n = 0
    for lokasi, teks in items:
        bersih = PENGECUALIAN.sub(lambda m: " " * len(m.group(0)), teks)
        for m in RE.finditer(bersih):
            n += 1
            kata = m.group(1)
            opsi = KAMUS[kata.lower()]
            print(f"[{n}] {lokasi}\n    \"{teks}\"\n    diksi: «{kata}» → opsi: " + " | ".join(opsi) + "\n")
    print(f"Total temuan: {n}" if n else "Tidak ada diksi negatif dari daftar. Tetap baca ulang nadanya secara utuh.")


if __name__ == "__main__":
    main()
