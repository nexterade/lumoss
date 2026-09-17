# 📋 BACKLOG — LUMOSS v7.2.12

**Update terakhir:** 2026-09-17
**Total issues:** 38 PR (FASE 4) + 1 side project
**Status:** 🔥 IN PROGRESS (9 selesai, 29 pending)

📎 **Checkpoint terkait:** `docs/checkpoint.md`
📎 **State terkait:** `docs/state.md`

---

## 🎯 RINGKASAN

| Kategori | Jumlah |
|----------|--------|
| 🔴 KRITIS | 0 (semua selesai) |
| 🟡 MEDIUM | 4 |
| 🟢 MINOR | 19 |
| ⚠️ SKIP | 1 |
| 🔒 LOCKED | 1 |
| 🟢 FINAL | 4 |
| 🟡 KESENTUH | 4 |
| ✅ **SELESAI** | **9** |
| ⏸️ **PENDING** | **29** |
| **TOTAL PR LUMOSS** | **38** |
| **SIDE PROJECT** | **1** |

**PRIORITAS EKSEKUSI:**
1. ~~PR-1 (Layout Main Menu)~~ ✅ **SELESAI v7.2.12**
2. ~~PR-2 (Tag lightbox)~~ ✅ **SELESAI**
3. ~~PR-3 (Emoji gear)~~ ✅ **SELESAI v7.2.12**
4. ~~PR-4 (GITHUB_REPO)~~ ✅ **SELESAI v7.2.12**
5. ~~PR-5 (templates/about.html)~~ ✅ **SELESAI v7.2.12**
6. ~~PR-6 (tools.py header)~~ ✅ **SELESAI v7.2.12**
7. ~~PR-7 (YouTube Error 153)~~ ✅ **SELESAI v7.2.11**
8. ~~PR-8 (Instagram embed)~~ ✅ **SELESAI v7.2.11**
9. **PR-9** (Deteksi embed vs video) — 🟡 MEDIUM ← **NEXT!**
10. **PR-10** (Info panel "0 B") — 🟡 MEDIUM
11. **PR-11** (Link "Buka di platform") — 🟢 MINOR

---

## ✅ SELESAI (9 PR)

### ✅ PR-1: Layout Main Menu berantakan — SELESAI v7.2.12
- **Prioritas:** 🟡 MEDIUM
- **Deskripsi:** Layout Main Menu v7.2.0 kadang berantakan di beberapa ukuran terminal
- **File:** `menu.py`, `ui_helpers.py`
- **Status:** ✅ **SELESAI v7.2.12**
- **Solusi:** Tree view ala `tree` command — `render_tree()` + `render_tree_group()`
- **Verified:** TEST 20 (Tree view main menu)

### ✅ PR-2: Tag terkait di lightbox kepotong — SELESAI
- **Prioritas:** 🟡 MEDIUM
- **Status:** ✅ **RESOLVED** (bukan bug LUMOSS — masalah browser Quetta)

### ✅ PR-3: Emoji gear ⚙ nyempil — SELESAI v7.2.12
- **Prioritas:** 🟢 MINOR
- **Deskripsi:** Emoji gear di menu nyempil dengan teks sebelahnya
- **File:** `menu.py`
- **Status:** ✅ **SELESAI v7.2.12** (ganti ⚙️ → ⚙)
- **Verified:** TEST 20

### ✅ PR-4: GITHUB_REPO gak di-inject — SELESAI v7.2.12
- **Prioritas:** 🟡 MEDIUM
- **Deskripsi:** GITHUB_REPO gak di-inject ke HTML, jadi link repo gak muncul
- **File:** `html_builder.py`, `templates/gallery.html`, `lumoss.py`
- **Status:** ✅ **SELESAI v7.2.12**
- **Solusi:** Chain fix — `build_all → build_gallery_html → template`
- **Verified:** TEST 21 (`const GITHUB_REPO = "";`)

### ✅ PR-5: Hapus templates/about.html — SELESAI v7.2.12
- **Prioritas:** 🟢 MINOR
- **File:** `templates/about.html`
- **Status:** ✅ **SELESAI v7.2.12** (file dihapus)
- **Verified:** TEST 23

