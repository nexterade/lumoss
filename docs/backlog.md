# 📋 BACKLOG — LUMOSS v7.2.2

**Update terakhir:** 2026-09-16
**Total issues:** 38 PR (FASE 5)
**Status:** ⏸️ BACKLOG (belum disentuh)

📎 **Checkpoint terkait:** `docs/checkpoint.txt`
📎 **State terkait:** `docs/state.txt`

---

## 🎯 RINGKASAN

| Kategori | Jumlah |
|----------|--------|
| 🔴 KRITIS | 2 |
| 🟡 MEDIUM | 5 |
| 🟢 MINOR | 24 |
| ⚠️ SKIP | 1 |
| 🔒 LOCKED | 1 |
| 🟢 FINAL | 4 |
| 🟡 KESENTUH | 4 |

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
- **Deskripsi:** File about.html di templates/ udah gak dipake
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
- **File:** `templates/gallery.html`, `embed_parser.py`
- **Status:** ⏸️ Belum difix

### PR-15: Auto-hide header on scroll
- **Prioritas:** 🟢 MINOR
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum difix

### PR-16: Menu Favicon (A+B Hybrid)
- **Prioritas:** 🟢 FINAL
- **File:** `menu.py`, `config_manager.py`
- **Status:** ⏸️ Belum dikerjain

### PR-17: Bundle Pengaturan Galeri
- **Prioritas:** 🟢 MINOR
- **File:** `menu.py`
- **Status:** ⏸️ Belum difix

### PR-18: Preview live terminal
- **Prioritas:** 🟢 MINOR
- **File:** `menu.py`
- **Status:** ⏸️ Belum difix

### PR-19: Export/Import config
- **Prioritas:** 🟢 MINOR
- **File:** `config_manager.py`
- **Status:** 🟡 KESENTUH rebranding

### PR-20: Per-account setting
- **Prioritas:** 🟢 MINOR
- **File:** `config_manager.py`
- **Status:** ⏸️ Belum difix

---

## ✨ GRUP D — VISUAL POLISH (6 PR)

### PR-21: Animasi judul Glow Pulse
- **Prioritas:** 🟢 FINAL
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum dikerjain

### PR-22: Stagger fade-in card
- **Prioritas:** 🟢 MINOR
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum difix

### PR-23: Hover effect card
- **Prioritas:** 🟢 MINOR
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum difix

### PR-24: Lightbox transition
- **Prioritas:** 🟢 MINOR
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum difix

### PR-25: Loading skeleton
- **Prioritas:** 🟢 MINOR
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum difix

### PR-26: Scroll reveal
- **Prioritas:** 🟢 MINOR
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum difix

---

## 🌊 GRUP E — UX & PERF (3 PR)

### PR-27: Moss particle bg
- **Prioritas:** ⚠️ SKIP
- **Deskripsi:** Background partikel moss (dibatalin — terlalu berat)
- **Status:** ⚠️ SKIP (keputusan final)

### PR-28: Smooth navigation paket
- **Prioritas:** 🟢 FINAL
- **File:** `templates/gallery.html`
- **Status:** ⏸️ Belum dikerjain

### PR-29: Support 120Hz optional
- **Prioritas:**

### PR-30: Setup Cinematic Resume Portfolio (GitHub Pages)
- **Prioritas:** 🟡 MEDIUM
- **Deskripsi:** Deploy Cinematic Resume sebagai portfolio pribadi di nexterade.github.io. Base udah di-clone & jalan lokal, tinggal:
  - Isi `data/resumeContent.js` dengan data pribadi (nexterade, LUMOSS, dll)
  - Ganti styling (moss green theme + font)
  - Fix hydration error di `app/layout.tsx`
  - Fix GSAP target error (`.project-stage-shell`, `.timeline-mobile-card`)
  - Deploy ke GitHub Pages
- **File:** `~/nexterade.github.io/` (repo terpisah)
- **Status:** ⏸️ PENDING
- **Catatan:** Base di `data/resumeContent.js` & `tailwind.config.js`. Rencana: Opsi B (Data + Styling).