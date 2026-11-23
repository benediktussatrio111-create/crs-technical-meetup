# Struktur data deck (`data.json`)

Satu file JSON berisi `acara` (info umum) dan `slides` (urutan slide). Nomor halaman `01 / 09` dan footer dibuat otomatis.

## `acara`

| Kunci | Wajib | Contoh |
|---|---|---|
| `nama` | ya | `"Technical Meetup"` — kata terakhir otomatis berwarna biru di cover |
| `organisasi` | tidak | `"CRS Ecosystem"` (default) |
| `tahun` | tidak | `"2026"` — pojok kanan atas cover |
| `tanggal` | ya | `"Selasa, 24 November 2026"` |
| `tanggal_hari` | tidak | `"24"` — angka di ikon kalender |
| `jam` | tidak | `"08.30 – 17.00 WIB"` |
| `tempat` | ya | `"Aruss Hotel"` — kata terakhir berwarna biru di slide venue |
| `maps_url` | tidak | tautan Google Maps untuk tombol di slide venue |

## Judul slide

Hampir semua slide memakai pola **eyebrow** (label kapital biru) + **judul** + **aksen** (bagian akhir judul berwarna biru). Ketiganya punya nilai default dan bisa ditimpa:

```json
{ "type": "rundown", "eyebrow": "Jadwal Hari-H", "judul": "Rundown", "aksen": "Acara", ... }
```

## Tipe slide

| `type` | Isi | Kunci khusus |
|---|---|---|
| `cover` | Judul besar 2 baris + chip tanggal & tempat + ilustrasi meja diskusi | `judul` (opsional, default `acara.nama`) |
| `venue` | Nama tempat besar, tombol Maps, 3 kartu fakta | `tanggal_label`, `dress_code`, `ruangan`, `lantai` (kartu tanpa isi otomatis disembunyikan) |
| `rundown` | Tabel Waktu · Acara · PIC | `rows`: `[{waktu, acara, pic, highlight}]` — `highlight: true` untuk sesi utama (maks ±11 baris) |
| `bidang` | Kartu per bidang FGD (2–4 kartu) | `sesi` (pill gelap kanan atas), `bidang`: `[{id, nama, lokasi, deskripsi, pj, notulis, warna?, ikon?}]` |
| `peserta` | Kolom anggota per kelompok + rekap kota | `asal`: `{kota: jumlah}`, `total` (opsional, default jumlah anggota), `kelompok`: `[{id, nama, pj, notulis, anggota: []}]` — maks ±10 nama per kolom |
| `petugas` | Kartu peran (2–4) | `petugas`: `[{peran, nama, tugas, warna?}]` |
| `daftar` | Kolom berjudul dengan poin bernomor 01, 02, … (syarat, aturan, checklist) | `kolom`: `[{judul, poin: [], warna?}]` (2–4 kolom, maks ±4 poin) |
| `rooming` | Pembagian kamar per gelombang | `pengumuman` (pill kuning), `gelombang`: `[{tanggal, info, kamar: [], catatan?}]` |
| `penutup` | "Terima kasih" besar + chip + ilustrasi kerumunan | `judul`, `aksen` |

Tipe boleh dipakai lebih dari sekali, dalam urutan apa pun, dan boleh dihilangkan.

## Warna

`warna` menerima: `produksi` (pink), `marketing` (oranye), `financial` (kuning tua), `sdm` (hijau), `blue`, `violet`.
Pada `bidang` dan `peserta`, `id` bidang otomatis dipakai sebagai warna bila `warna` tidak diisi.

## Ikon (`ikon` pada bidang)

`brush`, `chart`, `coins`, `group`, `person`, `shirt`, `clock`, `bed`. Default per bidang: produksi → brush, marketing → chart, financial → coins, sdm → group.
