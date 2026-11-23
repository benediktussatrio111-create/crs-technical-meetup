---
name: deck-technical-meetup
description: Membuat deck informasi acara 16:9 bergaya CRS Ecosystem (cover, venue, rundown, FGD per bidang, peserta, petugas, syarat/daftar, rooming hotel, penutup). Gunakan saat pengguna meminta "deck Technical Meetup", "slide informasi umum acara", "branding kit informasi umum", atau materi info acara CRS Ecosystem.
---

# Deck Informasi Acara (CRS Ecosystem)

Membuat deck 16:9 (1920×1080) dengan gaya visual deck "Technical Meetup CRS Ecosystem": latar abu kebiruan muda, kartu putih membulat, judul tebal Inter dengan bagian akhir berwarna biru, eyebrow kapital berjarak lebar, ilustrasi 3D lembut, dan footer `Nama Acara · Tanggal` + nomor `01 / 09`.

## Isi skill

- `scripts/build_deck.py` — mengubah `data.json` menjadi satu file HTML mandiri (hanya pustaka standar Python).
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

## Aturan gaya

- Judul slide: 2–5 kata, bagian akhir (`aksen`) berwarna biru — mis. "Rundown **Acara**", "Peserta dan **Kelompok FGD**".
- Eyebrow: label pendek kapital yang menjelaskan konteks (JADWAL HARI-H, VENUE, TIM HARI-H, CHECK-IN HOTEL, PENUTUP).
- Bahasa Indonesia ringkas, santai-profesional. Pakai "·" sebagai pemisah info (`PJ · Rio`, `Resto Lt. 3 · Indoor`) dan en dash untuk rentang waktu (`08.30 – 09.00`).
- Selalu tulis "Financial", bukan "Keuangan"; nama bidang default: Produksi, Marketing, Financial, SDM dengan warna pink, oranye, kuning tua, hijau.
- Satu gagasan per slide; maksimal ±11 baris rundown, ±10 nama per kolom peserta, ±4 poin per kolom daftar.
- Jangan menambahkan logo, foto orang, atau aset pihak lain. Ilustrasi memakai ikon SVG bawaan skrip.
