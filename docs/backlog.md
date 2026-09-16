# 📋 BACKLOG — LUMOSS v7.2.12

**Update terakhir:** 2026-09-17
**Total issues:** 38 PR (FASE 4) + 1 side project
**Status:** ⏸️ BACKLOG (4 selesai, 34 pending)

📎 **Checkpoint terkait:** `docs/checkpoint.md`
📎 **State terkait:** `docs/state.md`

---

## 🎯 RINGKASAN

| Kategori | Jumlah |
|----------|--------|
| 🔴 KRITIS | 2 |
| 🟡 MEDIUM | 6 |
| 🟢 MINOR | 24 |
| ⚠️ SKIP | 1 |
| 🔒 LOCKED | 1 |
| 🟢 FINAL | 4 |
| 🟡 KESENTUH | 4 |
| ✅ **SELESAI** | **4** |
| ⏸️ **PENDING** | **34** |
| **TOTAL PR LUMOSS** | **38** |
| **SIDE PROJECT** | **1** |

**PRIORITAS EKSEKUSI (REVISI — PR-7, PR-8 SELESAI):**
1. ~~PR-7 (YouTube Error 153)~~ ✅ **SELESAI**
2. ~~PR-8 (Instagram embed)~~ ✅ **SELESAI**
3. **PR-1** (Layout Main Menu) — 🟡 MEDIUM
4. **PR-4** (GITHUB_REPO gak di-inject) — 🟡 MEDIUM
5. **PR-6** (Cek tools.py v7.1.0) — 🟡 MEDIUM

---

## ✅ SELESAI (4 PR)

### ✅ PR-7: YouTube Error 153 — SELESAI
- **Prioritas:** 🔴 KRITIS
- **Deskripsi:** Embed YouTube error 153 (video unavailable / embedding disabled)
- **File:** `html_builder.py`, `embed_parser.py`, `templates/gallery.html`
- **Status:** ✅ **SELESAI v7.2.11**
- **Solusi:**
  - Tambah parameter `origin={ORIGIN}` (dynamic dari `window.location.origin`)
  - Tambah `enablejsapi=1`, `rel=0`, `modestbranding=1`, `playsinline=1`
  - Fallback UI kalo iframe gagal
- **Verified:** TEST 12 (YouTube embed works)

### ✅ PR-8: Instagram embed header doang — SELESAI
- **Prioritas:** 🔴 KRITIS
- **Deskripsi:** Embed Instagram cuma nampilin header, bukan konten
- **File:** `embed_parser.py`, `templates/gallery.html`
- **Status:** ✅ **SELESAI v7.2.11**
- **Solusi:** URL embed tambah `/captioned/` — biar caption + media muncul
- **Verified:** TEST 13 (IG post + reel works)

### ✅ PR-2: Tag terkait di lightbox kepotong — SELESAI
- **Prioritas:** 🟡 MEDIUM
- **Deskripsi:** Tag di lightbox kepotong kalau >3 tag
- **File:** `templates/gallery.html`
- **Status:** ✅ **RESOLVED** (bukan bug LUMOSS — masalah browser Quetta)
- **Kesimpulan:** Tag gak kepotong di Chrome — masalah di address bar Quetta yang di bawah
- **Verified:** Screenshot Chrome vs Quetta

### ✅ PR-12: Tag terkait kepotong (duplikat PR-2) — SELESAI
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** Sama kayak PR-2 (duplikat)
- **File:** `templates/gallery.html`
- **Status:** ✅ **RESOLVED** (duplikat PR-2)

### 🎁 BONUS (bukan PR di backlog, tapi included di v7.2.11):
- ✅ **Dynamic aspect ratio** — YouTube, IG, TikTok, Vimeo, Twitter, FB
- ✅ **Auto-hide UI** — portrait + landscape
- ✅ **Zona tap** — buat show UI di iframe full
- ✅ **Gallery header auto-hide** — scroll ke bawah
- ✅ **Smart history** — tombol back nutup lightbox
- ✅ **100dvh** — handle address bar mobile
- ✅ **Rebranding** — amuv7 → lumoss (storage keys)

