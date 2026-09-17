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
Status       : 🎨 UI POLISH (v7.2.11) + 📝 DOCS (v7.2.13) + ✅ FIX 12 PR + 🎁 NEW 5 FITUR

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
✅ FASE 3.5 — PLATFORM ICON + AUTO-TAG + PR-9/10/11 (SELESAI, v7.2.13)
🔥 FASE 4   — FASE 5 PR (38 PR — 12 selesai, 26 pending) ← ONGOING!
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
  · 8cea7dc — feat(v7.2.13): PR-9 + PR-10 + PR-11 + Platform Icon + Auto-Tag
  · 96fcf4f — chore: cleanup backup files + update .gitignore
  · 0625e69 — feat(PR-1,PR-3,PR-4,PR-5,PR-6): tree view + GITHUB_REPO fix + tools cleanup
  · ac6003e — docs(checkpoint): update v1.6 — rule 4.14 (release setiap perubahan)

Release Terbaru:
  · v7.2.13 — 🌿 LUMOSS v7.2.13 — Platform Icons + Auto-Tag
    https://github.com/nexterade/lumoss/releases/tag/v7.2.13
  · v7.2.12 — Tree View + GITHUB_REPO Fix
  · v7.2.11 — Embed Fix
  · v7.2.9  — Dokumentasi

