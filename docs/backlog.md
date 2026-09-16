# 📋 BACKLOG — LUMOSS v7.2.8

**Update terakhir:** 2026-09-16
**Total issues:** 38 PR (FASE 5) + 1 side project
**Status:** ⏸️ BACKLOG (belum disentuh)

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
| **TOTAL PR LUMOSS** | **38** |
| **SIDE PROJECT** | **1** |

**PRIORITAS EKSEKUSI:**
1. **PR-7** (YouTube Error 153) — 🔴 KRITIS
2. **PR-8** (Instagram embed header) — 🔴 KRITIS
3. **PR-1** (Layout Main Menu) — 🟡 MEDIUM
4. **PR-2** (Tag lightbox) — 🟡 MEDIUM
5. **PR-4** (GITHUB_REPO gak di-inject) — 🟡 MEDIUM

---

## 🐛 GRUP A — BUG FIX LAMA (6 PR)

### PR-1: Layout Main Menu berantakan
- **Prioritas:** 🟡 MEDIUM
- **Deskripsi:** Layout Main Menu v7.2.0 kadang berantakan di beberapa ukuran terminal
- **File:** `menu.py`
- **Status:** ⏸️ Belum difix

### PR-2: Tag terkait di lightbox kepotong
- **Prioritas:** 🟡 MEDIUM
- **Deskripsi:** Tag di lightbox kepotong kalau lebih dari 3 tag
- **File:** `templates/gallery.html`
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

## 📺 GRUP B — EMBED SYSTEM (7 PR)

### PR-7: YouTube Error 153
- **Prioritas:** 🔴 KRITIS
- **Deskripsi:** Embed YouTube error 153 (video unavailable / embedding disabled)
- **File:** `html_builder.py`, `embed_parser.py`
- **Status:** 🔴 CONFIRMED — belum difix

### PR-8: Instagram embed header doang
- **Prioritas:** 🔴 KRITIS
- **Deskripsi:** Embed Instagram cuma nampilin header, bukan konten
- **File:** `html_builder.py`, `embed_parser.py`
- **Status:** ⚠️ Perlu VERIFIKASI

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
- **Status:** ⏸️ Belum difix

### PR-12: Tag terkait kepotong
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** Sama kayak PR-2 (duplikat)
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum difix

### PR-13: Konsistensi nama file embed
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** Nama file embed kadang beda-beda format
- **File:** `embed_parser.py`
- **Status:** ⏸️ Belum difix

---

## ⚙️ GRUP C — SETTING (7 PR)

### PR-14: Auto-match favicon per platform
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** Otomatis pilih favicon berdasarkan platform embed
- **File:** `templates/gallery.html`, `embed_parser.py`
- **Status:** ⏸️ Belum difix

### PR-15: Auto-hide header on scroll
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** Header auto-hide saat scroll ke bawah
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum difix

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

## ✨ GRUP D — VISUAL POLISH (6 PR)

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
- ⏸️ Fix GSAP target error (`.project-stage-shell`, `.timeline-mobile-card`)
- ⏸️ Deploy ke GitHub Pages
- ⏸️ Update README LUMOSS — isi field Website

**Catatan teknis:**
- Next.js 16.3.5 — Turbopack **GAK SUPPORT** Android/arm64
- Dev server **WAJIB** pake Webpack: `npm run dev -- --webpack`
- Hydration error karena font variable — bukan fatal
- GSAP error karena section kosong — fix setelah isi data
- Struktur: `app/`, `components/`, `data/`, `hooks/`, `lib/`, `scripts/`

---

## 📊 RINGKASAN LENGKAP

| Kategori | Jumlah |
|----------|--------|
| **TOTAL PR (LUMOSS)** | **38 PR** |
| ⏸️ Belum difix | 30 |
| 🔴 KRITIS (confirmed) | 1 (PR-7) |
| 🔴 KRITIS (verifikasi) | 1 (PR-8) |
| ⚠️ SKIP | 1 (PR-27) |
| 🔒 LOCKED | 1 (PR-30) |
| 🟢 FINAL | 4 (PR-16, PR-21, PR-28, PR-29) |
| 🟡 KESENTUH rebranding | 4 (PR-4, PR-19, PR-40, PR-51) |
| **SIDE PROJECT** | **1 (PR-PORTFOLIO)** |

---

## 🎯 URUTAN PENGERJAAN (REKOMENDASI)

### **FASE 5A — KRITIS (2 PR)**
1. PR-7 (YouTube Error 153)
2. PR-8 (Instagram embed header)

### **FASE 5B — MEDIUM (5 PR)**
3. PR-1 (Layout Main Menu)
4. PR-2 (Tag lightbox)
5. PR-4 (GITHUB_REPO)
6. PR-9 (Deteksi embed vs video)
7. PR-10 (Info panel "0 B (MP4)")

### **FASE 5C — FINAL (4 PR)**
8. PR-16 (Menu Favicon)
9. PR-21 (Animasi Glow Pulse)
10. PR-28 (Smooth navigation)
11. PR-29 (Support 120Hz)

### **FASE 5D — PILIH (2 PR prioritas)**
12. PR-40 (Thumbnail generation) ⭐🥇
13. PR-43 (Pagination) ⭐🥈

### **FASE 5E — SISANYA (23 PR)**
14. PR-3, 5, 6, 11, 13, 14, 15, 17, 18, 19, 20, 22, 23, 24, 25, 26, 31, 32, 35, 38, 47, 51
+ PR-27 (SKIP), PR-30 (LOCKED)

### **SIDE PROJECT**
15. PR-PORTFOLIO (Cinematic Resume) — PENDING

---

## 🎯 NEXT STEP

**Pilih salah satu:**
1. **PR-7** (YouTube) — 🔴 KRITIS, butuh `html_builder.py` & `embed_parser.py`
2. **PR-8** (Instagram) — 🔴 KRITIS, butuh file yang sama
3. **PR-4** (GITHUB_REPO) — 🟡 MEDIUM, cepet
4. **PR-40** (Thumbnail) — 🟡 PILIH ⭐🥇
5. **PR-PORTFOLIO** (Cinematic Resume) — 🟡 MEDIUM

**Rekomendasi:** Mulai dari **PR-7** — karena ini **KRITIS** & user **paling ngerasain** (YouTube error).

---

**END OF BACKLOG v7.2.8**