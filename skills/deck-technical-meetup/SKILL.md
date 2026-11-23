---
name: deck-technical-meetup
description: Membuat deck 16:9 bergaya CRS Ecosystem, baik deck informasi acara (cover, venue, rundown, FGD, peserta, petugas, syarat, rooming, penutup) maupun slide notulensi FGD berformat Heading, Sub-heading, Poin dengan cek diksi negatif. Gunakan untuk "deck Technical Meetup", "informasi umum acara", "notulensi FGD", atau "rapikan notulen".
---

# Deck Informasi Acara (CRS Ecosystem)

Membuat deck 16:9 (1920×1080) dengan gaya visual deck "Technical Meetup CRS Ecosystem": latar abu kebiruan muda, kartu putih membulat, judul tebal Inter dengan bagian akhir berwarna biru, eyebrow kapital berjarak lebar, ilustrasi 3D lembut, dan footer `Nama Acara · Tanggal` + nomor `01 / 09`.

## Isi skill

- `scripts/build_deck.py` — mengubah `data.json` menjadi satu file HTML mandiri (hanya pustaka standar Python).
- `scripts/cek_diksi.py` — menandai diksi berkonotasi negatif di catatan notulensi beserta opsi penggantinya (tidak mengubah file).
- `references/diksi.json` — daftar diksi negatif → opsi yang lebih positif.
- `references/schema.md` — struktur data dan 9 tipe slide. **Baca dulu sebelum menyusun data.**
- `references/deck.css` — gaya bersama (disisipkan otomatis oleh skrip).
- `references/tokens.json` — token sistem desain CRS Ecosystem (warna, tipografi, spasi, radius).
- `examples/technical-meetup-nov-2026.json` — contoh lengkap 9 slide.

## Langkah

1. Kumpulkan info acara dari pengguna: nama acara, tanggal, jam, tempat, dan slide apa saja yang dibutuhkan. Tanyakan hanya yang belum jelas; data yang tidak ada tulis "…" agar mudah diisi nanti.
2. Salin `examples/technical-meetup-nov-2026.json` sebagai titik awal, lalu ganti isinya sesuai acara baru. Hapus slide yang tidak relevan, ubah urutan bila perlu.
3. Jalankan:
   ```bash
   python3 scripts/build_deck.py data.json deck.html
   ```
4. Buka/render hasilnya dan periksa setiap slide: teks tidak terpotong, tabel rundown dan kolom peserta tidak meluber. Jika terlalu padat, pecah menjadi dua slide dengan tipe yang sama.
5. Serahkan deck: publikasikan sebagai artifact (HTML) bila tersedia, atau kirim file HTML. Untuk PDF, buka di Chrome → Print → Save as PDF (ukuran mengikuti 1920×1080, margin None, background graphics aktif).
6. Jika sesi menawarkan tipe Slides dan pengguna ingin bisa mengedit langsung, susun dek dengan tipe Slides memakai `references/tokens.json` dan pola tata letak yang sama.

## Notulensi FGD (tipe `notulensi`)

Satu slide per bidang FGD: eyebrow `FGD 01 · NOTULENSI`, judul `Hasil FGD <Bidang>` dengan nama bidang berwarna biru (sama seperti deck informasi), tiga kartu (Lokasi · PJ · Notulis), lalu kotak **Catatan**. Contoh lengkap: `examples/notulensi-fgd.json`.

### Format isi Catatan: Heading → Sub-heading → Poin

Susun catatan mentah dari pengguna menjadi struktur ini, supaya rapi dan mudah dipahami:

```json
"catatan": [
  { "heading": "Laporan Keuangan Studio",
    "sub": [
      { "judul": "Kondisi saat ini", "poin": ["…", "…"] },
      { "judul": "Kesepakatan",      "poin": ["…", "…"] }
    ] },
  { "heading": "Kelas Marketing", "poin": ["…", "…"] }
]
```

- **Heading** = topik besar yang dibahas (2–5 kata, tanpa titik). Diberi nomor otomatis 01, 02, … dalam badge berwarna bidang.
- Warna: eyebrow, aksen judul, label CATATAN, sub-heading dan titik poin memakai biru utama; warna bidang hanya untuk badge nomor heading.
- **Sub-heading** (`sub[].judul`) = aspek dari topik. Pola yang dianjurkan: *Kondisi saat ini*, *Usulan*, *Kesepakatan*, *Tindak lanjut*, *PIC & tenggat*. Boleh dilewati bila topiknya sederhana (pakai `poin` langsung di bawah heading).
- **Poin** = satu gagasan per poin, kalimat pendek tanpa titik di akhir, maksimal ±15 kata. Mulai dengan kata kerja atau subjek yang jelas.
- Jangan mengarang isi. Rapikan bahasa dan kelompokkan saja; jika ada bagian yang tidak jelas, tanyakan ke pengguna.
- Catatan kosong (`[]`) tampil sebagai satu poin "…" untuk diisi manual.
- Isi panjang otomatis dibagi ke 2 kolom, lalu ke slide lanjutan (`FGD 03 · NOTULENSI · LANJUTAN`) tanpa terpotong.

### Wajib: cek diksi berkonotasi negatif sebelum membuat deck

1. Setelah catatan tersusun, jalankan:
   ```bash
   python3 scripts/cek_diksi.py data.json
   ```
   Lalu baca juga seluruh catatan sendiri: nada negatif bisa muncul tanpa kata yang ada di daftar (mis. menyalahkan orang tertentu, sindiran, kalimat yang menghakimi).
2. **Jangan mengganti diksi secara diam-diam.** Tampilkan setiap temuan ke pengguna dalam format:
   > **[1] Financial › Laporan Keuangan › Kondisi saat ini**
   > "Laporan beberapa studio sering *telat* masuk"
   > Opsi: (a) melewati jadwal · (b) belum tepat waktu · (c) perlu penyesuaian jadwal · (d) biarkan apa adanya
   Berikan 2–3 opsi yang lebih positif tetapi tetap jujur dan tidak mengubah fakta, plus opsi untuk membiarkan. Bila AskUserQuestion tersedia, pakai pilihan ganda per temuan (maks 4 per pertanyaan).
3. Terapkan pilihan pengguna, lalu baru jalankan `build_deck.py`. Jika pengguna memilih membiarkan, jangan tanyakan kata yang sama lagi di sesi itu.
4. Daftar kata dan opsinya ada di `references/diksi.json`; tambahkan entri baru bila pengguna menyebut diksi lain yang ingin dihindari.

## Aturan gaya

- Judul slide: 2–5 kata, bagian akhir (`aksen`) berwarna biru — mis. "Rundown **Acara**", "Peserta dan **Kelompok FGD**".
- Eyebrow: label pendek kapital yang menjelaskan konteks (JADWAL HARI-H, VENUE, TIM HARI-H, CHECK-IN HOTEL, PENUTUP).
- Bahasa Indonesia ringkas, santai-profesional. Pakai "·" sebagai pemisah info (`PJ · Rio`, `Resto Lt. 3 · Indoor`) dan en dash untuk rentang waktu (`08.30 – 09.00`).
- Selalu tulis "Financial", bukan "Keuangan"; nama bidang default: Produksi, Marketing, Financial, SDM dengan warna pink, oranye, kuning tua, hijau.
- Satu gagasan per slide; maksimal ±11 baris rundown, ±10 nama per kolom peserta, ±4 poin per kolom daftar.
- Jangan menambahkan logo, foto orang, atau aset pihak lain. Ilustrasi memakai ikon SVG bawaan skrip.