---

## 🐛 GRUP A — BUG FIX LAMA (5 PR PENDING)

### PR-1: Layout Main Menu berantakan
- **Prioritas:** 🟡 MEDIUM
- **Deskripsi:** Layout Main Menu v7.2.0 kadang berantakan di beberapa ukuran terminal
- **File:** `menu.py`
- **Status:** ⏸️ Belum difix

### PR-3: Emoji gear ⚙️ nyempil
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** Emoji gear di menu nyempil dengan teks sebelahnya
- **File:** `menu.py`
- **Status:** ⏸️ Belum difix

### PR-4: GITHUB_REPO gak di-inject
- **Prioritas:** 🟡 MEDIUM
- **Deskripsi:** GITHUB_REPO gak di-inject ke HTML, jadi link repo gak muncul
- **File:** `html_builder.py`
- **Status:** 🟡 KESENTUH rebranding (belum full fix)

### PR-5: Hapus templates/about.html
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** File about.html di templates/ udah gak dipake (About digabung ke gallery)
- **File:** `templates/about.html`
- **Status:** ⏸️ Belum dihapus

### PR-6: Cek tools.py v7.1.0
- **Prioritas:** 🟡 MEDIUM
- **Deskripsi:** Ada file tools.py versi lama di root, cek dulu sebelum hapus
- **File:** `tools.py`
- **Status:** ⏸️ Belum dicek

---

## 📺 GRUP B — EMBED SYSTEM (5 PR PENDING)

### PR-9: Deteksi embed vs video
- **Prioritas:** 🟡 MEDIUM
- **Deskripsi:** Sistem kadang salah deteksi embed vs video native
- **File:** `embed_parser.py`
- **Status:** ⏸️ Belum difix

### PR-10: Info panel "0 B (MP4)"
- **Prioritas:** 🟡 MEDIUM
- **Deskripsi:** Info panel nampilin "0 B (MP4)" untuk file embed
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum difix

### PR-11: Link "Buka di platform"
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** Tambah link "Buka di platform" di lightbox embed
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum difix (sebagian udah ada di fallback UI)

### PR-13: Konsistensi nama file embed
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** Nama file embed kadang beda-beda format
- **File:** `embed_parser.py`
- **Status:** ⏸️ Belum difix

### PR-14: Auto-match favicon per platform
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** Otomatis pilih favicon berdasarkan platform embed
- **File:** `templates/gallery.html`, `embed_parser.py`
- **Status:** ⏸️ Belum difix

---

## ⚙️ GRUP C — SETTING (6 PR PENDING)

### PR-15: Auto-hide header on scroll
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** Header auto-hide saat scroll ke bawah
- **File:** `templates/gallery.html`
- **Status:** ✅ **SELESAI v7.2.11** (bonus)

### PR-16: Menu Favicon (A+B Hybrid)
- **Prioritas:** 🟢 FINAL
- **Deskripsi:** Menu setting favicon — Hybrid opsi A+B
- **File:** `menu.py`, `config_manager.py`
- **Status:** ⏸️ Belum dikerjain

### PR-17: Bundle Pengaturan Galeri
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** Gabungin pengaturan galeri jadi 1 bundle
- **File:** `menu.py`
- **Status:** ⏸️ Belum difix

### PR-18: Preview live terminal
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** Preview theme di terminal sebelum apply
- **File:** `menu.py`
- **Status:** ⏸️ Belum difix

### PR-19: Export/Import config
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** Export & import config akun
- **File:** `config_manager.py`
- **Status:** 🟡 KESENTUH rebranding

### PR-20: Per-account setting
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** Setting per-akun (bukan global)
- **File:** `config_manager.py`
- **Status:** ⏸️ Belum difix

---

## ✨ GRUP D — VISUAL POLISH (6 PR PENDING)

