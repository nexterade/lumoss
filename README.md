# 🌿 LUMOSS — Media Garden, in bloom

<p align="center">
  <img src="https://img.shields.io/badge/LUMOSS-v7.2.12-2BEE34?style=for-the-badge&logo=leaflet&logoColor=white" alt="LUMOSS Version">
  <img src="https://img.shields.io/badge/Python-3.14%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Termux-Android-000000?style=for-the-badge&logo=termux&logoColor=white" alt="Termux">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT License">
</p>

<p align="center">
  <b>Upload media otomatis dari HP, tanpa drama, tanpa klik-klik sampai jempol keriting. 🌿</b>
</p>

<p align="center">
  <code>Python</code> • <code>Termux</code> • <code>Android</code> • <code>Multi Account</code> • <code>Media Automation</code> • <code>Luminous Moss UI</code>
</p>

---

## 🌿 LUMOSS itu apaan, sih?

**LUMOSS (Luminous Moss)** adalah project automation berbasis Python yang dirancang untuk mengelola dan mengunggah koleksi media dari Android melalui **Termux**.

> Dulu dikenal sebagai **AMUV7 (Automated Media Uploader v7)** — sekarang dibranding ulang jadi LUMOSS.

Bayangin begini:

> 📱 Kamu punya folder berisi foto/video.  
> 📂 LUMOSS ngecek isinya.  
> 🔍 LUMOSS menghitung statistiknya.  
> 🧠 LUMOSS tahu mana yang sudah dan belum diproses.  
> ☁️ Kamu tinggal pilih mau upload sekarang atau nanti.  
> 😎 Sisanya biarkan mesin yang kerja.

Project ini dikembangkan dengan pendekatan **CLI-first**, tetapi tampilannya sengaja dibuat lebih kece daripada terminal zaman dinosaurus.

Tema visual:

> 🌿 **Luminous Moss** — `#2BEE34` + dark terminal aesthetic.

Tagline:

> **Media Garden, in bloom.**

---

## 📌 FEATURE PINNED

> Bagian ini adalah fitur-fitur yang paling layak dipamerkan. Karena kalau nggak dipin, nanti dikira cuma script Python biasa. 😌

### 🟢 01 — Automated Media Upload

LUMOSS menangani proses upload media melalui engine uploader yang sudah tersedia di project.

Flow sederhananya:

```text
📂 Media Folder
      ↓
🔍 Scan Media
      ↓
📊 Hitung Statistik
      ↓
🧠 Cek Status Upload
      ↓
🚦 Upload Gate
      ↓
☁️ Upload
```

---

### 👥 02 — Multi Account + Multi Folder

LUMOSS memiliki struktur **multi-account** dengan dukungan **multi-folder media** per akun.

Struktur folder:

```text
lumoss/
├── accounts/
│   ├── active.json
│   ├── cantika/
│   │   └── config.json
│   └── akun_lain/
│       └── config.json
│
├── output/
│   ├── cantika/
│   │   ├── index.html
│   │   └── manager.html
│   └── akun_lain/
│
└── cache/
    ├── cantika/
    │   ├── uploads_cache.json
    │   └── deleted.json
    └── akun_lain/
```

Setiap akun punya:
- **Config sendiri** — `accounts/<slug>/config.json`
- **Output HTML sendiri** — `output/<slug>/`
- **Cache sendiri** — `cache/<slug>/`
- **Multi-folder media** — `media_dirs` array

---

### 📊 03 — Media Statistics

Menu **Cek Folder Media** menampilkan informasi:

```text
📊 STATISTIK MEDIA

Total file    › 26
Total size    › 18.6 MB
Subfolder     › 2
```

Jadi sebelum upload, kamu bisa tahu dulu:

> "Ini folder isinya berapa file sih?"

Daripada upload dulu baru sadar:

> "LAH KOK 3 GB?! 😭"

---

### 📤 04 — Upload Status Tracking

Media dibedakan menjadi:

