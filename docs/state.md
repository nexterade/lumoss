================================================================================
                    LUMOSS PROJECT — STATE
                    Progress, Struktur, Status Fase
================================================================================

Terakhir update  : 2026-09-17
Versi state      : v7.2.13
Format           : Markdown (.md)
Tipe             : DYNAMIC (update tiap sesi)

📎 FILE TERKAIT:
  · Checkpoint  : docs/checkpoint.md        ← kepribadian + aturan (constant)
  · Backlog     : docs/backlog.md           ← detail 38 PR + 1 side project (dynamic)

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
Status       : 🎨 UI POLISH (v7.2.11) + 📝 DOCS (v7.2.13)

TOOLKIT (SELESAI):
  Lokasi     : /storage/emulated/0/Project/auto-release-wizard/
  Fungsi     : Rilis project + 12 tools bantu (universal)
  Status     : ✅ 100% DONE (13 file)

SIDE PROJECT (SELESAI):
  Nama       : Cinematic Resume Portfolio
  Repo       : https://github.com/nexterade/nexterade.github.io
  Lokal      : ~/nexterade.github.io/
  Live       : https://nexterade.github.io
  Status     : ✅ SELESAI v1.0 (Live!)
  Detail     : Lihat section 8b — Side Project

================================================================================
2. STATUS FASE
================================================================================

✅ FASE 1   — REBRANDING (SELESAI, 8/8 step)
✅ FASE 1.5 — UI POLISH (SELESAI, v7.2.3 → v7.2.6)
✅ FASE 2   — GIT INIT (SELESAI, v7.2.7)
✅ FASE 2.5 — DOKUMENTASI (SELESAI, v7.2.9)
✅ FASE 3   — EMBED FIX (SELESAI, v7.2.11)
✅ SIDE PROJECT — PORTFOLIO (SELESAI, v1.0)
⏸️ FASE 4   — FASE 5 PR (38 PR — 4 selesai, 34 pending)
⏸️ FASE 5   — BACKLOG v7.3.0 (PENDING)

================================================================================
3. GIT INFO
================================================================================