### PR-21: Animasi judul Glow Pulse
- **Prioritas:** 🟢 FINAL
- **Deskripsi:** Animasi Glow Pulse di judul galeri (Opsi A)
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum dikerjain

### PR-22: Stagger fade-in card
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** Card muncul stagger (satu-satu) dengan fade-in
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum difix

### PR-23: Hover effect card
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** Hover effect di card media
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum difix

### PR-24: Lightbox transition
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** Transisi smooth saat buka lightbox
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum difix

### PR-25: Loading skeleton
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** Loading skeleton saat gambar loading
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum difix

### PR-26: Scroll reveal
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** Elemen muncul saat di-scroll (scroll reveal)
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum difix

---

## 🌊 GRUP E — UX & PERF (3 PR)

### PR-27: Moss particle bg
- **Prioritas:** ⚠️ SKIP
- **Deskripsi:** Background partikel moss (dibatalin — terlalu berat)
- **File:** -
- **Status:** ⚠️ SKIP (keputusan final)

### PR-28: Smooth navigation paket
- **Prioritas:** 🟢 FINAL
- **Deskripsi:** Paket "Smooth UX" (navigasi halus)
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum dikerjain

### PR-29: Support 120Hz optional
- **Prioritas:** 🟢 FINAL
- **Deskripsi:** Support 120Hz (optional, default OFF)
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum dikerjain

---

## 🧠 GRUP F — ADVANCED (8 PR)

### PR-30: Auto grouping wajah
- **Prioritas:** 🔒 LOCKED
- **Deskripsi:** Auto grouping wajah (optional, fitur advanced)
- **File:** `media_processor.py`
- **Status:** 🔒 LOCKED OPTIONAL

### PR-31: Auto-tag EXIF
- **Prioritas:** 🟢 PILIH
- **Deskripsi:** Auto-tag dari EXIF metadata
- **File:** `media_processor.py`
- **Status:** ⏸️ Belum difix

### PR-32: Duplicate detection
- **Prioritas:** 🟢 PILIH
- **Deskripsi:** Deteksi file duplikat
- **File:** `media_processor.py`
- **Status:** ⏸️ Belum difix

### PR-35: Timeline view
- **Prioritas:** 🟢 PILIH
- **Deskripsi:** Tampilan timeline (per tanggal)
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum difix

### PR-38: Dark/Light mode toggle
- **Prioritas:** 🟢 PILIH
- **Deskripsi:** Toggle dark/light mode
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum difix

### PR-40: Thumbnail generation
- **Prioritas:** 🟡 PILIH ⭐🥇
- **Deskripsi:** Generate thumbnail (prioritas tertinggi)
- **File:** `media_processor.py`
- **Status:** 🟡 KESENTUH rebranding (belum full fix)

### PR-43: Pagination / infinite scroll
- **Prioritas:** 🟡 PILIH ⭐🥈
- **Deskripsi:** Pagination atau infinite scroll
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum difix

### PR-47: PWA install as app
- **Prioritas:** 🟢 PILIH
- **Deskripsi:** PWA install as app (bisa di-install ke homescreen)
- **File:** `templates/gallery.html`, `manifest.json`
- **Status:** ⏸️ Belum difix

---

## 🌐 GRUP G — INFRA (1 PR)

### PR-51: Custom domain support
- **Prioritas:** 🟢 BARU
- **Deskripsi:** Support custom domain (bukan cuma GitHub Pages)
- **File:** `html_builder.py`, `config_manager.py`
- **Status:** 🟡 KESENTUH rebranding (belum full fix)

---

## 🎬 SIDE PROJECT (1 — bukan bagian LUMOSS)

### PR-PORTFOLIO: Cinematic Resume Portfolio
- **Prioritas:** 🟡 MEDIUM
- **Deskripsi:** Deploy Cinematic Resume sebagai portfolio pribadi di `nexterade.github.io`
- **Repo:** `https://github.com/nexterade/nexterade.github.io`
- **Lokal:** `~/nexterade.github.io/`
- **Base:** Cinematic Resume (Next.js 16.3.5, Webpack)
- **Status:** ⏸️ PENDING (base jalan, rombak belum)