```text
✓ Sudah diupload
◷ Belum diupload
```

Contoh:

```text
📤 STATUS UPLOAD

✓ Sudah  › 19 file (7.9 MB)
◷ Belum  › 7 file (10.8 MB)

Progress upload:
██████████████████████░░░░░░░░ 73%
```

Status menggunakan **cache key unik** `{source_label}/{rel_path}` untuk tracking.

Contoh key: `"Nagram/VID_20260718_154608_914.mp4"`

---

### 🧭 05 — Upload Gate

Salah satu UI terbaru LUMOSS.

Daripada langsung upload secara brutal, LUMOSS memberikan checkpoint:

```text
LUMOSS :: UPLOAD GATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

› Media detected
› Upload process ready

│ Mau diupload sekarang gak?

[Y]  Boleh
[N]  Jangan dulu ◄

│ INPUT :: [N]

› Pilihan [N]:
```

Default:

```text
N = Jangan dulu
```

Tekan `Y` / `y` / `ya` / `1` → upload dimulai.

Tekan `Enter` / `N` / `n` → kembali ke menu.

Input lain → kembali ke menu (safety).

---

### 🌈 06 — Cyber Moss Gradient

Pilihan Upload Gate memakai **ANSI True Color**:

```text
[Y]  Boleh
```
→ gradient 🟢 Neon Green → Luminous Moss

```text
[N]  Jangan dulu
```
→ gradient 🟡 Soft Gold → Amber

Arrow `◄` muncul di opsi default.

---

### 🧹 07 — Long Filename Cleanup

Nama file super panjang dipersingkat biar terminal gak jadi novel:

```text
_short_name(path, max_len=34)
_short_path(path, max_len=40)
```

Contoh:

```text
SaveVid.Net_AQOCb1o7y3aBl1WxCI7Q...mp4
```

Ekstensi tetap dipertahankan. **Nama file asli gak diubah** — cuma tampilannya.

---

### 📁 08 — Subfolder / Category Detection

Media di dalam subfolder tetap dihitung:

```text
📁 Kategori:

› Keluarga              (8 file)
› Wisata                (13 file)
```

Struktur folder tetap bisa dipakai untuk mengorganisir media tanpa ngacak-ngacak.

---

### 🎨 09 — Luminous Moss UI (v7.2.8)

Palet utama:

```text
Primary Moss   #2BEE34
Secondary Moss #37F650
Tertiary Moss  #50FF64
Dark Base      #141414
```

**Fitur UI v7.2.3 → v7.2.6:**

- ✅ **Banner LUMOSS** — border ngikutin lebar ASCII art (gak hardcoded)
- ✅ **`layout_widths()`** — full-width otomatis dari `term_width()`
- ✅ **`render_full_box()`** — 1 box full-width
- ✅ **`render_two_col_box()`** — 2 kolom 1 border utuh
- ✅ **`render_group_box()`** — grup menu border utuh
- ✅ **`render_merged_box()`** — 1 box, multiple section (horizontal)
- ✅ **`render_merged_group()`** — 1 box, multiple grup menu (horizontal)
- ✅ **`render_vertical_box()`** — section stack atas-bawah
- ✅ **`render_vertical_group()`** — grup menu stack atas-bawah
- ✅ **Emoji auto-convert** — `EMOJI_TO_UNICODE` mapping ~150 emoji → Unicode symbol
- ✅ **`convert_emoji()`** — auto-convert pas input (nama, judul)
- ✅ **`strip_emoji()`** — strip sisa emoji gak dikenal
- ✅ **🌿 (LUMOSS_SYMBOL)** — KEEP, gak di-convert (simbol utama LUMOSS)
- ✅ **Safety net** — double convert kalo user edit config manual

Hasil akhir:

> 🌿 terminal gelap + neon moss + sedikit cyber = nggak bikin mata langsung minta resign.

---

## 🖼️ GALLERY — 5 PR UTAMA