Repo URL     : https://github.com/nexterade/lumoss
Protocol     : HTTPS
Branch       : main
Author       : nexter <nexterade@gmail.com>
Remote       : origin (https://github.com/nexterade/lumoss.git)
Status       : ✅ Up to date with origin/main

Commit History (terbaru):
  · ac6003e — docs(checkpoint): update v1.6 — rule 4.14 (release setiap perubahan)
  · 80eef54 — docs(checkpoint): update v1.4 — 5 rule baru dari sesi v7.2.11
  · 682c0d5 — feat(PR-7, PR-8): YouTube + IG embed + aspect ratio + auto-hide UI
  · 34334a6 — docs(backlog): update v7.2.12 — 4 PR selesai
  · eac3ea4 — docs(state): update v7.2.12 — FASE 3 (Embed Fix) selesai
  · ffc71bc — docs(backlog): merge PR-FASE5 into backlog.md — v7.2.8
  · 58819eb — chore: initial commit — LUMOSS v7.2.6

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
Ukuran repo  : ~145 KiB

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
    │   ├── gallery.html             ✅ v7.2.11
    │   └── manager.html
    ├── docs/                        ✅ Dokumentasi
    │   ├── checkpoint.md            ← CONSTANT (v1.6)
    │   ├── state.md                 ← DYNAMIC (file ini)
    │   ├── backlog.md               ← DYNAMIC (38 PR + 1 side)
    │   └── PR-PORTOFOLIO.md         ← Side project
    ├── backup/                      ✅ Backup
    │
    ├── account_manager.py           ✅ v7.2.6
    ├── config_manager.py            ✅ v7.2.6
    ├── embed_parser.py              ✅ v7.2.11 (aspect ratio)
    ├── global_config.json           ✅ v7.2.6
    ├── html_builder.py              ✅ v7.2.6
    ├── lumoss.py                    ✅ v7.2.6
    ├── media_processor.py           ✅ v7.2.6
    ├── menu.py                      ✅ v7.2.6
    ├── menu_account.py              ✅ v7.2.6
    ├── menu_embed.py                ✅ v7.2.6
    ├── menu_tools.py                ✅ v7.2.6
    ├── README.md                    ✅ v7.2.9
    ├── requirements.txt
    ├── tools.py                     ✅ v7.2.6
    ├── ui_helpers.py                ✅ v7.2.6
    └── uploader.py                  ✅ v7.2.9

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
6. FITUR v7.2.2 (BASE)
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
6a. FITUR v7.2.11 (EMBED FIX) — SELESAI
================================================================================

🎯 PR-7 — YouTube Error 153 FIXED:
  ✅ URL embed tambah parameter:
     · origin={ORIGIN} — dynamic dari window.location.origin
     · enablejsapi=1 — kontrol via JS
     · rel=0 — gak nampilin rekomendasi
     · modestbranding=1 — minimal branding
     · playsinline=1 — support inline play
  ✅ Fallback UI kalo iframe gagal

🎯 PR-8 — Instagram Embed FIXED:
  ✅ URL embed: /embed/captioned/ (tambah captioned)
  ✅ Caption + media muncul, bukan cuma header

🎯 DYNAMIC ASPECT RATIO (BARU):
  ✅ YouTube watch → 16/9 (landscape)
  ✅ YouTube Shorts → 9/16 (portrait)
  ✅ Instagram Post → 4/5 (portrait)
  ✅ Instagram Reel/TV → 9/16 (portrait)
  ✅ TikTok → 9/16 (portrait)
  ✅ Vimeo → 16/9 (landscape)
  ✅ Twitter/X → 16/9 (landscape)
  ✅ Facebook → 16/9 (landscape)

🎯 AUTO-HIDE UI (BARU):
  ✅ Header & footer auto-hide setelah 3 detik
  ✅ Opacity 0.15 pas non-aktif
  ✅ Opacity 1 pas hover/active/show
  ✅ Tap area atas & bawah iframe → show UI
  ✅ Rotate/resize → reset timer

🎯 GALLERY HEADER AUTO-HIDE (BARU):
  ✅ Scroll ke bawah (>10px) → header hide
  ✅ Auto-show setelah 3 detik
  ✅ Scroll ke atas → header show

🎯 SMART HISTORY (BARU):
  ✅ pushState pas buka lightbox
  ✅ replaceState pas pindah item (gak numpuk)
  ✅ popstate handler — tombol back nutup lightbox
  ✅ 100dvh — handle address bar mobile

================================================================================
6b. UI POLISH v7.2.3 → v7.2.6 (SELESAI)
================================================================================

🎨 UI OVERHAUL (v7.2.3):
  ✅ Banner LUMOSS — border ngikutin lebar ASCII art
  ✅ layout_widths() — full-width otomatis dari term_width()
  ✅ render_full_box() — 1 box full-width
  ✅ render_two_col_box() — 2 kolom 1 border utuh
  ✅ render_group_box() — grup menu border utuh
  ✅ Emoji di menu → Unicode symbol

🎨 MERGED BOXES (v7.2.4):
  ✅ render_merged_box() — 1 box, multiple section
  ✅ render_merged_group() — 1 box, multiple grup menu

🎨 VERTICAL LAYOUT (v7.2.5):
  ✅ render_vertical_box() — section stack atas-bawah
  ✅ render_vertical_group() — grup menu stack atas-bawah
  ✅ "AKUN & RINGKASAN" + "MENU UTAMA"

🎨 EMOJI AUTO-CONVERT (v7.2.6):
  ✅ EMOJI_TO_UNICODE — mapping ~150 emoji
  ✅ convert_emoji() + strip_emoji()
  ✅ 🌿 (LUMOSS_SYMBOL) — KEEP, gak di-convert

================================================================================
7. BUG DITEMUKAN & DIFIX
================================================================================

BUG #1-4 (v7.2.0): ask(), auto-detect, TODO, f-string
BUG #5-6 (v7.2.2): Onboarding _selected ilang, toggle salah
BUG #7 (v7.2.2): .thumbnails ke-scan
BUG #8 (v7.2.11): YouTube error 153 → FIXED
BUG #9 (v7.2.11): Instagram cuma header → FIXED
BUG #10 (v7.2.11): Iframe gak full (aspect ratio) → FIXED
BUG #11 (v7.2.11): Tombol back exit → FIXED
BUG #12 (v7.2.11): Address bar kepotong (Quetta) → FIXED

SEMUA FIXED ✅

================================================================================
8. ROADMAP
================================================================================

✅ FASE 1   — REBRANDING (SELESAI)
✅ FASE 1.5 — UI POLISH v7.2.3 → v7.2.6 (SELESAI)
✅ FASE 2   — GIT INIT (SELESAI v7.2.7)
✅ FASE 2.5 — DOKUMENTASI (SELESAI v7.2.9)
✅ FASE 3   — EMBED FIX (SELESAI v7.2.11)
✅ SIDE PROJECT — PORTFOLIO (SELESAI v1.0)
⏸️ FASE 4   — FASE 5 PR (38 PR)
⏸️ FASE 5   — BACKLOG v7.3.0 (13 saran)

================================================================================
8b. SIDE PROJECT — CINEMATIC RESUME PORTFOLIO (SELESAI!)
================================================================================

Status       : ✅ SELESAI v1.0 — Live!
Repo         : https://github.com/nexterade/nexterade.github.io
Lokal        : ~/nexterade.github.io/
Live URL     : https://nexterade.github.io
Base         : Cinematic Resume (Next.js 16.3.5, Webpack)
Prioritas    : 🟡 MEDIUM → ✅ DONE

SETUP YANG UDAH KELAR:
  ✅ Fork repo Cinematic Resume
  ✅ Clone ke Termux (~/nexterade.github.io/)
  ✅ Pindah ke home — fix symlink error (FAT32)
  ✅ npm install — 96 packages, 0 vulnerabilities
  ✅ Preview lokal: npm run dev -- --webpack
  ✅ Personalisasi data (resumeContent.js) — nexterade
  ✅ Personalisasi GitHub snapshot (githubSnapshot.json)
  ✅ Fix null guards (HeroSection, LoaderOverlay)
  ✅ Fix favicon (app/icon.svg — moss circle)
  ✅ Fix Footer.js (repoUrl nexterade)
  ✅ Fix next.config.mjs (basePath kosong)
  ✅ Reset git history (fresh start)
  ✅ Deploy via GitHub Actions
  ✅ Live di https://nexterade.github.io

TASK YANG BELUM:
  ⏸️ Update README LUMOSS — isi field Website
  ⏸️ Update README portfolio (masih template Amir)

CATATAN TEKNIS:
  · Next.js 16.3.5 — Turbopack GAK SUPPORT Android/arm64
  · Dev server WAJIB pake Webpack: npm run dev -- --webpack
  · Build WAJIB pake Webpack: npm run build -- --webpack
  · basePath HARUS kosong (User Site, bukan Project Site)
  · GitHub Actions: .github/workflows/deploy-pages.yml

================================================================================
9. CATATAN PENTING
================================================================================

  · Akun real: Cantika (bukan dummy)
  · Akun dummy: Akun Utama (bisa dihapus kalau perlu)
  · Git UDAH di-init — repo: github.com/nexterade/lumoss
  · Branch: main | Protocol: HTTPS | Author: nexter
  · Commit terbaru: ac6003e (checkpoint v1.6)
  · PR FASE 5 detail: docs/backlog.md (39 item)
  · Multi-folder media (media_dirs array)
  · Onboarding WAJIB pilih folder
  · Struktur: accounts/ + output/ + cache/
  · Backup folder: /storage/emulated/0/Project/backup/
  · UI polished ke v7.2.6 (vertical layout + emoji auto-convert)
  · Embed fix v7.2.11 (YouTube, IG, aspect ratio, auto-hide UI)
  · Submenu pake Unicode symbol (bukan emoji)
  · 🌿 = simbol utama Lumoss (gak di-convert)
  · Side project Cinematic Resume — SELESAI v1.0 (Live!)
  · Portfolio URL: https://nexterade.github.io
  · ⛔ ATURAN KERAS: JANGAN kasih command Termux dengan tag #
    (lihat checkpoint.md section 5)
  · 📌 6 rule baru dari sesi v7.2.11 (checkpoint v1.6)

================================================================================
10. TEST REPORT (2026-09-17)
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
✅ TEST 10 — Merge PR-FASE5 → backlog.md (39 item)
✅ TEST 11 — Update README (rebranding LUMOSS)
✅ TEST 12 — YouTube embed (watch, shorts) — WORKS
✅ TEST 13 — Instagram embed (post, reel) — WORKS
✅ TEST 14 — TikTok embed — WORKS
✅ TEST 15 — Auto-hide UI + zona tap — WORKS
✅ TEST 16 — Gallery header auto-hide — WORKS
✅ TEST 17 — Tombol back (smart history) — WORKS
✅ TEST 18 — Test di localhost (bukan file://) — WORKS
✅ TEST 19 — Portfolio live (https://nexterade.github.io) — WORKS

🎯 SEMUA FITUR JALAN SEMPURNA

================================================================================
11. UI/UX PATTERN v7.2.11 (REUSE)
================================================================================

Pattern yang dipake di v7.2.11 — bisa di-reuse di project lain:

1. DYNAMIC ASPECT RATIO
   · Deteksi dari URL pattern (bukan fetch)
   · Set CSS variable --embed-aspect
   · Class data-orientation="portrait"/"landscape"

2. AUTO-HIDE UI
   · Header/footer opacity 0.15 default
   · Class .show → opacity 1
   · Timer 3 detik auto-hide
   · Trigger: tap, hover, rotate, resize

3. ZONA TAP (buat iframe full)
   · .lb-tap-zone-top (70px dari atas)
   · .lb-tap-zone-bottom (110px dari bawah)
   · Transparan, z-index di atas iframe
   · Tap → show UI

4. SMART HISTORY
   · pushState pas buka (1 entry)
   · replaceState pas pindah item (gak numpuk)
   · popstate handler
   · closeLightbox → history.back()

5. FALLBACK UI
   · Timeout 8 detik → tampilin fallback
   · Link "Buka di platform"
   · Tombol "Learn more"

================================================================================
12. FILE TRACKED BY GIT (24 files)
================================================================================

docs/
  · backlog.md
  · checkpoint.md
  · state.md
  · PR-PORTOFOLIO.md

templates/
  · gallery.html
  · manager.html

accounts/
  · active.json

Root:
  · .gitignore
  · README.md
  · account_manager.py
  · config_manager.py
  · embed_parser.py
  · global_config.json
  · html_builder.py
  · lumoss.py
  · media_processor.py
  · menu.py
  · menu_account.py
  · menu_embed.py
  · menu_tools.py
  · requirements.txt
  · tools.py
  · ui_helpers.py
  · uploader.py

================================================================================
                    END OF STATE v7.2.13
================================================================================