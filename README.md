# 🚀 AMUV7 — Automated Media Uploader v7

<p align="center">
  <img src="https://img.shields.io/badge/AMUV7-v7.1.2-2BEE34?style=for-the-badge&logo=android&logoColor=white" alt="AMUV7 Version">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Termux-Android-000000?style=for-the-badge&logo=termux&logoColor=white" alt="Termux">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT License">
</p>

<p align="center">
  <b>Upload media otomatis dari HP, tanpa drama, tanpa klik-klik sampai jempol keriting. 🗿</b>
</p>

<p align="center">
  <code>Python</code> • <code>Termux</code> • <code>Android</code> • <code>Multi Account</code> • <code>Media Automation</code> • <code>Luminous Moss UI</code>
</p>

---

## 🧠 AMUV7 itu apaan, sih?

**AMUV7 (Automated Media Uploader v7)** adalah project automation berbasis Python yang dirancang untuk mengelola dan mengunggah koleksi media dari Android melalui **Termux**.

Bayangin begini:

> 📱 Kamu punya folder berisi foto/video.  
> 📂 AMUV7 ngecek isinya.  
> 🔍 AMUV7 menghitung statistiknya.  
> 🧠 AMUV7 tahu mana yang sudah dan belum diproses.  
> ☁️ Kamu tinggal pilih mau upload sekarang atau nanti.  
> 😎 Sisanya biarkan mesin yang kerja.

Project ini dikembangkan dengan pendekatan **CLI-first**, tetapi tampilannya sengaja dibuat lebih kece daripada terminal zaman dinosaurus.

Tema visual saat ini adalah:

> 🌿 **Luminous Moss** — `#2BEE34` + dark terminal aesthetic.

---

# 📌 FEATURE PINNED

> Bagian ini adalah fitur-fitur yang paling layak dipamerkan. Karena kalau nggak dipin, nanti dikira cuma script Python biasa. 😌

### 🟢 01 — Automated Media Upload

AMUV7 menangani proses upload media melalui engine uploader yang sudah tersedia di project.

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

### 👥 02 — Multi Account

AMUV7 memiliki struktur **multi-account**.

Contoh struktur media:

```text
accounts/
├── cantika/
│   └── media/
│       ├── foto.jpg
│       └── video.mp4
│
├── akun_lain/
│   └── media/
│       └── ...
│
└── ...
```

Setiap account dapat memiliki folder media dan konfigurasi masing-masing.

---

### 📊 03 — Media Statistics

Menu **Cek Folder Media** dapat menampilkan informasi seperti:

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

Status ini menggunakan cache yang tersedia pada account untuk menentukan apakah media sudah memiliki URL/status upload.

---

### 🧭 05 — Upload Gate

Ini salah satu UI terbaru AMUV7.

Daripada langsung upload secara brutal, AMUV7 memberikan checkpoint:

```text
AMUV7 :: UPLOAD GATE
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

Tekan:

- `Y`
- `y`
- `ya`
- `1`

→ upload dimulai.

Tekan:

- `Enter`
- `N`
- `n`

→ kembali ke menu.

Input lainnya juga kembali ke menu agar tidak terjadi eksekusi upload secara tidak sengaja.

---

### 🌈 06 — Cyber Moss Gradient

Pilihan Upload Gate memakai ANSI True Color.

```text
[Y]  Boleh
```

menggunakan gradient:

> 🟢 Neon Green → Luminous Moss

Sedangkan:

```text
[N]  Jangan dulu
```

menggunakan:

> 🟡 Soft Gold → Amber

Arrow:

```text
◄
```

hanya muncul pada opsi yang sedang menjadi **default configuration**.

---

### 🧹 07 — Long Filename Cleanup

Nama file super panjang bisa bikin terminal berubah menjadi:

```text
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.mp4
```

Alias:

> "Terminal saya kenapa jadi novel?"

AMUV7 sekarang memiliki mekanisme pemendekan nama:

```text
_short_name(path, max_len=34)
_short_path(path, max_len=40)
```

Contoh:

```text
SaveVid.Net_AQOCb1o7y3aBl1WxCI7Q...mp4
```

Ekstensi tetap dipertahankan.

Daftar file yang ditampilkan juga dibatasi agar layar Android tidak menjadi scroll hell.

---

### 📁 08 — Subfolder / Category Detection

Media di dalam subfolder tetap dihitung.

Contoh:

```text
📁 Kategori:

› Keluarga              (8 file)
› Wisata                (13 file)
```

Struktur folder tetap bisa dipakai untuk mengorganisir media tanpa harus mengacak-acak semuanya ke satu folder.

---

### 🎨 09 — Luminous Moss UI

Palet utama:

```text
Primary Moss   #2BEE34
Dark Base      #141414
```

Tema ini diterapkan pada beberapa bagian project, termasuk:

- Gallery
- Manager
- About
- Menu utilities
- CLI helpers
- Upload progress
- Upload Gate

Hasil akhirnya:

> 🌿 terminal gelap + neon moss + sedikit cyber = nggak bikin mata langsung minta resign.

---

# 🖼️ GALLERY — 5 PR UTAMA

Salah satu milestone besar AMUV7 adalah penyempurnaan `templates/gallery.html`.

Lima PR utama yang sudah diselesaikan:

### ① 🎯 Video Centering

Video dibuat lebih terkontrol posisinya agar tampilan gallery tidak terasa miring atau random.

---

### ② 🌫️ Dynamic Backdrop Blur

Gallery menggunakan konsep backdrop blur dinamis untuk membuat media lebih menyatu dengan tampilan sekitarnya.

Tujuannya:

```text
Media utama
     ↓
Backdrop mengikuti media
     ↓
Visual terasa lebih immersive
```

---

### ③ 👆 Touch Gesture Swipe

Interaksi video mendukung gesture sentuh/swipe sehingga pengalaman penggunaan di perangkat mobile terasa lebih natural.

---

### ④ 🧩 Metadata Grid Redesign

Informasi metadata disusun ulang menjadi grid agar lebih rapi, mudah dipindai, dan tidak terlihat seperti dump teks.

---

### ⑤ 🌿 Moss Theme Synchronization

Tema gallery disinkronkan dengan identitas visual Luminous Moss.

Jadi:

```text
CLI
Manager
About
Gallery
   ↓
🌿 Luminous Moss
```

Bukan lagi masing-masing punya kepribadian sendiri. 😂

---

# ⚙️ ARSITEKTUR PROJECT

Struktur penting project saat ini:

```text
amuv7/
│
├── amuv7.py
├── menu.py
├── menu_tools.py
├── ui_helpers.py
├── account_manager.py
├── config_manager.py
├── html_builder.py
├── uploader.py
├── tools.py
│
└── templates/
    ├── gallery.html
    ├── manager.html
    └── about.html
```

### 🔩 Komponen penting

| File | Peran |
|---|---|
| `amuv7.py` | Entry point CLI |
| `menu.py` | Menu utama dan workflow interaktif |
| `menu_tools.py` | Utility menu & terminal UI |
| `ui_helpers.py` | Warna, cursor, dan helper visual |
| `account_manager.py` | Manajemen multi-account |
| `config_manager.py` | Konfigurasi project |
| `html_builder.py` | Generator HTML |
| `uploader.py` | Engine/proses upload |
| `tools.py` | Subprocess helper & statistik |
| `gallery.html` | Template gallery |
| `manager.html` | Template manager |
| `about.html` | Halaman informasi/about |

---

# 📱 DIBUAT UNTUK SIAPA?

AMUV7 dibuat terutama untuk:

### 📱 Android Power User

Orang yang ingin melakukan automation langsung dari HP menggunakan Termux.

### 🗂️ Kolektor Media

Yang punya banyak foto/video dan malas melakukan pekerjaan manual satu per satu.

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

# 🧰 REQUIREMENTS

AMUV7 dikembangkan untuk environment:

```text
Android
└── Termux
    └── Python 3.11+