Salah satu milestone besar LUMOSS adalah penyempurnaan `templates/gallery.html`.

Lima PR utama yang sudah diselesaikan:

### ① 🎯 Video Centering

Video dibuat lebih terkontrol posisinya agar tampilan gallery tidak terasa miring atau random.

### ② 🌫️ Dynamic Backdrop Blur

Gallery menggunakan konsep backdrop blur dinamis untuk membuat media lebih menyatu dengan tampilan sekitarnya.

```text
Media utama
     ↓
Backdrop mengikuti media
     ↓
Visual terasa lebih immersive
```

### ③ 👆 Touch Gesture Swipe

Interaksi video mendukung gesture sentuh/swipe sehingga pengalaman penggunaan di perangkat mobile terasa lebih natural.

### ④ 🧩 Metadata Grid Redesign

Informasi metadata disusun ulang menjadi grid agar lebih rapi, mudah dipindai, dan tidak terlihat seperti dump teks.

### ⑤ 🌿 Moss Theme Synchronization

Tema gallery disinkronkan dengan identitas visual Luminous Moss.

```text
CLI
Manager
Gallery
   ↓
🌿 Luminous Moss
```

---

## ⚙️ ARSITEKTUR PROJECT

Struktur project v7.2.12:

```text
lumoss/
│
├── accounts/                    ← Config + active.json
│   ├── active.json
│   ├── akun_utama/
│   └── cantika/
│
├── output/                      ← Hasil generate
│   └── <slug>/
│       ├── index.html
│       └── manager.html
│
├── cache/                       ← Cache & state
│   └── <slug>/
│       ├── uploads_cache.json
│       └── deleted.json
│
├── templates/                   ← Template HTML
│   ├── gallery.html
│   └── manager.html
│
├── docs/                        ← Dokumentasi
│   ├── checkpoint.md            ← CONSTANT
│   ├── state.md                 ← DYNAMIC
│   └── backlog.md               ← DYNAMIC
│
├── backup/                      ← Backup
│
├── account_manager.py           ← v7.2.2
├── config_manager.py            ← v7.2.2
├── embed_parser.py              ← v7.2.11
├── global_config.json           ← v7.2.2
├── html_builder.py              ← v7.2.12
├── lumoss.py                    ← v7.2.12 (entry point)
├── media_processor.py           ← v7.2.0
├── menu.py                      ← v7.2.11
├── menu_account.py              ← v7.2.2
├── menu_embed.py                ← v7.2.2
├── menu_tools.py                ← v7.2.2
├── tools.py                     ← v7.2.11
├── ui_helpers.py                ← v7.2.11
├── uploader.py                  ← v7.2.9
├── README.md
└── requirements.txt
```

### 🔩 Komponen penting

| File | Peran |
|---|---|
| `lumoss.py` | Entry point CLI |
| `menu.py` | Menu utama dan workflow interaktif |
| `menu_account.py` | Menu manajemen akun |
| `menu_embed.py` | Menu embed system |
| `menu_tools.py` | Utility menu & terminal UI |
| `ui_helpers.py` | Warna, cursor, layout, emoji converter |
| `account_manager.py` | Manajemen multi-account |
| `config_manager.py` | Konfigurasi project |
| `media_processor.py` | Processing media (thumbnail, EXIF, dll) |
| `html_builder.py` | Generator HTML |
| `embed_parser.py` | Parser embed URL (YouTube, Instagram, dll) |
| `uploader.py` | Engine/proses upload |
| `tools.py` | Subprocess helper & statistik |
| `gallery.html` | Template gallery |
| `manager.html` | Template manager |

---

## 📱 DIBUAT UNTUK SIAPA?

### 📱 Android Power User

Yang ingin automation langsung dari HP menggunakan Termux.

### 🗂️ Kolektor Media

Yang punya banyak foto/video dan malas kerja manual satu per satu.

### 🧑‍💻 Python Tinkerer

Yang suka bongkar script:

```text
"Ini script sebenarnya ngapain?"
```

