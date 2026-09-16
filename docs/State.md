================================================================================
                    LUMOSS PROJECT — STATE
                    Progress, Struktur, Status Fase
================================================================================

Terakhir update  : 2026-09-16
Versi state      : v7.2.8
Format           : Markdown (.md)
Tipe             : DYNAMIC (update tiap sesi)

📎 FILE TERKAIT:
  · Checkpoint  : docs/checkpoint.md        ← kepribadian + aturan (constant)
  · Backlog     : docs/backlog.md           ← detail 38 PR (dynamic)

================================================================================
1. STATUS PROJECT
================================================================================

Project      : lumoss (ex amuv7)
Nama lama    : amuv7 (Automated Media Uploader v7)
Lokasi       : /storage/emulated/0/Project/lumoss/
Environment  : Python 3.14+ di Termux Android
Tema         : Luminous Moss (#2BEE34)
Logo         : 🌿
Tagline      : "Media Garden, in bloom"
Author       : @nexterade
License      : MIT
Status       : 🎨 UI POLISH (v7.2.6) + 🔧 GIT INIT (v7.2.7)

TOOLKIT (SELESAI):
  Lokasi     : /storage/emulated/0/Project/auto-release-wizard/
  Fungsi     : Rilis project + 12 tools bantu (universal)
  Status     : ✅ 100% DONE (13 file)

SIDE PROJECT (PENDING):
  Nama       : Cinematic Resume Portfolio
  Repo       : https://github.com/nexterade/nexterade.github.io
  Lokal      : ~/nexterade.github.io/
  Status     : ⏸️ PENDING (base jalan, rombak belum)
  Detail     : Lihat section 8b — Side Project

================================================================================
2. STATUS FASE
================================================================================

✅ FASE 1   — REBRANDING (SELESAI, 8/8 step)
✅ FASE 1.5 — UI POLISH (SELESAI, v7.2.3 → v7.2.6)
✅ FASE 2   — GIT INIT (SELESAI, v7.2.7)
⏸️ FASE 3   — HYBRID MENU (v7.2.7)        ← NEXT!
⏸️ FASE 4   — FASE 5 PR (38 PR, PENDING)
⏸️ FASE 5   — BACKLOG v7.3.0 (PENDING)

SIDE PROJECT (PENDING):
⏸️ PORTFOLIO — CINEMATIC RESUME (lihat section 8b)

================================================================================
3. GIT INFO
================================================================================

Repo URL     : https://github.com/nexterade/lumoss
Protocol     : HTTPS
Branch       : main
Author       : nexter <nexterade@gmail.com>
Commit Awal  : 58819eb — "chore: initial commit — LUMOSS v7.2.6"
Remote       : origin (https://github.com/nexterade/lumoss.git)
Status       : ✅ Up to date with origin/main

.gitignore:
  · accounts/*/ (kecuali active.json)
  · output/
  · cache/
  · backup/
  · __pycache__/, *.pyc
  · venv/, .venv/, env/
  · *.log, *.tmp, *.bak
  · *.zip, *.tar.gz, *.rar
  · fix_emoji.py
  · templates/about.html

File tracked : 24 files (lihat `git ls-files`)
Ukuran repo  : 132 KiB

================================================================================
4. STRUKTUR PROJECT
================================================================================

Path: /storage/emulated/0/Project/lumoss/

  lumoss/
    ├── accounts/                    ✅ Config + active.json
    │   ├── active.json
    │   ├── akun_utama/
    │   └── cantika/                 ✅ AKUN REAL
    ├── output/                      ✅ Hasil generate
    │   ├── akun_utama/
    │   └── cantika/
    │       ├── index.html
    │       └── manager.html
    ├── cache/                       ✅ Cache & state
    │   ├── akun_utama/
    │   └── cantika/
    ├── templates/                   ✅ Template HTML
    │   ├── gallery.html
    │   └── manager.html
    ├── docs/                        ✅ Dokumentasi
    │   ├── checkpoint.md            ← CONSTANT
    │   ├── state.md                 ← DYNAMIC (file ini)
    │   └── backlog.md               ← DYNAMIC
    ├── backup/                      ✅ Backup
    │
    ├── account_manager.py           ✅ v7.2.6
    ├── config_manager.py            ✅ v7.2.6
    ├── embed_parser.py              ✅ v7.2.6
    ├── global_config.json           ✅ v7.2.6
    ├── html_builder.py              ✅ v7.2.6
    ├── lumoss.py                    ✅ v7.2.6
    ├── media_processor.py           ✅ v7.2.6
    ├── menu.py                      ✅ v7.2.6
    ├── menu_account.py              ✅ v7.2.6
    ├── menu_embed.py                ✅ v7.2.6
    ├── menu_tools.py                ✅ v7.2.6
    ├── README.md
    ├── requirements.txt
    ├── tools.py                     ✅ v7.2.6
    ├── ui_helpers.py                ✅ v7.2.6
    └── uploader.py                  ✅ v7.2.6

================================================================================
5. STRUKTUR DATA
================================================================================

accounts/active.json             — registry akun
accounts/<slug>/config.json      — config akun (media_dirs array)
output/<slug>/index.html         — galeri
output/<slug>/manager.html       — manager
output/<slug>/embed.txt          — list URL embed
cache/<slug>/uploads_cache.json  — cache upload
cache/<slug>/deleted.json        — blacklist

Cache key format:
  {source_label}/{rel_path}
  Contoh: "Nagram/VID_20260718_154608_914.mp4"

================================================================================
6. FITUR v7.2.2
================================================================================

1. STRUKTUR FOLDER TERPISAH: accounts/ + output/ + cache/
2. MULTI-FOLDER MEDIA: pilih beberapa folder
3. ONBOARDING WAJIB PILIH FOLDER
4. KELOLA FOLDER MEDIA (menu 7 → 5)
5. SKIP FOLDER & FILE SAMPAH (.thumbnails, .cache, Android, dll)
6. CACHE KEY UNIK: {source_label}/{rel_path}
7. SHARED ONBOARDING HELPERS (di account_manager.py)
8. BANNER LUMOSS: "Media Garden, in bloom"

================================================================================
6a. TEST REPORT (2026-09-16)
================================================================================

✅ TEST 1  — Banner LUMOSS v7.2.2
✅ TEST 2  — Onboarding (7 folder, .thumbnails HILANG)
✅ TEST 3  — Bikin akun Cantika
✅ TEST 4  — Upload Gate Dashboard
✅ TEST 5  — Eksekusi Upload (2 file, 14.4 MB, 55s)
✅ TEST 6  — Generate HTML (index.html + manager.html)
✅ TEST 7  — Path display (accounts/output/cache)
✅ TEST 8  — ConnectionError retry — SUKSES
✅ TEST 9  — Git Init + Push ke GitHub
              (repo: nexterade/lumoss, branch: main)

🎯 SEMUA FITUR JALAN SEMPURNA

================================================================================
6b. UI POLISH v7.2.3 → v7.2.6
================================================================================

🎨 UI OVERHAUL (v7.2.3):
  ✅ Banner LUMOSS — border ngikutin lebar ASCII art (gak hardcoded 41)
  ✅ layout_widths() — full-width otomatis dari term_width()
  ✅ render_full_box() — 1 box full-width
  ✅ render_two_col_box() — 2 kolom 1 border utuh
  ✅ render_group_box() — grup menu border utuh
  ✅ Emoji di menu → Unicode symbol (◉ ▸ ◆ ▶ ↻ ▣ ◐ ❖ ⚒ ✎ ◈ ℹ ? ✗)

🎨 MERGED BOXES (v7.2.4):
  ✅ render_merged_box() — 1 box, multiple section (horizontal)
  ✅ render_merged_group() — 1 box, multiple grup menu (horizontal)

🎨 VERTICAL LAYOUT (v7.2.5):
  ✅ render_vertical_box() — section stack atas-bawah (Opsi C)
  ✅ render_vertical_group() — grup menu stack atas-bawah
  ✅ "AKUN & RINGKASAN" — sub-judul AKUN AKTIF / RINGKASAN
  ✅ "MENU UTAMA" — sub-judul AKSI UTAMA / PENGATURAN

🎨 EMOJI AUTO-CONVERT (v7.2.6):
  ✅ EMOJI_TO_UNICODE — mapping ~150 emoji → Unicode symbol
  ✅ convert_emoji() — auto-convert pas input (nama, judul)
  ✅ strip_emoji() — strip sisa emoji gak dikenal
  ✅ 🌿 (LUMOSS_SYMBOL) — KEEP, gak di-convert (simbol Lumoss)
  ✅ Safety net di render — double convert kalo user edit config manual

📁 FILE YANG DIUBAH:
  • ui_helpers.py  → +4 helper layout + emoji converter
  • menu.py        → +convert_emoji di input flow

📁 FILE YANG DIUBAH (bulk via fix_emoji.py):
  • menu_account.py  → emoji → Unicode symbol
  • menu_tools.py    → emoji → Unicode symbol
  • menu_embed.py    → emoji → Unicode symbol

================================================================================
7. BUG DITEMUKAN & DIFIX
================================================================================

BUG #1-4 (v7.2.0): ask(), auto-detect, TODO, f-string
BUG #5-6 (v7.2.2): Onboarding _selected ilang, toggle salah
BUG #7 (v7.2.2): .thumbnails ke-scan

SEMUA FIXED ✅

================================================================================
8. ROADMAP
================================================================================

✅ FASE 1   — REBRANDING (SELESAI)
✅ FASE 1.5 — UI POLISH v7.2.3 → v7.2.6 (SELESAI)
✅ FASE 2   — GIT INIT (SELESAI v7.2.7)
⏸️ FASE 3   — HYBRID MENU (v7.2.7)        ← NEXT
⏸️ FASE 4   — FASE 5 PR (38 PR)
⏸️ FASE 5   — BACKLOG v7.3.0 (13 saran)

================================================================================
8b. SIDE PROJECT — CINEMATIC RESUME PORTFOLIO
================================================================================

Status       : ⏸️ PENDING (base jalan, rombak belum)
Repo         : https://github.com/nexterade/nexterade.github.io
Lokal        : ~/nexterade.github.io/
Base         : Cinematic Resume (Next.js 16.3.5, Webpack)
Prioritas    : 🟡 MEDIUM

SETUP YANG UDAH KELAR:
  ✅ Fork repo Cinematic Resume
  ✅ Clone ke Termux (~/nexterade.github.io/)
  ✅ Pindah ke home — fix symlink error (FAT32)
  ✅ npm install — 96 packages, 0 vulnerabilities
  ✅ Preview lokal jalan: npm run dev -- --webpack

YANG BELUM (TASK ROMBAK):
  ⏸️ Isi data/resumeContent.js dengan data pribadi
      (nexterade, LUMOSS, Auto Release Wizard, dll)
  ⏸️ Ganti styling di tailwind.config.js — moss green theme
  ⏸️ Fix hydration error di app/layout.tsx (font variable)
  ⏸️ Fix GSAP target error (.project-stage-shell, .timeline-mobile-card)
  ⏸️ Deploy ke GitHub Pages
  ⏸️ Update README LUMOSS — isi field Website

CATATAN TEKNIS:
  · Next.js 16.3.5 — Turbopack GAK SUPPORT Android/arm64
  · Dev server WAJIB pake Webpack: npm run dev -- --webpack
  · Hydration error karena font variable — bukan fatal
  · GSAP error karena section kosong — fix setelah isi data
  · Struktur: app/, components/, data/, hooks/, lib/, scripts/

================================================================================
9. CATATAN PENTING
================================================================================

  · Akun real: Cantika (bukan dummy)
  · Akun dummy: Akun Utama (bisa dihapus kalau perlu)
  · Git UDAH di-init — repo: github.com/nexterade/lumoss
  · Branch: main | Protocol: HTTPS | Author: nexter
  · Commit awal: 58819eb (initial commit v7.2.6)
  · PR FASE 5 detail: docs/backlog.md
  · Multi-folder media (media_dirs array)
  · Onboarding WAJIB pilih folder
  · Struktur: accounts/ + output/ + cache/
  · Backup folder: /storage/emulated/0/Project/backup/
  · UI polished ke v7.2.6 (vertical layout + emoji auto-convert)
  · Submenu pake Unicode symbol (bukan emoji)
  · 🌿 = simbol utama Lumoss (gak di-convert)
  · Side project Cinematic Resume — PENDING (lihat 8b)
  · ⛔ ATURAN KERAS: JANGAN kasih command Termux dengan tag #
    (lihat checkpoint.md section 5)

================================================================================
                    END OF STATE v7.2.8
================================================================================