```

Direktori project yang digunakan:

```text
/storage/emulated/0/Project/amuv7/
```

> ⚠️ Requirement eksternal yang lebih spesifik bergantung pada konfigurasi uploader dan environment project yang digunakan. Jangan mengasumsikan dependency tambahan hanya dari README ini; gunakan konfigurasi/dependency yang memang disediakan project.

---

# 🚀 INSTALASI DI TERMUX

> Tutorial ini dibuat untuk orang yang baru kenal Termux. Santai. Kita nggak akan pura-pura semua orang lahir sambil pegang terminal. 😭

## 1️⃣ Install Termux

Pastikan Termux sudah terpasang di Android.

Kemudian buka:

```bash
pkg update && pkg upgrade
```

---

## 2️⃣ Aktifkan akses storage

Jalankan:

```bash
termux-setup-storage
```

Android akan meminta izin storage.

Pilih:

> **Allow / Izinkan**

Setelah berhasil, biasanya storage dapat diakses melalui:

```text
/storage/emulated/0/
```

---

## 3️⃣ Pastikan Python tersedia

Cek:

```bash
python --version
```

Target environment AMUV7:

```text
Python 3.11+
```

Kalau Python belum tersedia:

```bash
pkg install python
```

---

## 4️⃣ Masuk ke project

```bash
cd /storage/emulated/0/Project/amuv7/
```

Cek isi folder:

```bash
ls
```

Kamu seharusnya melihat file-file project seperti:

```text
amuv7.py
menu.py
uploader.py
config_manager.py
...
```

---

# ▶️ CARA MENJALANKAN

Dari direktori project:

```bash
python amuv7.py
```

Jika project menggunakan executable/script wrapper yang tersedia di environment kamu, ikuti entry point yang disediakan project.

---

# 🧭 CARA MENGGUNAKAN — VERSI ORANG AWAM

## Step 1 — Jalankan AMUV7

```bash
python amuv7.py
```

---

## Step 2 — Pilih akun

Gunakan menu account yang tersedia.

Konsepnya:

```text
Menu Utama
   ↓
Account
   ↓
Pilih akun aktif
```

---

## Step 3 — Masukkan media

Taruh foto/video ke folder media account.

Contoh:

```text
accounts/
└── cantika/
    └── media/
        ├── foto1.jpg
        ├── foto2.png
        ├── video1.mp4
        │
        ├── Keluarga/
        │   ├── foto3.jpg
        │   └── foto4.jpg
        │
        └── Wisata/
            └── liburan.mp4
```

---

## Step 4 — Cek Folder Media

Masuk:

```text
Menu Utama
   › Cek Folder Media
```

AMUV7 akan melakukan scanning.

Kamu akan mendapatkan gambaran seperti:

```text
📊 STATISTIK MEDIA

Total file    › 26
Total size    › 18.6 MB
Subfolder     › 2
```

Kemudian status:

```text
📤 STATUS UPLOAD

✓ Sudah  › 19 file (7.9 MB)
◷ Belum  › 7 file (10.8 MB)
```

---

## Step 5 — Periksa file yang belum upload

AMUV7 menampilkan daftar secara ringkas.

Misalnya:

```text
📋 Rincian file

• IMG_2571.jpg
• IMG_2604.jpg
• VID_20250819_0917.mp4
• tokio_blue_archive.jpg
• savevid_aQ0Cb1o7y3aBl1WxCI7Q...mp4
```

Kalau nama terlalu panjang:

```text
nama-super-panjang-yang-bikin-terminal-menangis...mp4
```

akan dipersingkat.

---

## Step 6 — Upload Gate

AMUV7 bertanya:

```text
│ Mau diupload sekarang gak?

[Y]  Boleh
[N]  Jangan dulu ◄
```

### Mau upload?

Ketik:

```text
Y
```

atau:

```text
ya
```

atau:

```text
1
```

Kemudian proses upload dipanggil melalui callback uploader yang sudah tersedia.

### Belum mau upload?

Tekan:

```text
Enter
```

atau:

```text
N
```

AMUV7 kembali ke menu.

---

# 🛡️ KENAPA DEFAULT-NYA N?

Karena automation itu keren.

Automation yang salah pencet:

> **tidak keren.** 💀

Default:

```text
N = Jangan dulu
```

berfungsi sebagai safety gate sederhana agar media tidak langsung di-upload hanya karena user masuk ke menu pengecekan.

---

# 🧪 DEBUGGING DASAR

Kalau kamu melakukan modifikasi Python dan ingin mengecek syntax sebelum menjalankan:

```bash
python -m py_compile menu.py
```

Jika tidak ada output error:

```text
✅ Syntax aman
```

Kalau ada error:

```text
SyntaxError
```

jangan panik.

Itu Python sedang bilang:

> "Bro, ada typo."

---

# 🔧 WORKFLOW PENGEMBANGAN YANG DISARANKAN

Kalau ingin memodifikasi AMUV7:

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

# 🧬 CONFIGURATION

Tema utama saat ini:

```text
Theme: moss
Version: 7.1.0
Primary: #2BEE34
Base: #141414
```

Default theme dikendalikan melalui konfigurasi project.

Jangan hard-code perubahan konfigurasi di banyak file kalau sebenarnya nilai tersebut sudah tersedia melalui config manager.

---

# 🎨 DESIGN PHILOSOPHY

AMUV7 bukan cuma ingin:

> "yang penting jalan."

Tapi:

> **"jalan + enak dilihat + enak dipakai."**

Prinsip visualnya:

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
🌿 AMUV7 UI
```

