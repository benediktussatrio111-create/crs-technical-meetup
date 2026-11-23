#!/usr/bin/env python3
"""Bangun deck informasi acara CRS Ecosystem (16:9) dari file data JSON.

Pemakaian:
    python3 build_deck.py data.json output.html

Hanya memakai pustaka standar Python. Hasilnya satu file HTML mandiri
(CSS disisipkan) yang bisa dibuka di browser, dipublikasikan, atau dicetak
ke PDF 1920x1080 (Print -> Save as PDF, margin None).
Struktur data: lihat ../references/schema.md dan ../examples/.
"""
import json
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSS = (HERE.parent / "references" / "deck.css").read_text(encoding="utf-8")

BIDANG_WARNA = {"produksi", "marketing", "financial", "sdm", "blue", "violet"}


def e(x):
    return escape(str(x if x is not None else "…"))


def kelas(warna):
    w = (warna or "blue").lower()
    return "k-" + (w if w in BIDANG_WARNA else "blue")


# ---------------------------------------------------------------- ilustrasi
# Ilustrasi vektor sederhana bergaya "3D lembut" (gradien + bayangan).
# Bukan salinan aset PDF referensi; dibuat ulang agar plugin mandiri.
_uid = [0]


def _g(c1, c2):
    _uid[0] += 1
    gid = f"g{_uid[0]}"
    return gid, (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0.4" y2="1">'
                 f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>')


PAL = {
    "blue": ("#60a5fa", "#1d4ed8"), "violet": ("#c4b5fd", "#7c3aed"),
    "green": ("#6ee7b7", "#059669"), "pink": ("#f9a8d4", "#db2777"),
    "amber": ("#fde68a", "#d97706"), "orange": ("#fdba74", "#ea580c"),
}


def person(cx, cy, s, col):
    g1, d1 = _g(*PAL[col])
    g2, d2 = _g(*PAL[col])
    return (f"<defs>{d1}{d2}</defs>"
            f'<path d="M{cx-s},{cy+1.9*s} C{cx-s},{cy+0.75*s} {cx-0.55*s},{cy+0.55*s} {cx},{cy+0.55*s} '
            f'C{cx+0.55*s},{cy+0.55*s} {cx+s},{cy+0.75*s} {cx+s},{cy+1.9*s} Z" fill="url(#{g2})"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{0.5*s}" fill="url(#{g1})"/>'
            f'<ellipse cx="{cx-0.15*s}" cy="{cy-0.2*s}" rx="{0.16*s}" ry="{0.1*s}" fill="#fff" opacity=".45"/>')


def svg(inner, vb="0 0 200 200"):
    return f'<svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'


def shadow(cx, cy, rx):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{rx*0.12}" fill="#0b1220" opacity=".08"/>'


def ic_person(col="blue"):
    return svg(shadow(100, 190, 70) + person(100, 70, 70, col))


def ic_group(cols=("violet", "blue", "green")):
    a, b, c = cols
    return svg(shadow(100, 186, 90) + person(48, 82, 40, a) + person(152, 82, 40, c) + person(100, 92, 48, b))


def ic_crowd():
    return svg(shadow(200, 380, 190) +
               person(120, 120, 70, "violet") + person(290, 110, 70, "amber") +
               person(80, 210, 78, "green") + person(320, 210, 78, "pink") + person(200, 200, 92, "blue"),
               "0 0 400 400")


def ic_meeting():
    g, d = _g("#f1f5f9", "#cbd5e1")
    gc, dc = _g("#fcd34d", "#f59e0b")
    return svg(f"<defs>{d}{dc}</defs>" + shadow(200, 372, 170) +
               person(110, 150, 52, "violet") + person(290, 160, 50, "green") + person(200, 130, 62, "blue") +
               f'<rect x="160" y="200" width="80" height="54" rx="10" fill="#1e3a8a"/>'
               f'<rect x="168" y="208" width="64" height="38" rx="6" fill="#3b82f6"/>'
               f'<rect x="50" y="250" width="300" height="46" rx="20" fill="url(#{g})"/>'
               f'<rect x="80" y="292" width="22" height="70" rx="6" fill="#cbd5e1"/>'
               f'<rect x="298" y="292" width="22" height="70" rx="6" fill="#cbd5e1"/>'
               f'<path d="M250,30 h110 a22,22 0 0 1 22,22 v50 a22,22 0 0 1 -22,22 h-50 l-26,26 v-26 h-34 a22,22 0 0 1 -22,-22 v-50 a22,22 0 0 1 22,-22z" fill="url(#{gc})"/>'
               '<circle cx="280" cy="77" r="9" fill="#fff"/><circle cx="306" cy="77" r="9" fill="#fff"/><circle cx="332" cy="77" r="9" fill="#fff"/>',
               "0 0 400 400")


def ic_building(label):
    g, d = _g("#60a5fa", "#1d4ed8")
    gp, dp = _g("#93c5fd", "#2563eb")
    wins = "".join(f'<rect x="{x}" y="{y}" width="34" height="26" rx="6" fill="#dbeafe"/>'
                   for y in (120, 162, 204) for x in (130, 180, 230))
    lab = e(label.upper())[:12]
    return svg(f"<defs>{d}{dp}</defs>" + shadow(210, 370, 150) +
               f'<rect x="108" y="84" width="196" height="270" rx="26" fill="url(#{g})"/>{wins}'
               f'<rect x="96" y="46" width="220" height="50" rx="14" fill="#0b1220"/>'
               f'<text x="206" y="81" font-family="Inter,Arial" font-weight="800" font-size="26" letter-spacing="4" fill="#fbbf24" text-anchor="middle">{lab}</text>'
               '<path d="M182,354 v-58 a24,24 0 0 1 48,0 v58z" fill="#fbbf24"/>'
               f'<path d="M60,214 a44,44 0 0 1 88,0 c0,34 -44,78 -44,78 c0,0 -44,-44 -44,-78z" fill="url(#{gp})"/>'
               '<circle cx="104" cy="214" r="15" fill="#fff"/>', "0 0 400 400")


def ic_calendar(day):
    return svg('<rect x="24" y="40" width="152" height="140" rx="26" fill="#fff" stroke="#e7ebf3" stroke-width="6"/>'
               '<path d="M24,66 a26,26 0 0 1 26,-26 h100 a26,26 0 0 1 26,26 v24 h-152z" fill="#2563eb"/>'
               '<rect x="58" y="22" width="14" height="36" rx="7" fill="#1e3a8a"/><rect x="128" y="22" width="14" height="36" rx="7" fill="#1e3a8a"/>'
               f'<text x="100" y="158" font-family="Inter,Arial" font-weight="800" font-size="62" fill="#0b1220" text-anchor="middle">{e(day)}</text>')


def ic_shirt():
    g, d = _g("#475569", "#0b1220")
    return svg(f"<defs>{d}</defs>" + shadow(100, 186, 60) +
               f'<path d="M70,30 l-52,26 l18,48 l22,-8 v86 h84 v-86 l22,8 l18,-48 l-52,-26 c-4,16 -16,24 -30,24 c-14,0 -26,-8 -30,-24z" fill="url(#{g})"/>')


def ic_clock():
    return svg('<circle cx="100" cy="100" r="80" fill="#fff" stroke="#2563eb" stroke-width="14"/>'
               '<path d="M100,52 v52 l32,20" stroke="#0b1220" stroke-width="12" fill="none" stroke-linecap="round"/>')


def ic_chart():
    g, d = _g("#86efac", "#059669")
    bars = "".join(f'<rect x="{x}" y="{y}" width="26" height="{170-y}" rx="6" fill="url(#{g})"/>'
                   for x, y in ((34, 120), (74, 96), (114, 70), (154, 44)))
    return svg(f"<defs>{d}</defs>{bars}"
               '<path d="M26,118 L80,74 L112,92 L172,30" stroke="#ea580c" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
               '<path d="M150,26 l28,-2 l-4,28z" fill="#ea580c"/>')


def ic_coins():
    g, d = _g("#fde68a", "#d97706")
    stack = "".join(f'<ellipse cx="90" cy="{y}" rx="62" ry="20" fill="url(#{g})" stroke="#b45309" stroke-width="3"/>'
                    for y in (160, 136, 112, 88, 64))
    return svg(f"<defs>{d}</defs>" + shadow(90, 186, 70) + stack +
               f'<circle cx="160" cy="54" r="26" fill="url(#{g})" stroke="#b45309" stroke-width="3"/>')


def ic_brush():
    g, d = _g("#f9a8d4", "#db2777")
    return svg(f"<defs>{d}</defs>" + shadow(100, 186, 70) +
               '<rect x="28" y="40" width="144" height="120" rx="18" fill="#fff" stroke="#e7ebf3" stroke-width="6"/>'
               f'<path d="M48,130 c20,-50 40,10 60,-30 s30,-20 44,-30" stroke="url(#{g})" stroke-width="14" fill="none" stroke-linecap="round"/>'
               '<path d="M150,24 l26,26 l-60,60 l-30,4 l4,-30z" fill="#7c3aed"/>')


def ic_bed():
    return svg('<rect x="20" y="96" width="160" height="56" rx="16" fill="#2563eb"/>'
               '<rect x="30" y="70" width="60" height="36" rx="14" fill="#e0e7ff"/>'
               '<rect x="84" y="84" width="96" height="24" rx="10" fill="#93c5fd"/>'
               '<rect x="26" y="150" width="14" height="22" rx="5" fill="#1e3a8a"/><rect x="160" y="150" width="14" height="22" rx="5" fill="#1e3a8a"/>')


ICONS = {
    "person": lambda a: ic_person(a or "blue"), "group": lambda a: ic_group(),
    "chart": lambda a: ic_chart(), "coins": lambda a: ic_coins(), "brush": lambda a: ic_brush(),
    "shirt": lambda a: ic_shirt(), "clock": lambda a: ic_clock(), "bed": lambda a: ic_bed(),
}
IKON_BIDANG = {"produksi": "brush", "marketing": "chart", "financial": "coins", "sdm": "group"}


def icon(name, arg=None):
    return ICONS.get(name, ICONS["group"])(arg)


# ---------------------------------------------------------------- slide
def judul(s, default_eyebrow, default_judul, default_aksen=""):
    eb = s.get("eyebrow", default_eyebrow)
    j = s.get("judul", default_judul)
    a = s.get("aksen", default_aksen)
    return (f'<div class="l"><p class="eyebrow">{e(eb)}</p>'
            f'<h2 class="title">{e(j)} <span class="accent">{e(a)}</span></h2></div>')


def chips_info(ev):
    return (f'<div class="row"><span class="pill white">{ic_calendar(ev.get("tanggal_hari", ""))}{e(ev["tanggal"])}</span>'
            f'<span class="pill white">{ic_building("")}{e(ev["tempat"])}</span></div>')


def s_cover(s, ev):
    nama = s.get("judul", ev["nama"]).split()
    a, b = " ".join(nama[:-1]) or nama[0], nama[-1] if len(nama) > 1 else ""
    return ("cover", f'<div class="top"><span>{e(ev["organisasi"]).upper()}</span><span class="yr">{e(ev.get("tahun", ""))}</span></div>'
            f'<h1 class="display">{e(a)}<br><span class="accent">{e(b)}</span></h1>{chips_info(ev)}'
            f'<div class="art">{ic_meeting()}</div>', False)


def s_penutup(s, ev):
    a, b = s.get("judul", "Terima"), s.get("aksen", "kasih")
    return ("cover", f'<h1 class="display">{e(a)}<br><span class="accent">{e(b)}</span></h1>{chips_info(ev)}'
            f'<div class="art">{ic_crowd()}</div>', "brand")


def s_venue(s, ev):
    words = ev["tempat"].split()
    a, b = " ".join(words[:-1]), words[-1]
    maps = s.get("maps_url") or ev.get("maps_url")
    btn = f'<div class="row"><a class="pill dark" href="{e(maps)}">Buka lokasi di Google Maps →</a></div>' if maps else ""
    facts = [
        (ic_calendar(ev.get("tanggal_hari", "")), "Hari, tanggal", s.get("tanggal_label", ev["tanggal"]), ev.get("jam")),
        (ic_shirt(), "Dress code", s.get("dress_code"), None),
        (ic_group(), "Ruangan", s.get("ruangan"), s.get("lantai")),
    ]
    fh = "".join(f'<div class="card fact">{ic}<div><p class="k">{e(k)}</p><p class="v">{e(v)}</p>'
                 + (f'<span class="pill blue">{e(p)}</span>' if p else "") + "</div></div>"
                 for ic, k, v, p in facts if v)
    return ("venue", f'<div class="l"><p class="eyebrow">{e(s.get("eyebrow", "Venue"))}</p>'
            f'<h2 class="venue-name">{e(a)} <span class="accent">{e(b)}</span></h2></div>{btn}'
            f'<div class="art">{ic_building(a or b)}</div><div class="facts">{fh}</div>', False)


def s_rundown(s, ev):
    rows = "".join(f'<tr class="{"hl" if r.get("highlight") else ""}"><td class="tm">{e(r["waktu"])}</td>'
                   f'<td>{e(r["acara"])}</td><td class="pic">{e(r.get("pic", "–"))}</td></tr>' for r in s["rows"])
    return ("", f'<div class="head">{judul(s, "Jadwal Hari-H", "Rundown", "Acara")}'
            f'<div class="row">{ic_clock().replace("<svg", "<svg width=72 height=72", 1)}'
            f'<div class="when"><p class="d">{e(ev["tanggal"])}</p><p class="t">{e(ev.get("jam", ""))}</p></div></div></div>'
            f'<table class="rd"><thead><tr><th>Waktu</th><th>Acara</th><th>PIC</th></tr></thead><tbody>{rows}</tbody></table>', False)


def s_bidang(s, ev):
    cards = []
    for i, b in enumerate(s["bidang"], 1):
        w = b.get("warna", b.get("id", "blue"))
        cards.append(f'<div class="card bcard {kelas(w)}">{icon(b.get("ikon", IKON_BIDANG.get(w, "group")))}<div class="b">'
                     f'<p class="eyebrow ct">Bidang {i:02d}</p><div class="t"><h3>{e(b["nama"])}</h3>'
                     + (f'<span class="pill dark">{e(b["lokasi"])}</span>' if b.get("lokasi") else "") +
                     f'</div><p class="d">{e(b.get("deskripsi", ""))}</p><div class="row">'
                     f'<span class="pill tint">PJ · {e(b.get("pj"))}</span><span class="pill white">Notulis · {e(b.get("notulis"))}</span>'
                     f'</div></div></div>')
    cols = "g2" if len(cards) in (2, 4) else "g3"
    sesi = f'<span class="pill dark">{e(s["sesi"])}</span>' if s.get("sesi") else ""
    return ("", f'<div class="head">{judul(s, "Diskusi Kelompok Terpumpun", "FGD:", "Diskusi per Bidang")}{sesi}</div>'
            f'<div class="grid {cols}">{"".join(cards)}</div>', False)


def s_peserta(s, ev):
    groups = s["kelompok"]
    total = s.get("total") or sum(len(g["anggota"]) for g in groups)
    cities = "".join(f'<span>{e(k)}<b>{e(v)}</b></span>' for k, v in s.get("asal", {}).items())
    cards = []
    for g in groups:
        w = g.get("warna", g.get("id", "blue"))
        items = []
        for i, nm in enumerate(g["anggota"], 1):
            role = ""
            cls = ""
            if nm == g.get("pj"):
                role, cls = '<span class="role cc">PJ</span>', "lead"
            elif nm == g.get("notulis"):
                role, cls = '<span class="role cc">NOTULIS</span>', "lead"
            no = f'<span class="no{" badge" if cls else ""}">{i}</span>'
            items.append(f'<li class="{cls}">{no}{e(nm)}{role}</li>')
        cards.append(f'<div class="card gcard {kelas(w)}"><div class="t"><span>{e(g["nama"])}</span><span class="c cc">{len(g["anggota"])}</span></div>'
                     f'<p class="sub">PJ {e(g.get("pj"))} · Notulis {e(g.get("notulis"))}</p><ul>{"".join(items)}</ul></div>')
    n = len(cards)
    return ("", f'<div class="head">{judul(s, "Peserta", "Peserta dan", "Kelompok FGD")}'
            f'<div class="stats"><div class="cities">{cities}</div><div class="statbox"><p class="n">{total}</p><p class="k">PESERTA</p></div></div></div>'
            f'<div class="grid" style="grid-template-columns:repeat({n},1fr);align-items:start">{"".join(cards)}</div>', False)


def s_petugas(s, ev):
    cols = ("blue", "violet", "green", "pink")
    cards = []
    for i, p in enumerate(s["petugas"]):
        w = p.get("warna", ("blue", "violet", "sdm", "produksi")[i % 4])
        ic = ic_group() if "," in p["nama"] or "&" in p["nama"] else ic_person(cols[i % 4])
        cards.append(f'<div class="card pcard {kelas(w)}">{ic}<p class="k ct">{e(p["peran"])}</p>'
                     f'<p class="v">{e(p["nama"])}</p><p class="d">{e(p.get("tugas", ""))}</p></div>')
    return ("", f'<div class="head">{judul(s, "Tim Hari-H", "Petugas", "Acara")}</div>'
            f'<div class="grid g{min(max(len(cards), 2), 4)}">{"".join(cards)}</div>', False)


def s_daftar(s, ev):
    cols = ("blue", "sdm", "marketing", "violet")
    cards = []
    for i, k in enumerate(s["kolom"]):
        w = k.get("warna", cols[i % 4])
        li = "".join(f'<li><span class="no tint">{j:02d}</span><span>{e(t)}</span></li>' for j, t in enumerate(k["poin"], 1))
        cards.append(f'<div class="card lcard {kelas(w)}"><h3>{e(k["judul"])}</h3><ol>{li}</ol></div>')
    return ("", f'<div class="head">{judul(s, "Informasi", "Judul", "Slide")}</div>'
            f'<div class="grid g{min(max(len(cards), 2), 4)}">{"".join(cards)}</div>', False)


def s_rooming(s, ev):
    cards = []
    for g in s["gelombang"]:
        rooms = g["kamar"]
        ncol = 2 if len(rooms) > 6 else 1
        chips = "".join(f'<span class="chip">{e(r)}</span>' for r in rooms)
        call = f'<p class="callout">{e(g["catatan"])}</p>' if g.get("catatan") else ""
        cards.append((ncol, f'<div class="card rcard"><div class="t"><h3>{e(g["tanggal"])}</h3><span class="pill blue">{e(g.get("info", ""))}</span></div>'
                      f'<div class="chips" style="grid-template-columns:repeat({ncol},1fr)">{chips}</div>{call}</div>'))
    tmpl = " ".join(f"{n}fr" for n, _ in cards)
    note = f'<span class="pill note">{e(s["pengumuman"])}</span>' if s.get("pengumuman") else ""
    return ("", f'<div class="head">{judul(s, "Check-in Hotel", "Rooming", "Hotel")}<div class="row">{note}'
            f'{ic_bed().replace("<svg", "<svg width=96 height=96", 1)}</div></div>'
            f'<div class="grid" style="grid-template-columns:{tmpl};align-items:start">{"".join(c for _, c in cards)}</div>', False)


# ---------------------------------------------------------------- notulensi
# catatan: [{"heading": "...", "poin": [...], "sub": [{"judul": "...", "poin": [...]}]}]
# Tinggi tiap blok diperkirakan (px, kanvas 1920x1080) lalu diisi ke kolom
# secara berurutan: 1 kolom lebar bila muat, 2 kolom bila tidak, lalu slide
# lanjutan. Dengan begitu teks tidak pernah terpotong.
KAP_KOLOM = 378                 # tinggi area isi Catatan (terukur 384px)
CHAR_1KOL, CHAR_2KOL = 115, 52  # perkiraan karakter per baris poin (24px Inter)
H_BARIS, H_HEAD, H_SUB = 35, 64, 50


def _baris(teks, lebar):
    return max(1, -(-len(str(teks)) // lebar))


def _blok(tp, lebar):
    """Pecah topik menjadi (tinggi_heading, [blok]) — blok = poin langsung atau satu sub-heading."""
    hh = H_HEAD + 38 * (_baris(tp.get("heading", ""), lebar - 4) - 1)
    out = []
    if tp.get("poin"):
        out.append({"sub": None, "poin": tp["poin"], "h": sum(H_BARIS * _baris(t, lebar) for t in tp["poin"])})
    for sb in tp.get("sub") or []:
        out.append({"sub": sb.get("judul", ""), "poin": sb.get("poin") or [],
                    "h": H_SUB + 32 * (_baris(sb.get("judul", ""), lebar) - 1)
                    + sum(H_BARIS * _baris(t, lebar) for t in sb.get("poin") or [])})
    return hh, out


def _isi_kolom(catatan, lebar):
    """Kembalikan list kolom; tiap kolom = list potongan topik."""
    kolom, cur, pakai = [], [], 0
    for tp in catatan:
        hh, bl = _blok(tp, lebar)
        potong = None
        for b in bl or [{"sub": None, "poin": [], "h": 0}]:
            perlu = b["h"] + (hh if potong is None else 0)
            if cur and pakai + perlu > KAP_KOLOM:
                kolom.append(cur); cur, pakai = [], 0
                lanj = potong is not None
                potong = None
                perlu = b["h"] + hh
            else:
                lanj = False
            if potong is None:
                potong = {"no": tp.get("no"), "heading": tp.get("heading", ""), "bl": [],
                          "lanjutan": lanj or any(x["heading"] == tp.get("heading") and x["no"] == tp.get("no")
                                                  for k in kolom for x in k)}
                cur.append(potong)
            potong["bl"].append(b)
            pakai += perlu
    if cur:
        kolom.append(cur)
    return kolom or [[]]


def bagi_catatan(catatan):
    """List halaman; tiap halaman = (jumlah_kolom, [kolom])."""
    satu = _isi_kolom(catatan, CHAR_1KOL)
    if len(satu) == 1:
        return [(1, satu)]
    dua = _isi_kolom(catatan, CHAR_2KOL)
    return [(2, dua[i:i + 2]) for i in range(0, len(dua), 2)]


def render_kolom(potongan):
    if not potongan:
        return '<div class="kol"><ul class="poin flat"><li class="kosong">…</li></ul></div>'
    html = []
    for tp in potongan:
        lanj = '<span class="lanj">(lanjutan)</span>' if tp["lanjutan"] else ""
        parts = [f'<div class="topik"><h3><span class="no badge">{e(tp["no"])}</span><span>{e(tp["heading"])}{lanj}</span></h3>']
        for b in tp["bl"]:
            li = "".join(f"<li>{e(t)}</li>" for t in b["poin"])
            if b["sub"] is None:
                parts.append(f'<ul class="poin flat">{li}</ul>')
            else:
                parts.append(f'<div class="sub"><h4>{e(b["sub"])}</h4><ul class="poin">{li}</ul></div>')
        parts.append("</div>")
        html.append("".join(parts))
    return '<div class="kol">' + "".join(html) + "</div>"


def s_notulensi(s, ev):
    w = s.get("warna", s.get("id", "blue"))
    cls = kelas(w)
    nomor = s.get("nomor", "01")
    meta = "".join(f'<div class="mcard"><p class="k">{k}</p><p class="v">{e(s.get(f))}</p></div>'
                   for k, f in (("Lokasi", "lokasi"), ("PJ", "pj"), ("Notulis", "notulis")))
    kolom = s.get("_kolom") or [[]]
    return (f"notul {cls}", f'<div class="head"><div class="l"><p class="eyebrow">FGD {e(nomor)} · Notulensi{" · Lanjutan" if s.get("_lanjutan") else ""}</p>'
            f'<h2 class="title">{e(s.get("judul", "Hasil FGD"))} <span class="accent">{e(s.get("nama", s.get("bidang", "…")))}</span></h2></div></div>'
            f'<div class="meta">{meta}</div>'
            f'<div class="notes"><p class="k">Catatan</p><div class="body" style="--cols:{s.get('_ncol', 1)}">'
            f'{"".join(render_kolom(k) for k in kolom)}</div></div>',
            "notul")


def expand(slides):
    """Pecah slide notulensi panjang menjadi beberapa halaman."""
    out = []
    for s in slides:
        if s.get("type") != "notulensi":
            out.append(s)
            continue
        cat = s.get("catatan") or []
        for i, tp in enumerate(cat, 1):
            tp.setdefault("no", f"{i:02d}")
        for j, (ncol, kolom) in enumerate(bagi_catatan(cat)):
            out.append(dict(s, _ncol=ncol, _kolom=kolom, _lanjutan=j > 0))
    return out


LAYOUT = {"cover": s_cover, "venue": s_venue, "rundown": s_rundown, "bidang": s_bidang, "peserta": s_peserta,
          "petugas": s_petugas, "daftar": s_daftar, "rooming": s_rooming, "penutup": s_penutup,
          "notulensi": s_notulensi}


def build(data):
    ev = data["acara"]
    ev.setdefault("organisasi", "CRS Ecosystem")
    slides = expand(data["slides"])
    total = len(slides)
    out = []
    for i, s in enumerate(slides, 1):
        if s["type"] not in LAYOUT:
            raise SystemExit(f"Tipe slide tidak dikenal: {s['type']} (pilihan: {', '.join(LAYOUT)})")
        cls, body, foot = LAYOUT[s["type"]](s, ev)
        if foot == "brand":
            f = f'<p class="foot brand">{e(ev["organisasi"]).upper()}</p>'
        elif foot == "notul":
            f = f'<p class="foot">Notulensi FGD · {e(ev["nama"])} {e(ev["organisasi"])}</p>'
        elif s["type"] == "cover":
            f = ""
        else:
            f = f'<p class="foot">{e(ev["nama"])} {e(ev["organisasi"])} · {e(ev["tanggal"])}</p>'
        out.append(f'<div class="frame"><section class="s {cls}" id="s{i:02d}">{body}{f}'
                   f'<p class="page"><span class="n">{i:02d}</span> / {total:02d}</p></section></div>')
    title = f'{ev["nama"]} {ev["organisasi"]}'
    return f"""<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..900&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body><main class="deck">{''.join(out)}</main>
<script>
function fit(){{var k=Math.min((innerWidth-48)/1920,1);document.documentElement.style.setProperty('--k',k);}}
addEventListener('resize',fit);fit();
</script></body></html>"""


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    Path(sys.argv[2]).write_text(build(data), encoding="utf-8")
    print(f"OK: {len(data['slides'])} slide -> {sys.argv[2]}")


if __name__ == "__main__":
    main()