lalu:

```text
"Kayaknya bisa gue fork..."
```

lalu 3 jam kemudian:

```text
"Kenapa sekarang ada 17 file baru?" 💀
```

### ⚙️ Automation Enthusiast

Yang lebih suka:

```text
1 command
   ↓
mesin bekerja
```

daripada:

```text
klik → tunggu → klik → scroll → klik → ulangi
```

---

## 🧰 REQUIREMENTS

LUMOSS dikembangkan untuk environment:

```text
Android
└── Termux
    └── Python 3.14+
```

Direktori project:

```text
/storage/emulated/0/Project/lumoss/
```

> ⚠️ Requirement eksternal spesifik bergantung pada konfigurasi uploader & environment. Gunakan dependency yang disediakan project (lihat `requirements.txt`).

---

## 🚀 INSTALASI DI TERMUX

> Tutorial ini dibuat untuk orang yang baru kenal Termux. Santai. Kita nggak akan pura-pura semua orang lahir sambil pegang terminal. 😭

### 1️⃣ Install Termux

Pastikan Termux sudah terpasang di Android.

```bash
pkg update && pkg upgrade
```

### 2️⃣ Aktifkan akses storage

```bash
termux-setup-storage
```

Android akan meminta izin storage. Pilih **Allow / Izinkan**.

Storage dapat diakses melalui:

```text
/storage/emulated/0/
```

### 3️⃣ Pastikan Python tersedia

```bash
python --version
```

Target: **Python 3.14+**

Kalau belum:

```bash
pkg install python
```

### 4️⃣ Clone repo

```bash
cd /storage/emulated/0/Project/
git clone https://github.com/nexterade/lumoss.git
cd lumoss
```

### 5️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 6️⃣ Masuk ke project

```bash
cd /storage/emulated/0/Project/lumoss/
ls
```

Kamu seharusnya melihat:

```text
lumoss.py
menu.py
uploader.py
config_manager.py
...
```

---

## ▶️ CARA MENJALANKAN

Dari direktori project:

```bash
python lumoss.py
```

---

## 🧭 CARA MENGGUNAKAN — VERSI ORANG AWAM

### Step 1 — Jalankan LUMOSS

```bash
python lumoss.py
```

### Step 2 — Pilih akun

```text
Menu Utama
   ↓
Account
   ↓
Pilih akun aktif
```

### Step 3 — Masukkan media

Taruh foto/video ke folder media account. Setiap akun bisa punya **beberapa folder media** (multi-folder support).

### Step 4 — Cek Folder Media

Masuk:

```text
Menu Utama
   › Cek Folder Media
```

LUMOSS akan scanning:

```text
📊 STATISTIK MEDIA

Total file    › 26
Total size    › 18.6 MB
Subfolder     › 2
```

Status:

```text
📤 STATUS UPLOAD

✓ Sudah  › 19 file (7.9 MB)
◷ Belum  › 7 file (10.8 MB)
```

### Step 5 — Periksa file yang belum upload

Daftar ringkas:

```text
📋 Rincian file

• IMG_2571.jpg
• IMG_2604.jpg
• VID_20250819_0917.mp4
• tokio_blue_archive.jpg
• savevid_aQ0Cb1o7y3aBl1WxCI7Q...mp4
```

Nama panjang dipersingkat otomatis.

### Step 6 — Upload Gate

```text
│ Mau diupload sekarang gak?

[Y]  Boleh
[N]  Jangan dulu ◄
```

**Mau upload:** `Y` / `ya` / `1`

**Belum mau:** `Enter` / `N` → kembali ke menu.

---

## 🛡️ KENAPA DEFAULT-NYA N?

Karena automation itu keren.

Automation yang salah pencet:

> **tidak keren.** 💀

Default `N = Jangan dulu` berfungsi sebagai **safety gate** agar media tidak langsung di-upload hanya karena user masuk ke menu pengecekan.

---

## 🧪 DEBUGGING DASAR

