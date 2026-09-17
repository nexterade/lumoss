# 🌿 LUMOSS — Media Garden, in bloom

<p align="center">
  <img src="https://img.shields.io/badge/LUMOSS-v7.2.13-2BEE34?style=for-the-badge&logo=leaflet&logoColor=white" alt="LUMOSS Version">
  <img src="https://img.shields.io/badge/Python-3.14%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Termux-Android-000000?style=for-the-badge&logo=termux&logoColor=white" alt="Termux">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT License">
</p>

<p align="center">
  <b>Upload media otomatis dari HP, tanpa drama, tanpa klik-klik sampai jempol keriting. 🌿</b>
</p>

---

## 📖 DAFTAR ISI

> Klik buat loncat ke section. Cocok buat yang gak sabaran. 😌

- [🌿 LUMOSS itu apaan?](#-lumoss-itu-apaan)
- [✨ Fitur Utama](#-fitur-utama)
- [🚀 Quick Start](#-quick-start)
- [📁 Struktur Project](#-struktur-project)
- [🎨 Themes](#-themes)
- [📈 Changelog](#-changelog)
- [🔗 Link Berguna](#-link-berguna)
- [👤 Author](#-author)
- [📜 License](#-license)

---

## 🌿 LUMOSS itu apaan?

**LUMOSS (Luminous Moss)** adalah tool automation berbasis Python untuk **upload otomatis foto/video** ke Catbox.moe, generate **galeri HTML interaktif**, dan **deploy ke GitHub Pages** — semua dari terminal Android (Termux).

> Dulu dikenal sebagai **AMUV7** (Automated Media Uploader v7) — sekarang rebranding jadi LUMOSS.

**Alur:**

📂 Media Folder → 🔍 Scan → 📊 Statistik → 🧠 Cek Cache → ☁️ Upload → 🎨 Generate HTML → 🚀 Deploy

**Tagline:** *Media Garden, in bloom.*

---

## ✨ Fitur Utama

### 📤 Upload Otomatis
- Multi-akun Catbox (folder terisolasi per akun)
- Multi-folder media (DCIM + Pictures + Download, dll)
- Cache tracking (skip file yang udah diupload)
- Retry otomatis + rate limit handling
- Progress bar real-time

### 🎨 Gallery Interaktif
- **6 tema aesthetic** — Moss, Dark, Light, AMOLED, Midnight, Sunset
- **2 layout** — Mosaic (Pinterest) + Grid
- Search, filter, sort
- Lightbox dengan zoom + swipe + keyboard shortcut
- Autoplay video Instagram-style
- Auto-hide UI (portrait + landscape)

### 🌐 Import Embed
- YouTube (watch + shorts)
- Instagram (post + reel + tv)
- TikTok, Facebook, Twitter/X, Vimeo
- Auto-detect aspect ratio (16:9, 9:16, 4:5)
- Platform icon + gradient per brand
- Auto-tag dari URL (opsional)

### 🛠️ Tools Bantu
- Upload ke GitHub Pages 1 klik
- Backup project (zip)
- Fix broken cache
- Cleanup thumbnail lama
- Kelola folder media (add/remove/toggle)

### 🎯 UI Terminal
- Banner LUMOSS + tree view menu
- Emoji auto-convert (Unicode symbol)
- Color palette Luminous Moss (#2BEE34)
- Unicode box-drawing (anti-miring)

---

## 🚀 Quick Start

### 1. Install Termux + Python

pkg update && pkg upgrade
pkg install python
termux-setup-storage

### 2. Clone & Install

cd /storage/emulated/0/Project/
git clone https://github.com/nexterade/lumoss.git
cd lumoss
pip install -r requirements.txt

### 3. Jalankan

python lumoss.py

### 4. Flow Cepat

1. Buat akun → Menu 5 (Account Manager)
2. Pilih folder media → Onboarding / Menu 7 → 5
3. Taruh foto/video di folder → Auto-detect
4. Upload → Menu 1 (Jalankan Upload)
5. Buka galeri → output/<slug>/index.html

> 💡 **Tip:** Upload pertama kali pake Y di Upload Gate. Setelah itu cache bikin skip file lama.

---

## 📁 Struktur Project
```
lumoss/
├── accounts/               ← Config per akun (active.json + <slug>/config.json)
├── output/                 ← Hasil generate HTML per akun
├── cache/                  ← Cache upload + blacklist
├── templates/              ← Template HTML + platform-icons.js
├── docs/                   ← Dokumentasi (checkpoint, state, backlog)
├── backup/                 ← Backup zip
│
├── lumoss.py               ← Entry point
├── menu.py                 ← Menu utama
├── uploader.py             ← Engine upload
├── media_processor.py      ← EXIF, thumbnail, auto-tag
├── html_builder.py         ← Generator HTML
├── embed_parser.py         ← Parser URL embed
├── ui_helpers.py           ← UI terminal (box, color, emoji)
├── account_manager.py      ← Multi-account
├── config_manager.py       ← Config
├── tools.py                ← Tools bantu
└── menu_*.py               ← Submenu (account, embed, tools)

**Detail struktur:** docs/state.md → section 4
```
---

## 🎨 Themes

| Nama | Preview | Deskripsi |
|------|---------|-----------|
| **Moss** 🌿 | #2BEE34 | Hijau neon (default) |
| **Dark** 🌙 | #58a6ff | Biru gelap |
| **Light** ☀️ | #0969da | Putih terang |
| **AMOLED** ⚫ | #ffffff | Hitam pekat |
| **Midnight** 🌌 | #22d3ee | Cyan malam |
| **Sunset** 🌅 | #f97316 | Oranye-pink |

**Ganti tema:** Menu 8 (Pilih Tema) atau via UI gallery → tombol 🎨

---

## 📈 Changelog

### v7.2.13 — Platform Icons + Auto-Tag (Terbaru)
- ✅ **PR-9** — Deteksi embed vs video (query string, HLS/DASH, whitelist)
- ✅ **PR-10** — Info panel embed (bukan "0 B")
- ✅ **PR-11** — Tombol "Buka di Platform" (dynamic action bar)
- 🎁 **Platform Icon** — SVG inline per platform (YouTube, IG, TikTok, dll)
- 🎁 **Auto-Tag** — Extract tag dari URL embed (opt-in fetch title)
- 🔧 **Refactor** — gallery.html + platform-icons.js dipisah

### v7.2.12 — Tree View + GITHUB_REPO Fix
- ✅ **PR-1** — Main menu pake tree view (ala tree command)
- ✅ **PR-3** — Emoji gear ⚙ nyempil → symbol konsisten
- ✅ **PR-4** — GITHUB_REPO chain fix (opsional, kalo diisi muncul)
- ✅ **PR-5** — templates/about.html dihapus
- ✅ **PR-6** — tools.py header cleanup

### v7.2.11 — Embed Fix
- ✅ **PR-7** — YouTube error 153 fix (origin + enablejsapi)
- ✅ **PR-8** — Instagram embed /captioned/
- 🎁 Dynamic aspect ratio, auto-hide UI, smart history

### Versi Lama
Lihat **Releases** → https://github.com/nexterade/lumoss/releases

---

## 🔗 Link Berguna

| Link | Deskripsi |
|------|-----------|
| 🐙 **Repo** | https://github.com/nexterade/lumoss |
| 📦 **Releases** | https://github.com/nexterade/lumoss/releases |
| 🐛 **Issues** | https://github.com/nexterade/lumoss/issues |
| 📖 **Docs** | docs/checkpoint.md, docs/state.md, docs/backlog.md |
| 🌐 **Portfolio** | https://nexterade.github.io |

---

## 👤 Author

<p align="center">
  <img src="https://github.com/nexterade.png?size=180" width="120" height="120" style="border-radius:50%" alt="Author Profile">
</p>

<h3 align="center">🌿 nexterade</h3>

<p align="center">
  <i>Builder • Tinkerer • Automation Enjoyer</i>
</p>

**Contact:**
- 🐙 GitHub — @nexterade (https://github.com/nexterade)
- 💬 Telegram — @nexterade (https://t.me/nexterade)
- 📧 Email — nexterade@gmail.com
- 🌐 Website — https://nexterade.github.io

---

## 🤝 Contributing

Pull request, issue, ide UI — sangat welcome.

git clone https://github.com/nexterade/lumoss.git
cd lumoss
python -m py_compile <file>.py

> ⚠️ Sebelum kirim PR: pastiin py_compile OK, dan jangan ubah engine upload cuma buat "mempercantik warna tombol". 😌

---

## 📜 License

**MIT License** — Copyright (c) 2026 nexterade

Full text: LICENSE (https://github.com/nexterade/lumoss/blob/main/LICENSE) atau docs/LICENSE.md

---

## ⭐ Support

Kalau LUMOSS berguna:

⭐ Star repo
🐛 Report bug
💡 Suggest feature
🔧 Submit PR

> **Kasih ⭐. Gratis. Gak ngurangin kuota nasi.** 🍚😂

---

## 🧭 Catatan

**LUMOSS** lahir dari prinsip sederhana:

> *Kalo pekerjaan bisa diotomatis, kenapa manual berkali-kali?*

Project ini **masih aktif dikembangkan**. Beberapa fitur udah live, beberapa masih di pipeline.

**Detail lengkap:**
- 🎯 **Checkpoint** — docs/checkpoint.md (aturan + kepribadian)
- 📊 **State** — docs/state.md (progress + struktur)
- 📋 **Backlog** — docs/backlog.md (38 PR + roadmap)

**LUMOSS — Media Garden, in bloom. 🌿⚡**

<p align="center">
  <b>Made with 🧠 + 🐍 + 📱 + ☕ + sedikit chaos.</b>
</p>