.gitignore:
  · accounts/*/ (kecuali active.json)
  · output/
  · cache/
  · backup/
  · __pycache__/, *.pyc
  · venv/, .venv/, env/
  · *.log, *.tmp, *.bak, *.bak_*
  · *.zip, *.tar.gz, *.rar
  · setup-*.sh, *-pointless-*
  · fix_emoji.py
  · templates/about.html

File tracked : 24 files (lihat `git ls-files`)
Ukuran repo  : ~150 KiB

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
    │   ├── gallery.html             ✅ v7.2.13
    │   ├── manager.html
    │   └── platform-icons.js        ✅ v7.2.13 (BARU!)
    ├── docs/                        ✅ Dokumentasi
    │   ├── checkpoint.md            ← CONSTANT (v1.8)
    │   ├── state.md                 ← DYNAMIC (file ini)
    │   ├── backlog.md               ← DYNAMIC (38 PR + 1 side)
    │   └── PR-PORTOFOLIO.md         ← Side project
    ├── backup/                      ✅ Backup
    │
    ├── account_manager.py           ✅ v7.2.2
    ├── config_manager.py            ✅ v7.2.2
    ├── embed_parser.py              ✅ v7.2.13 (auto-tag + detection)
    ├── global_config.json           ✅ v7.2.13
    ├── html_builder.py              ✅ v7.2.13 (platform-icons)
    ├── lumoss.py                    ✅ v7.2.12
    ├── media_processor.py           ✅ v7.2.0
    ├── menu.py                      ✅ v7.2.13 (tree view)
    ├── menu_account.py              ✅ v7.2.2
    ├── menu_embed.py                ✅ v7.2.2
    ├── menu_tools.py                ✅ v7.2.2
    ├── README.md                    ✅ v7.2.13
    ├── requirements.txt             ✅ v7.2.12
    ├── tools.py                     ✅ v7.2.11
    ├── ui_helpers.py                ✅ v7.2.13
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

Embed item fields (v7.2.13):
  {
    "id": "embed_xxx",
    "platform": "youtube",       ← NEW (lowercase slug)
    "source": "YouTube",          ← display name
    "original_url": "https://...",  ← URL asli ke platform
    "no_iframe": false,           ← NEW (flag fallback)
    "tags": ["embed", "youtube", "video"],  ← auto-tag
    ...
  }

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
  ✅ URL embed tambah parameter: origin, enablejsapi, rel, modestbranding, playsinline
  ✅ Fallback UI kalo iframe gagal

🎯 PR-8 — Instagram Embed FIXED:
  ✅ URL embed: /embed/captioned/

🎯 DYNAMIC ASPECT RATIO:
  ✅ YouTube watch → 16/9, Shorts → 9/16
  ✅ Instagram Post → 4/5, Reel/TV → 9/16
  ✅ TikTok → 9/16, Vimeo → 16/9
  ✅ Twitter/X → 16/9, Facebook → 16/9

🎯 AUTO-HIDE UI:
  ✅ Header & footer auto-hide setelah 3 detik
  ✅ Zona tap atas & bawah iframe

🎯 SMART HISTORY:
  ✅ pushState/replaceState + popstate

================================================================================
6b. FITUR v7.2.12 (TREE VIEW + GITHUB_REPO FIX) — SELESAI
================================================================================

✅ PR-1 — Layout Main Menu (tree view ala `tree` command)
✅ PR-3 — Emoji gear ⚙ nyempil → symbol konsisten
✅ PR-4 — GITHUB_REPO gak di-inject → chain fix
✅ PR-5 — templates/about.html dihapus
✅ PR-6 — tools.py header cleanup

================================================================================
6c. FITUR v7.2.13 (PLATFORM ICON + AUTO-TAG + PR-9/10/11) — SELESAI
================================================================================

🔥 3 PR + 5 FITUR + 1 REFACTOR + 2 POLISH DALAM 1 RILIS:

✅ PR-9 — Deteksi embed vs video:
  · A1: Cek extension di query string
  · A2: Tambah HLS/DASH extension (.m3u8, .mpd)
  · A3: is_embed_url() strict (whitelist)
  · A4: _parse_generic() cek whitelist domain
  · A5: _parse_twitter() flag no_iframe (endpoint deprecated)

✅ PR-10 — Info panel "0 B (MP4)":
  · Buat embed: tampilin "Platform: YouTube (MP4)"
  · Hide "Nama/Album/Ukuran/Upload" — gak relevan
  · Tampilin "Link" + "Platform"

✅ PR-11 — Link "Buka di Platform":
  · Tombol "🌐 Buka di [Platform]" (pake icon platform)
  · Fallback UI buat no_iframe (Twitter/X)

🎁 FITUR BARU:

1. PLATFORM ICON (SVG inline):
   · YouTube, Instagram, TikTok, Facebook, Twitter/X, Vimeo
   · Direct Image, Direct Video, Generic
   · Background gradient per platform
   · File: templates/platform-icons.js (BARU)

2. AUTO-TAG dari URL embed:
   · Extract tag dari URL path/query
   · Config toggle: enable_embed_autotag (default ON)
   · Config toggle: embed_autotag_fetch_title (default OFF)
   · File: embed_parser.py

3. FIELD BARU di item dict:
   · `platform` — slug lowercase (youtube, instagram, dll)
   · `original_url` — URL asli ke platform
   · `no_iframe` — flag fallback

4. REFACTOR: gallery.html + platform-icons.js dipisah
   · html_builder.py inject platform-icons.js ke HTML
   · Cleaner architecture

5. ACTION BAR DYNAMIC:
   · Embed → "🌐 Buka di [Platform]"
   · Media biasa → "⬇️ Download"

🎯 BONUS:
   · Git cleanup (menu.py.bak + setup-pointless-repo.sh dihapus)
   · .gitignore update

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
BUG #13 (v7.2.12): Border box miring (emoji width) → FIXED
BUG #14 (v7.2.12): GITHUB_REPO gak di-inject → FIXED
BUG #15 (v7.2.12): tools.py header cursor error → FIXED
BUG #16 (v7.2.13): Info panel "0 B (MP4)" di embed → FIXED
BUG #17 (v7.2.13): Action bar gak relevan buat embed → FIXED
BUG #18 (v7.2.13): Link di info panel pake embed URL → FIXED

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
✅ FASE 3.5 — PLATFORM ICON + AUTO-TAG (SELESAI v7.2.13)
🔥 FASE 4   — FASE 5 PR (38 PR — 12 selesai)
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

TASK YANG BELUM:
  ⏸️ Update README LUMOSS — isi field Website
  ⏸️ Update README portfolio (masih template Amir)

================================================================================
9. CATATAN PENTING
================================================================================

  · Akun real: Cantika (bukan dummy)
  · Akun dummy: Akun Utama (bisa dihapus kalau perlu)
  · Git UDAH di-init — repo: github.com/nexterade/lumoss
  · Branch: main | Protocol: HTTPS | Author: nexter
  · Commit terbaru: 8cea7dc (v7.2.13)
  · Release terbaru: v7.2.13 (Platform Icons + Auto-Tag)
  · PR FASE 5 detail: docs/backlog.md (39 item)
  · Multi-folder media (media_dirs array)
  · Onboarding WAJIB pilih folder
  · Struktur: accounts/ + output/ + cache/
  · Backup folder: /storage/emulated/0/Project/backup/
  · UI tree view v7.2.12
  · Platform icons + auto-tag v7.2.13
  · Embed fix v7.2.11
  · Submenu pake Unicode symbol (bukan emoji)
  · 🌿 = simbol utama Lumoss (gak di-convert)
  · Side project Cinematic Resume — SELESAI v1.0 (Live!)
  · ⛔ ATURAN KERAS: JANGAN kasih command Termux dengan tag #
    (lihat checkpoint.md section 5, rule 4.15)
  · 📌 8 rule + 1 baru = 9 rule total (checkpoint v1.8)
  · 🔥 12 PR selesai total (dari 38)

================================================================================
10. TEST REPORT (2026-09-17)
================================================================================

✅ TEST 1-19  — (lihat state v7.2.12)
✅ TEST 20    — Tree view main menu (v7.2.12) — WORKS
✅ TEST 21    — GITHUB_REPO inject — WORKS
✅ TEST 22    — tools.py header clean — WORKS
✅ TEST 23    — templates/about.html dihapus — WORKS
✅ TEST 24    — PR-9: deteksi embed vs video — WORKS
✅ TEST 25    — Auto-Tag dari URL — WORKS (#shorts kedetect)
✅ TEST 26    — Platform Icon (YouTube, IG, TikTok) — WORKS
✅ TEST 27    — PR-11: Link "Buka di Platform" — WORKS
✅ TEST 28    — PR-10: Info panel embed (bukan "0 B") — WORKS
✅ TEST 29    — Action bar dynamic (Download vs Buka) — WORKS
✅ TEST 30    — Auto-tag #shorts + #video — WORKS

🎯 SEMUA FITUR JALAN SEMPURNA

================================================================================
11. UI/UX PATTERN v7.2.13 (REUSE)
================================================================================

Pattern yang dipake di v7.2.13 — bisa di-reuse di project lain:

1. PLATFORM ICON (SVG inline)
   · SVG path resmi per platform
   · Inline ke HTML via build-time injection
   · File terpisah (platform-icons.js) — gampang maintain
   · Background gradient per platform

2. AUTO-TAG dari URL
   · Extract dari URL path/query
   · Opt-in fetch HTML title
   · Stop words filter
   · Batasi max 8-10 tag

3. DYNAMIC ACTION BAR
   · Conditional render berdasarkan tipe item
   · Embed → "Buka di Platform"
   · Media biasa → "Download"

4. PROGRESSIVE DISCLOSURE (Info Panel)
   · Hide field gak relevan
   · Embed: Platform + Link + Tag
   · Media: Nama + Album + Ukuran + Upload

5. GRACEFUL DEGRADATION
   · no_iframe flag → fallback UI
   · Timeout 8 detik → tampilin link card

6. DEFENSIVE JS
   · `typeof GITHUB_REPO === "string" ? GITHUB_REPO : ""`
   · Guard clause sebelum use

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
  · platform-icons.js         ← NEW v7.2.13

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
13. NEXT STEP
================================================================================

🔥 FASE 4 — ONGOING (12 PR selesai, 26 pending)

PRIORITAS BERIKUTNYA (medium):
  1. PR-16 — Menu Favicon (A+B Hybrid) — 🟢 FINAL
  2. PR-21 — Animasi Glow Pulse — 🟢 FINAL
  3. PR-40 — Thumbnail generation (media_processor.py) ⭐🥇
  4. PR-43 — Pagination / infinite scroll ⭐🥈
  5. PR-28 — Smooth navigation — 🟢 FINAL

REKOMENDASI: PR-16 (Menu Favicon — medium, low risk)

================================================================================
                    END OF STATE v7.2.13
================================================================================