Cek syntax:

```bash
python -m py_compile menu.py
```

Kalau gak ada output error:

```text
✅ Syntax aman
```

Kalau ada error:

```text
SyntaxError
```

Jangan panik. Python sedang bilang:

> "Bro, ada typo."

---

## 🔧 WORKFLOW PENGEMBANGAN YANG DISARANKAN

```text
1. Backup
   ↓
2. Ubah satu bagian
   ↓
3. py_compile
   ↓
4. Jalankan
   ↓
5. Test fitur
   ↓
6. Baru lanjut modifikasi berikutnya
```

Jangan:

```text
ubah 27 file
       ↓
run
       ↓
error
       ↓
"yang rusak yang mana ya?"
       ↓
💀
```

---

## 🧬 CONFIGURATION

Tema utama:

```text
Theme: moss
Version: 7.2.8
Primary: #2BEE34
Base: #141414
```

Default theme dikendalikan melalui `global_config.json`.

Jangan hard-code konfigurasi di banyak file kalau sudah tersedia via config manager.

---

## 🎨 DESIGN PHILOSOPHY

LUMOSS bukan cuma ingin:

> "yang penting jalan."

Tapi:

> **"jalan + enak dilihat + enak dipakai."**

```text
Dark Terminal
      +
Luminous Moss
      +
Minimal Border
      +
Useful Information
      +
Mobile Friendly
      =
🌿 LUMOSS UI
```

---

## 🗺️ ROADMAP

> Roadmap ini adalah arah pengembangan yang direncanakan, bukan janji.

### ✅ Phase 1 — Core (SELESAI)

- [x] Automated uploader foundation
- [x] CLI menu
- [x] Multi-account foundation
- [x] Media folder scanner
- [x] Upload status/cache detection
- [x] Upload progress
- [x] Media statistics

### ✅ Phase 2 — Rebranding (SELESAI)

- [x] Rebranding amuv7 → lumoss
- [x] Struktur baru: `accounts/` + `output/` + `cache/`
- [x] Multi-folder media support
- [x] Onboarding wajib pilih folder
- [x] Skip folder & file sampah
- [x] Cache key unik `{source_label}/{rel_path}`

### ✅ Phase 3 — UI Polish v7.2.3 → v7.2.6 (SELESAI)

- [x] Banner LUMOSS full-width
- [x] `layout_widths()` — auto dari term_width
- [x] `render_merged_box()` & `render_merged_group()`
- [x] `render_vertical_box()` & `render_vertical_group()`
- [x] Emoji auto-convert (~150 mapping)
- [x] `strip_emoji()` safety net
- [x] 🌿 LUMOSS_SYMBOL keep

### ✅ Phase 4 — Git Init (SELESAI v7.2.7)

- [x] Git init
- [x] `.gitignore` setup
- [x] Initial commit
- [x] Push ke GitHub
- [ ] (opsional) GitHub Actions

### 🔵 Phase 5 — FASE 5 PR (38 PR, PENDING)

Detail di `docs/backlog.md`. Highlight:

- [ ] PR-7 YouTube Error 153 (KRITIS)
- [ ] PR-8 Instagram embed header (KRITIS)
- [ ] PR-1 Layout Main Menu
- [ ] PR-2 Tag lightbox
- [ ] PR-4 `GITHUB_REPO` inject

### 🟣 Phase 6 — Backlog v7.3.0 (13 saran, PENDING)

---

## 📈 VERSION HISTORY

### `v7.2.12` — GITHUB_REPO + Tree View + Tools Fix
- FIX: PR-4 — GITHUB_REPO gak di-inject ke HTML (chain fix)
- NEW: Tree view layout (v7.2.11) — menu utama pake `render_tree_group()`
- NEW: Nested tree buat AKUN & RINGKASAN
- FIX: PR-3 — Emoji gear ⚙ nyempil (symbol konsisten)
- FIX: PR-5 — templates/about.html dihapus
- FIX: PR-6 — tools.py header (hapus emoji, ganti Unicode symbol)
- UPDATE: requirements.txt header → lumoss
- UPDATE: Versi state ke v7.2.12