### ✅ PR-6: Cek tools.py v7.1.0 — SELESAI v7.2.12
- **Prioritas:** 🟡 MEDIUM
- **File:** `tools.py`
- **Status:** ✅ **SELESAI v7.2.12** (header clean, emoji → Unicode)
- **Verified:** TEST 22

### ✅ PR-7: YouTube Error 153 — SELESAI v7.2.11
- **Prioritas:** 🔴 KRITIS
- **File:** `html_builder.py`, `embed_parser.py`, `templates/gallery.html`
- **Status:** ✅ **SELESAI v7.2.11**
- **Solusi:** Parameter origin, enablejsapi, rel, modestbranding, playsinline

### ✅ PR-8: Instagram embed header doang — SELESAI v7.2.11
- **Prioritas:** 🔴 KRITIS
- **File:** `embed_parser.py`, `templates/gallery.html`
- **Status:** ✅ **SELESAI v7.2.11**
- **Solusi:** URL embed tambah `/captioned/`

### ✅ PR-12: Tag terkait kepotong (duplikat PR-2) — SELESAI
- **Status:** ✅ **RESOLVED** (duplikat PR-2)

### 🎁 BONUS (included di v7.2.11 & v7.2.12):
- ✅ Dynamic aspect ratio (YouTube, IG, TikTok, Vimeo, Twitter, FB)
- ✅ Auto-hide UI (portrait + landscape)
- ✅ Zona tap buat show UI
- ✅ Gallery header auto-hide
- ✅ Smart history (tombol back)
- ✅ 100dvh handle address bar mobile
- ✅ Tree view main menu (v7.2.12)
- ✅ Git cleanup (hapus .bak + setup-pointless-repo.sh)
- ✅ .gitignore update

---

## 🟡 GRUP A — BUG FIX (0 PR PENDING)

**Semua bug fix di grup ini udah selesai!** ✅

---

## 📺 GRUP B — EMBED SYSTEM (5 PR PENDING)

### PR-9: Deteksi embed vs video ← **NEXT!**
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
- **File:** `embed_parser.py`
- **Status:** ⏸️ Belum difix

### PR-14: Auto-match favicon per platform
- **Prioritas:** 🟢 MINOR
- **File:** `templates/gallery.html`, `embed_parser.py`
- **Status:** ⏸️ Belum difix

---

## ⚙️ GRUP C — SETTING (5 PR PENDING)

### PR-16: Menu Favicon (A+B Hybrid) — 🟢 FINAL
- **Status:** ⏸️ Belum dikerjain

### PR-17: Bundle Pengaturan Galeri — 🟢 MINOR
- **Status:** ⏸️ Belum difix

### PR-18: Preview live terminal — 🟢 MINOR
- **Status:** ⏸️ Belum difix

### PR-19: Export/Import config — 🟢 MINOR
- **Status:** 🟡 KESENTUH rebranding

### PR-20: Per-account setting — 🟢 MINOR
- **Status:** ⏸️ Belum difix

---

## ✨ GRUP D — VISUAL POLISH (6 PR PENDING)

### PR-21: Animasi judul Glow Pulse — 🟢 FINAL
- **Status:** ⏸️ Belum dikerjain

### PR-22: Stagger fade-in card — 🟢 MINOR
- **Status:** ⏸️ Belum difix

### PR-23: Hover effect card — 🟢 MINOR
- **Status:** ⏸️ Belum difix

### PR-24: Lightbox transition — 🟢 MINOR
- **Status:** ⏸️ Belum difix

### PR-25: Loading skeleton — 🟢 MINOR
- **Status:** ⏸️ Belum difix

### PR-26: Scroll reveal — 🟢 MINOR
- **Status:** ⏸️ Belum difix

---

## 🌊 GRUP E — UX & PERF (2 PR PENDING)

### PR-27: Moss particle bg — ⚠️ SKIP
- **Status:** ⚠️ SKIP (keputusan final)

### PR-28: Smooth navigation paket — 🟢 FINAL
- **Status:** ⏸️ Belum dikerjain

### PR-29: Support 120Hz optional — 🟢 FINAL
- **Status:** ⏸️ Belum dikerjain