---

# 🗺️ ROADMAP

> Roadmap ini adalah arah pengembangan yang direncanakan, bukan janji bahwa semua item sudah tersedia.

## 🟢 Phase 1 — Core

- [x] Automated uploader foundation
- [x] CLI menu
- [x] Multi-account foundation
- [x] Media folder scanner
- [x] Upload status/cache detection
- [x] Upload progress
- [x] Media statistics

---

## 🟢 Phase 2 — UI Refresh

- [x] Luminous Moss theme
- [x] Manager UI redesign
- [x] About UI redesign
- [x] Gallery theme synchronization
- [x] Cyber Moss Upload Gate
- [x] Gradient upload options
- [x] Compact long filenames

---

## 🟡 Phase 3 — Gallery Experience

- [x] Video centering
- [x] Dynamic backdrop blur
- [x] Touch gesture swipe
- [x] Metadata grid redesign
- [x] Moss theme synchronization

---

## 🟡 Phase 4 — UX Polish

- [ ] Gabungkan seluruh dashboard + confirmation menjadi satu `UPLOAD GATE`
- [ ] Optimasi layout untuk layar Android kecil
- [ ] Penyempurnaan responsive terminal UI
- [ ] Pengurangan output terminal yang tidak perlu
- [ ] Better error recovery
- [ ] More granular upload controls

---

## 🔵 Phase 5 — Automation++

Ide pengembangan:

- [ ] Scheduled upload
- [ ] Queue management
- [ ] Retry system yang lebih pintar
- [ ] Upload history viewer
- [ ] Filtering media
- [ ] Search media
- [ ] Per-account upload statistics
- [ ] Better logging
- [ ] Backup/restore configuration

---

## 🟣 Phase 6 — Gallery++

Ide jangka panjang:

- [ ] Lazy loading yang lebih agresif
- [ ] Thumbnail optimization
- [ ] Better video preview performance
- [ ] Gallery caching
- [ ] Improved mobile gesture system
- [ ] Advanced media metadata
- [ ] More gallery themes

---

# 📈 VERSION HISTORY

## `v7.1.2` — Upload Gate Dashboard

### Added

- Cyber Moss Upload Gate.
- Media statistics integrated into Upload Gate dashboard.
- Upload status integrated into dashboard.
- Upload progress visualization.
- Compact file listing.
- Long filename shortening.
- Subfolder/category compact display.
- Gradient Y/N options.
- Default arrow indicator.

### Behavior

```text
Y / ya / 1 → Upload
N / Enter   → Back
Other input → Back
```

---

## `v7.1.1` — Cyber Moss Upload Gate

### Added

- Upload confirmation prompt.
- Default `N`.
- Cyber Moss visual style.
- Borderless terminal UI.
- Gradient options.
- Dynamic default arrow.

---

## `v7.1.0` — Luminous Moss Synchronization

### Added / Updated

- Global theme `moss`.
- Default theme configuration.
- Luminous Moss manager UI.
- Luminous Moss about UI.
- Moss terminal helpers.
- Moss upload progress.

---

## `v7.0.x` — Gallery & Media UX

Major improvements included:

- Video centering.
- Dynamic backdrop blur.
- Touch gesture/swipe interaction.
- Metadata grid redesign.
- Gallery theme synchronization.
- Media statistics.
- Uploaded/not-uploaded status tracking.
- Enhanced media folder checking.

---

# 🧯 TROUBLESHOOTING

## ❌ "Python command tidak ditemukan"

Coba:

```bash
pkg install python
```

Lalu:

```bash
python --version
```

---

## ❌ Storage tidak bisa diakses

Jalankan:

```bash
termux-setup-storage
```

Kemudian berikan permission Android.

---

## ❌ Script error setelah diedit

Pertama:

```bash
python -m py_compile menu.py
```

Kalau gagal, baca baris error yang ditunjukkan Python.

---

## ❌ Upload tidak dimulai

Pastikan:

1. Ada media yang belum diupload.
2. Account aktif sudah dipilih.
3. Konfigurasi account benar.
4. Callback/engine uploader tersedia.
5. Kamu memilih:

```text
Y
```

atau:

```text
ya
```

atau:

```text
1
```

---

## ❌ Nama file terlalu panjang

AMUV7 sudah memiliki mekanisme pemendekan nama pada tampilan daftar file.

Nama file asli **tidak diubah** hanya karena nama yang ditampilkan dipersingkat.

---

# 🤝 CONTRIBUTING

Pull request, issue, ide UI, dan eksperimen sangat welcome.

Workflow sederhana:

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

Sebelum mengirim perubahan Python:

```bash
python -m py_compile <file>.py
```

Dan sebisa mungkin:

> jangan mengubah engine upload hanya demi mempercantik warna tombol. 😭

---

# 🧪 DEVELOPMENT NOTES

AMUV7 masih aktif dikembangkan.

Beberapa bagian UI dan automation dapat berubah antar versi.

Checkpoint project digunakan untuk menjaga state pengembangan dan mencegah perubahan baru menghapus pekerjaan sebelumnya.

Untuk sesi development, biasakan membuat:

```text
checkpoint.md
```

setelah milestone besar.

---

# ❤️ DIBUAT DENGAN

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

# 🙏 TERIMA KASIH KEPADA

AMUV7 dibangun dengan memanfaatkan ekosistem open-source dan inspirasi dari berbagai tools, library, dokumentasi, komunitas, serta para developer yang membagikan pengetahuan mereka.

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

# 👤 AUTHOR

> **Catatan:** identitas GitHub, foto profil, kontak, dan link donasi belum tersedia di source/checkpoint project yang menjadi basis README ini. Karena itu bagian berikut sengaja memakai placeholder dan **tidak mengarang identitas author**.

<p align="center">
  <img src="https://github.com/YOUR_GITHUB_USERNAME.png?size=180" width="120" height="120" style="border-radius:50%" alt="Author Profile">
</p>

<h3 align="center">👨‍💻 YOUR NAME / YOUR ALIAS</h3>

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
| 🐙 GitHub | `https://github.com/YOUR_GITHUB_USERNAME` |
| 💬 Telegram | `YOUR_TELEGRAM_CONTACT` |
| 📧 Email | `YOUR_EMAIL@example.com` |
| 🌐 Website | `YOUR_WEBSITE` |
| ☕ Donation | `YOUR_DONATION_LINK` |

### 💚 Support Development

Kalau AMUV7 membantu pekerjaanmu dan ingin mendukung pengembangannya:

```text
☕ Buy me a coffee
💚 Donate
⭐ Star repository
🐛 Report bug
💡 Kirim ide
```

> Bahkan satu ⭐ GitHub kadang cukup untuk membuat developer kembali membuka laptop setelah bilang:
>
> **"Udah, besok aja lanjut."** 😂

---

# 💰 DONASI

Project ini gratis dan menggunakan **MIT License**.

Jika ingin mendukung:

```text
☕ YOUR_DONATION_LINK
```

Pilihan platform dapat diisi sesuai akun author, misalnya:

- Ko-fi
- Saweria
- Trakteer
- GitHub Sponsors
- PayPal
- platform donasi lain

> Jangan memasukkan link pembayaran pribadi sebelum mengganti placeholder dengan link resmi author.

---

# 📜 LICENSE

AMUV7 menggunakan **MIT License**.

```text
MIT License

Copyright (c) 2026 YOUR NAME / YOUR ALIAS

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

> ⚠️ Ganti `YOUR NAME / YOUR ALIAS` dengan nama pemegang copyright sebelum repository dipublikasikan.

---

# ⭐ SUPPORT THE PROJECT

Kalau project ini berguna:

```text
⭐ Star
🍴 Fork
🐛 Report bugs
💡 Suggest features
🔧 Submit PR
📢 Share
☕ Donate
```

Yang paling simpel:

> **Kasih ⭐. Gratis. Tidak mengurangi kuota nasi.** 🍚😂

---

# 🧭 FINAL WORD

AMUV7 bukan project yang lahir langsung sempurna.

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

**AMUV7 — Automate the boring stuff. Keep the moss glowing. 🌿⚡**

<p align="center">
  <b>Made with 🧠 + 🐍 + 📱 + ☕ + sedikit chaos.</b>
</p>