### `v7.2.8` — Documentation Update
- Merge `PR-FASE5.md` → `backlog.md` (39 item)
- Update state: FASE 2 selesai, side project Cinematic Resume
- Checkpoint: tambah larangan keras aturan tag `#`
- Lowercase file names di `docs/`

### `v7.2.7` — Git Init
- Git init + push ke GitHub
- `.gitignore` setup
- README rebranding

### `v7.2.6` — Emoji Auto-Convert (UI Polish)
- `EMOJI_TO_UNICODE` mapping (~150 emoji → Unicode symbol)
- `convert_emoji()` + `strip_emoji()`
- 🌿 LUMOSS_SYMBOL (keep)

### `v7.2.5` — Vertical Layout
- `render_vertical_box()`
- `render_vertical_group()`
- Sub-judul "AKUN & RINGKASAN" / "MENU UTAMA"

### `v7.2.4` — Merged Boxes
- `render_merged_box()`
- `render_merged_group()`

### `v7.2.3` — UI Overhaul
- Banner LUMOSS auto-width
- `layout_widths()` full-width
- Helper layout baru
- Emoji → Unicode symbol di submenu

### `v7.2.2` — Struktur Baru
- Struktur folder terpisah: `accounts/` + `output/` + `cache/`
- Multi-folder media support
- Onboarding wajib pilih folder
- Skip folder & file sampah (`.thumbnails`, `.cache`, Android, dll)
- Cache key unik: `{source_label}/{rel_path}`

### `v7.1.2` — Upload Gate Dashboard (AMUV7)
- Cyber Moss Upload Gate
- Media statistics + status dashboard
- Upload progress visualization
- Compact file listing
- Long filename shortening
- Subfolder/category compact display
- Gradient Y/N options

### `v7.1.x` & sebelumnya (AMUV7)
- Gallery & Media UX improvements
- Video centering, backdrop blur, touch swipe
- Metadata grid redesign
- Gallery theme synchronization

---

## 🧯 TROUBLESHOOTING

### ❌ "Python command tidak ditemukan"

```bash
pkg install python
python --version
```

### ❌ Storage tidak bisa diakses

```bash
termux-setup-storage
```

Berikan permission Android.

### ❌ Script error setelah diedit

```bash
python -m py_compile menu.py
```

Baca baris error yang ditunjukkan Python.

### ❌ Upload tidak dimulai

Pastikan:
1. Ada media yang belum diupload
2. Akun aktif sudah dipilih
3. Konfigurasi akun benar
4. Callback/engine uploader tersedia
5. Kamu memilih `Y` / `ya` / `1`

### ❌ Nama file terlalu panjang

LUMOSS sudah punya mekanisme pemendekan nama. Nama file asli **tidak diubah**.

### ❌ Git push ditolak

Pastikan:
1. `gh auth status` → logged in
2. Remote udah di-set: `git remote -v`
3. Branch udah di-track: `git push -u origin main`

---

## 🤝 CONTRIBUTING

Pull request, issue, ide UI, eksperimen sangat welcome.

```text
Fork
  ↓
Branch
  ↓
Modify
  ↓
Test
  ↓
Commit
  ↓
Pull Request
```

Sebelum kirim perubahan Python:

```bash
python -m py_compile <file>.py
```

Dan sebisa mungkin:

> jangan mengubah engine upload hanya demi mempercantik warna tombol. 😭

---

## 🧪 DEVELOPMENT NOTES

LUMOSS masih aktif dikembangkan.

Tiga file dokumentasi inti (lihat `docs/`):

| File | Tipe | Fungsi |
|------|------|--------|
| `checkpoint.md` | CONSTANT | Peran, kepribadian, aturan |
| `state.md` | DYNAMIC | Progress, struktur, status fase |
| `backlog.md` | DYNAMIC | Detail PR/issues |