---

## 🧠 GRUP F — ADVANCED (8 PR PENDING)

### PR-30: Auto grouping wajah — 🔒 LOCKED
- **Status:** 🔒 LOCKED OPTIONAL

### PR-31: Auto-tag EXIF — 🟢 PILIH
- **Status:** ⏸️ Belum difix

### PR-32: Duplicate detection — 🟢 PILIH
- **Status:** ⏸️ Belum difix

### PR-35: Timeline view — 🟢 PILIH
- **Status:** ⏸️ Belum difix

### PR-38: Dark/Light mode toggle — 🟢 PILIH
- **Status:** ⏸️ Belum difix

### PR-40: Thumbnail generation — 🟡 PILIH ⭐🥇
- **Status:** 🟡 KESENTUH rebranding

### PR-43: Pagination / infinite scroll — 🟡 PILIH ⭐🥈
- **Status:** ⏸️ Belum difix

### PR-47: PWA install as app — 🟢 PILIH
- **Status:** ⏸️ Belum difix

---

## 🌐 GRUP G — INFRA (1 PR PENDING)

### PR-51: Custom domain support — 🟢 BARU
- **Status:** 🟡 KESENTUH rebranding

---

## 🎬 SIDE PROJECT (1 — ✅ SELESAI!)

### PR-PORTFOLIO: Cinematic Resume Portfolio — ✅ SELESAI v1.0
- **Repo:** `https://github.com/nexterade/nexterade.github.io`
- **Live:** **https://nexterade.github.io**
- **Status:** ✅ **SELESAI v1.0**

**Task yang belum (follow-up):**
- ⏸️ Update README LUMOSS — isi field Website
- ⏸️ Update README portfolio (masih template Amir)

---

## 📊 RINGKASAN LENGKAP

| Kategori | Jumlah |
|----------|--------|
| **TOTAL PR (LUMOSS)** | **38 PR** |
| ✅ SELESAI | **9** (PR-1, PR-2, PR-3, PR-4, PR-5, PR-6, PR-7, PR-8, PR-12) |
| ⏸️ PENDING | **29** |
| 🔴 KRITIS | 0 (semua selesai) |
| 🟡 MEDIUM | 4 (PR-9, PR-10, PR-16, PR-40) |
| 🟢 MINOR | 19 |
| ⚠️ SKIP | 1 (PR-27) |
| 🔒 LOCKED | 1 (PR-30) |
| 🟢 FINAL | 4 (PR-16, PR-21, PR-28, PR-29) |
| 🟡 KESENTUH rebranding | 4 (PR-19, PR-40, PR-51) |
| **SIDE PROJECT** | **1 (PR-PORTFOLIO)** ✅ |

---

## 🎯 URUTAN PENGERJAAN (REKOMENDASI)

### **FASE 4A — MEDIUM (4 PR)** ⭐ **PRIORITAS**
1. **PR-9** (Deteksi embed vs video) — 🟡 MEDIUM ← **NEXT!**
2. **PR-10** (Info panel "0 B") — 🟡 MEDIUM
3. **PR-16** (Menu Favicon) — 🟢 FINAL
4. **PR-40** (Thumbnail generation) — 🟡 PILIH ⭐🥇

### **FASE 4B — FINAL (3 PR)**
5. PR-21 (Animasi Glow Pulse)
6. PR-28 (Smooth navigation)
7. PR-29 (Support 120Hz)

### **FASE 4C — PILIH (1 PR prioritas)**
8. PR-43 (Pagination) ⭐🥈

### **FASE 4D — MINOR (19 PR)**
9. PR-11, PR-13, PR-14, PR-17, PR-18, PR-19, PR-20, PR-22, PR-23,
   PR-24, PR-25, PR-26, PR-31, PR-32, PR-35, PR-38, PR-47, PR-51
   + PR-27 (SKIP), PR-30 (LOCKED)

---

## 🎯 NEXT STEP

**PR-9** — Deteksi embed vs video (embed_parser.py)
- Butuh: `embed_parser.py` (udah ada)
- Risiko: rendah (cuma improve detection logic)
- Estimasi: 1 sesi

---

**END OF BACKLOG v7.2.12**