**Setup yang udah kelar:**
- ✅ Fork repo Cinematic Resume
- ✅ Clone ke Termux
- ✅ Pindah ke home (fix symlink error)
- ✅ `npm install` sukses (96 packages, 0 vulnerabilities)
- ✅ Preview lokal jalan: `npm run dev -- --webpack`

**Task rombak (belum):**
- ⏸️ Isi `data/resumeContent.js` dengan data pribadi
- ⏸️ Ganti styling di `tailwind.config.js` (moss green theme)
- ⏸️ Fix hydration error di `app/layout.tsx`
- ⏸️ Fix GSAP target error
- ⏸️ Deploy ke GitHub Pages
- ⏸️ Update README LUMOSS — isi field Website

---

## 📊 RINGKASAN LENGKAP

| Kategori | Jumlah |
|----------|--------|
| **TOTAL PR (LUMOSS)** | **38 PR** |
| ✅ SELESAI | **4** (PR-2, PR-7, PR-8, PR-12) |
| ⏸️ PENDING | **34** |
| 🔴 KRITIS | 0 (semua selesai) |
| 🟡 MEDIUM | 4 (PR-1, PR-4, PR-6, PR-9) |
| 🟢 MINOR | 22 |
| ⚠️ SKIP | 1 (PR-27) |
| 🔒 LOCKED | 1 (PR-30) |
| 🟢 FINAL | 4 (PR-16, PR-21, PR-28, PR-29) |
| 🟡 KESENTUH rebranding | 4 (PR-4, PR-19, PR-40, PR-51) |
| **SIDE PROJECT** | **1 (PR-PORTFOLIO)** |

---

## 🎯 URUTAN PENGERJAAN (REKOMENDASI)

### **FASE 4A — MEDIUM (4 PR)** ⭐ **PRIORITAS**
1. **PR-1** (Layout Main Menu) — 🟡 MEDIUM
2. **PR-4** (GITHUB_REPO) — 🟡 MEDIUM
3. **PR-6** (Cek tools.py) — 🟡 MEDIUM
4. **PR-9** (Deteksi embed vs video) — 🟡 MEDIUM

### **FASE 4B — FINAL (4 PR)**
5. PR-16 (Menu Favicon)
6. PR-21 (Animasi Glow Pulse)
7. PR-28 (Smooth navigation)
8. PR-29 (Support 120Hz)

### **FASE 4C — PILIH (2 PR prioritas)**
9. PR-40 (Thumbnail generation) ⭐🥇
10. PR-43 (Pagination) ⭐🥈

### **FASE 4D — MINOR (24 PR)**
11. PR-3, PR-5, PR-10, PR-11, PR-13, PR-14, PR-15✅, PR-17, PR-18, PR-19, PR-20, PR-22, PR-23, PR-24, PR-25, PR-26, PR-31, PR-32, PR-35, PR-38, PR-47, PR-51
+ PR-27 (SKIP), PR-30 (LOCKED)

### **SIDE PROJECT**
12. PR-PORTFOLIO (Cinematic Resume) — PENDING

---

## 🎯 NEXT STEP

**Pilih salah satu:**
1. **PR-1** (Layout Main Menu) — 🟡 MEDIUM, butuh `menu.py`
2. **PR-4** (GITHUB_REPO) — 🟡 MEDIUM, cepet
3. **PR-6** (Cek tools.py) — 🟡 MEDIUM, cek dulu
4. **PR-9** (Deteksi embed) — 🟡 MEDIUM, butuh `embed_parser.py`
5. **PR-40** (Thumbnail) — 🟡 PILIH ⭐🥇

**Rekomendasi:** Mulai dari **PR-1** — karena udah lama pending & medium priority.

---

**END OF BACKLOG v7.2.12**