Biasakan update `state.md` tiap milestone besar.

---

## ❤️ DIBUAT DENGAN

```text
☕ kopi
🧠 rasa penasaran
📱 Android
🐍 Python
💻 Termux
🌿 Luminous Moss
💀 debugging
```

Dan tentu saja:

> beberapa keputusan desain yang awalnya cuma "coba-coba dulu"  
> lalu berubah menjadi fitur. 😂

---

## 🙏 TERIMA KASIH KEPADA

LUMOSS dibangun dengan memanfaatkan ekosistem open-source dan inspirasi dari berbagai tools, library, dokumentasi, komunitas, serta para developer yang membagikan pengetahuan mereka.

Terima kasih khusus kepada:

- 🐍 **Python community**
- 📱 **Termux community**
- 🌐 **Open-source community**
- 👨‍💻 Para developer yang membuat tools automation dan CLI
- 🎨 Para developer yang membangun UI/UX mobile dan terminal yang menjadi inspirasi
- 🧪 Semua orang yang membantu menemukan bug, memberi ide, atau sekadar bilang:
  > "Bro, ini bisa dibuat lebih bagus nggak?"

Jawabannya:

> **Bisa. Makanya project ini belum selesai. 😎**

---

## 👤 AUTHOR

<p align="center">
  <img src="https://github.com/nexterade.png?size=180" width="120" height="120" style="border-radius:50%" alt="Author Profile">
</p>

<h3 align="center">🌿 nexterade</h3>

<p align="center">
  <i>Builder • Tinkerer • Automation Enjoyer • Professional "coba dulu" specialist</i>
</p>

### 🧑‍💻 Bio

> Seorang manusia yang percaya bahwa kalau sebuah pekerjaan bisa dibuat otomatis,  
> kenapa harus dilakukan manual berkali-kali?
>
> Suka ngoprek Python, terminal, Android, automation, UI, dan project yang awalnya kecil...
> kemudian entah kenapa berubah menjadi project besar. 💀

### 🔗 Contact & Social

| Channel | Link |
|---|---|
| 🐙 GitHub | https://github.com/nexterade |
| 💬 Telegram | https://t.me/nexterade |
| 📧 Email | nexterade@gmail.com |
| 🌐 Website | https://nexterade.github.io |
| 🐙 Repo | https://github.com/nexterade/lumoss |

### 💚 Support Development

Kalau LUMOSS membantu pekerjaanmu dan ingin mendukung pengembangannya:

```text
⭐ Star repository
🐛 Report bug
💡 Kirim ide
🔧 Submit PR
📢 Share
```

> Bahkan satu ⭐ GitHub kadang cukup untuk membuat developer kembali membuka laptop setelah bilang:
>
> **"Udah, besok aja lanjut."** 😂

---

## 📜 LICENSE

LUMOSS menggunakan **MIT License**.

```text
MIT License

Copyright (c) 2026 nexterade

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## ⭐ SUPPORT THE PROJECT

Kalau project ini berguna:

```text
⭐ Star
🍴 Fork
🐛 Report bugs
💡 Suggest features
🔧 Submit PR
📢 Share
```

Yang paling simpel:

> **Kasih ⭐. Gratis. Tidak mengurangi kuota nasi.** 🍚😂

---

## 🧭 FINAL WORD

LUMOSS bukan project yang lahir langsung sempurna.

Ia berkembang lewat:

```text
ide
 ↓
implementasi
 ↓
bug
 ↓
debug
 ↓
"lah kok rusak?"
 ↓
fix
 ↓
UI baru
 ↓
optimasi
 ↓
bug baru
 ↓
fix lagi
 ↓
✨ lebih bagus
```

Dan begitulah kehidupan developer.

**LUMOSS — Media Garden, in bloom. 🌿⚡**

<p align="center">
  <b>Made with 🧠 + 🐍 + 📱 + ☕ + sedikit chaos.</b>
</p>
