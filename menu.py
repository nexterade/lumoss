"""
lumoss — Menu Utama (v7.2.6 MEDIA GARDEN)
Menu interaktif utama dengan tampilan minimalist modern + multi-folder media.

Changelog v7.2.6:
- NEW: Auto-convert emoji → Unicode symbol pas input (nama, judul, dll)
- KEEP: 🌿 sebagai simbol utama Lumoss (gak di-convert)
- UI: Banner main menu pake 🌿 (bukan ❦)
- UI: _menu_exit pake 🌿
- UPDATE: LUMOSS_VERSION → v7.2.6

Changelog v7.2.5:
- UI: Layout vertikal (Opsi C) — section stack atas-bawah
- UI: "AKUN & RINGKASAN" — sub-judul AKUN AKTIF / RINGKASAN
- UI: "MENU UTAMA" — sub-judul AKSI UTAMA / PENGATURAN
- UPDATE: LUMOSS_VERSION → v7.2.5

Changelog v7.2.4:
- UI: Main menu merged boxes (1 border utuh, multiple section)
- UPDATE: LUMOSS_VERSION → v7.2.4

Changelog v7.2.3:
- UI: Main menu full-width + border utuh (pake helper dari ui_helpers)
- UI: Emoji di main menu diganti Unicode symbol
- FIX: Layout gak lagi hardcoded width 62 — pake layout_widths()

Changelog v7.2.2:
- BREAKING: Output sekarang di output/<slug>/ (bukan accounts/<slug>/)
- BREAKING: Multi-folder media (media_dirs array) — scan multiple folder
- NEW: Onboarding WAJIB pilih folder media (dari DCIM, Pictures, dll)
- NEW: Menu Kelola Folder Media (tambah/hapus/toggle recursive)
- FIX: Skip folder & file hidden/sampah (.thumbnails, .cache, Android, dll)
"""

import os
import sys
import time
import shutil
import re

from ui_helpers import (
    C_RESET, C_BOLD, C_DIM, C_GREEN, C_YELLOW, C_RED, C_WHITE,
    C_MOSS_1, C_MOSS_2, C_MOSS_3, C_SILVER,
    clear_screen, print_banner, print_breadcrumb, print_section,
    print_success, print_error, print_warning, print_info,
    input_prompt, input_yes_no, input_int,
    press_enter, confirm_action, print_table, mask_secret,
    divider, section_title, kv_line, menu_item,
    print_account_card, print_menu_card,
    print_success_aesthetic, print_error_aesthetic,
    print_warning_aesthetic, print_info_aesthetic,
    print_step, print_highlight,
    format_bytes,
    vwidth, vpad, term_width,
    # ── v7.2.3 ──
    layout_widths, render_two_col_box, render_group_box,
    render_group_box_two_col,
    # ── v7.2.4 ──
    render_merged_box, render_merged_group,
    # ── v7.2.5 ──
    render_vertical_box, render_vertical_group,
    # ── v7.2.6 NEW ──
    convert_emoji, strip_emoji, EMOJI_TO_UNICODE, LUMOSS_SYMBOL,
    PROJECT_NAME, PROJECT_FULL, PROJECT_VERSION, PROJECT_AUTHOR,
)

import account_manager as am
import config_manager as cm


# ═══════════════════════════════════════════════════════════
# VERSION / CONSTANTS
# ═══════════════════════════════════════════════════════════

LUMOSS_VERSION = "v7.2.6"
LUMOSS_GATE_TITLE = "LUMOSS :: UPLOAD GATE"
LUMOSS_MENU_TITLE = "LUMOSS :: MAIN MENU"


# ═══════════════════════════════════════════════════════════
# MAIN MENU — ENTRY POINT
# ═══════════════════════════════════════════════════════════

def run_menu(callbacks=None):
    """Menu utama lumoss."""
    if callbacks is None:
        callbacks = {}

    if "run_account" not in callbacks:
        try:
            from menu_account import run_account_menu
            callbacks["run_account"] = run_account_menu
        except ImportError:
            pass

    if "run_tools" not in callbacks:
        try:
            from menu_tools import run_tools_menu
            callbacks["run_tools"] = run_tools_menu
        except ImportError:
            pass

    if "run_embed" not in callbacks:
        try:
            from menu_embed import run_embed_menu
            callbacks["run_embed"] = run_embed_menu
        except ImportError:
            pass

    while True:
        clear_screen()
        print_banner()

        has_account = am.has_accounts()

        if not has_account:
            _show_onboarding(callbacks)
            continue

        _render_main_menu_v2(callbacks)

        pilihan = input_prompt("Pilih menu", default="1")

        if pilihan == "1":
            _menu_upload(callbacks)
        elif pilihan == "2":
            _menu_regenerate(callbacks)
        elif pilihan == "3":
            _menu_check_media(callbacks)
        elif pilihan == "4":
            _menu_embed(callbacks)
        elif pilihan == "5":
            _menu_account(callbacks)
        elif pilihan == "6":
            _menu_tools(callbacks)
        elif pilihan == "7":
            _menu_edit_config()
        elif pilihan == "8":
            _menu_pick_theme()
        elif pilihan == "9":
            _menu_about()
        elif pilihan == "10":
            _menu_help()
        elif pilihan in ("99", "0", "q", "quit", "exit"):
            _menu_exit()


# ═══════════════════════════════════════════════════════════
# MAIN MENU — LAYOUT (v7.2.6 — vertical + 🌿)
# ═══════════════════════════════════════════════════════════

def _render_main_menu_v2(callbacks):
    """Render main menu layout (v7.2.6 — vertical + 🌿)."""
    slug = am.get_active_slug()
    info = am.get_account_info(slug) or {}
    stats = am.get_account_stats(slug)
    cfg = cm.load_config()
    theme = cm.get_theme_default()

    print(f"  {C_SILVER}▸{C_RESET} {C_WHITE}Menu Utama{C_RESET}  {C_SILVER}›{C_RESET}  {C_MOSS_1}{C_BOLD}Dashboard{C_RESET}")
    print()

    _render_menu_banner(slug)
    print()

    _render_top_boxes(slug, info, stats, cfg, theme)
    print()

    # ── MENU UTAMA (vertikal) ──
    render_vertical_group(
        title="MENU UTAMA",
        emoji="◆",
        groups=[
            {
                "title": "AKSI UTAMA",
                "emoji": "◆",
                "items": [
                    ("1", "▶", "Jalankan Upload & Generate"),
                    ("2", "↻", "Regenerate Output (HTML)"),
                    ("3", "▣", "Cek Folder Media"),
                    ("4", "◐", "Import Embed dari URL"),
                ],
            },
            {
                "title": "PENGATURAN",
                "emoji": "⚙",
                "items": [
                    ("5", "❖", "Account Manager"),
                    ("6", "⚒", "Tools & Utilities"),
                    ("7", "✎", "Edit Konfigurasi"),
                    ("8", "◈", "Pilih Tema"),
                    ("9", "ℹ", "Tentang Lumoss"),
                    ("10", "?", "Bantuan"),
                ],
            },
        ],
    )
    print()

    # Footer — align kiri
    total, _, _, _ = layout_widths()
    print(f"  {C_MOSS_1}│{C_RESET}  {C_SILVER}[99]{C_RESET}  {C_RED}✗{C_RESET}  {C_WHITE}Keluar{C_RESET}")
    print(f"  {C_MOSS_1}└{'─' * (total - 2)}┘{C_RESET}")
    print()


def _render_menu_banner(slug):
    """Banner main menu (v7.2.6 — pake 🌿)."""
    left = f"{C_MOSS_1}{C_BOLD}{LUMOSS_SYMBOL}  LUMOSS :: MAIN MENU{C_RESET}"
    right = f"{C_MOSS_3}v{LUMOSS_VERSION[1:]}{C_RESET}  {C_MOSS_1}///{C_RESET}"

    # vwidth handle 🌿 sebagai 2-cell emoji
    left_vis = vwidth(f"{LUMOSS_SYMBOL}  LUMOSS :: MAIN MENU")
    right_vis = vwidth(f"v{LUMOSS_VERSION[1:]}  ///")

    total, _, _, _ = layout_widths()
    gap = max(1, total - left_vis - right_vis - 2)

    print(f"  {left}{' ' * gap}{right}")
    print(f"  {C_MOSS_1}{'━' * total}{C_RESET}")


def _render_top_boxes(slug, info, stats, cfg, theme):
    """Akun Aktif + Ringkasan — 1 box vertikal (v7.2.6)."""
    name = info.get("name", slug)
    uh = info.get("userhash_masked", "") or "(anonymous)"

    # Safety net: kalo user manual edit config.json & masukin emoji
    # Konversi emoji → unicode symbol (kecuali 🌿)
    name = convert_emoji(name)
    uh = convert_emoji(uh)

    media_dirs = cm.get_enabled_media_dirs(slug)
    folder_count = len(media_dirs)

    akun_lines = [
        f"{C_SILVER}◉ Nama      {C_RESET}{C_SILVER}:{C_RESET} {C_WHITE}{name[:24]}{C_RESET}",
        f"{C_SILVER}⚿ Userhash  {C_RESET}{C_SILVER}:{C_RESET} {C_SILVER}{uh[:24]}{C_RESET}",
        f"{C_SILVER}▸ Folder    {C_RESET}{C_SILVER}:{C_RESET} {C_MOSS_3}{folder_count} folder{C_RESET}",
        f"{C_SILVER}◈ Tema      {C_RESET}{C_SILVER}:{C_RESET} {C_MOSS_1}{theme}{C_RESET}",
    ]

    gh_user = (cfg.get("github_username") or "").strip()
    gh_repo = (cfg.get("github_repo") or "").strip()
    gh_status = f"{gh_user}/{gh_repo}" if gh_user and gh_repo else "belum setup"
    if len(gh_status) > 24:
        gh_status = gh_status[:22] + "..."

    paths = am.get_account_paths(slug)
    pending = 0
    total_size = stats.get("size_bytes", 0)
    uploaded_count = stats.get("files", 0)
    try:
        scan = _scan_media_dirs(slug, paths)
        pending = scan["not_uploaded_count"]
        total_size = scan["total_size"]
        total_files = scan["total"]
    except Exception:
        total_files = uploaded_count

    ringkasan_lines = [
        f"{C_SILVER}▪ Files     {C_RESET}{C_SILVER}:{C_RESET} {C_WHITE}{total_files}{C_RESET} {C_SILVER}({format_bytes(total_size)}){C_RESET}",
        f"{C_GREEN}✓ Uploaded  {C_RESET}{C_SILVER}:{C_RESET} {C_WHITE}{uploaded_count} file{C_RESET}",
        f"{C_YELLOW}◷ Pending   {C_RESET}{C_SILVER}:{C_RESET} {C_WHITE}{pending} file{C_RESET}",
        f"{C_SILVER}⚑ GitHub    {C_RESET}{C_SILVER}:{C_RESET} {C_SILVER}{gh_status}{C_RESET}",
    ]

    render_vertical_box(
        title="AKUN & RINGKASAN",
        emoji="◉",
        sections=[
            {"title": "AKUN AKTIF", "emoji": "◉", "lines": akun_lines},
            {"title": "RINGKASAN",  "emoji": "▤", "lines": ringkasan_lines},
        ],
    )


def _render_menu_group(title, emoji, items):
    """Render 1 grup menu (legacy — backward compat)."""
    render_group_box(title, emoji, items)


def _render_menu_group_two_col(title, emoji, left, right):
    """Render grup menu 2 kolom (legacy — backward compat)."""
    render_group_box_two_col(title, emoji, left, right)


# ═══════════════════════════════════════════════════════════
# ONBOARDING (v7.2.2 — WAJIB PILIH FOLDER)
# ═══════════════════════════════════════════════════════════

def _show_onboarding(callbacks):
    """Tampilkan onboarding kalau belum ada akun."""
    print()
    section_title("SELAMAT DATANG DI LUMOSS", emoji=LUMOSS_SYMBOL)
    print()

    print(f"  {C_MOSS_1}Woy! Lumoss belum punya akun nih.{C_RESET}")
    print(f"  {C_SILVER}Yuk bikin akun pertama + pilih folder media! {LUMOSS_SYMBOL}{C_RESET}")
    print()

    print_menu_card(
        title="MULAI DARI SINI",
        emoji="◆",
        items=[
            ("1",  "Buat Akun Pertama", "✚"),
            ("2",  "Lihat Tutorial",    "?"),
            ("99", "Keluar",            "✗"),
        ],
    )

    pilihan = input_prompt("Pilih menu", default="1")

    if pilihan == "1":
        _menu_create_first_account(callbacks)
    elif pilihan == "2":
        _menu_quick_tutorial()
    elif pilihan in ("99", "0"):
        _menu_exit()
    else:
        print_error_aesthetic("Pilihan lu ngaco cuy")
        press_enter()


def _menu_create_first_account(callbacks):
    """Bikin akun pertama via wizard singkat + WAJIB pilih folder."""
    print()
    section_title("BUAT AKUN PERTAMA", emoji="✚")
    print()

    print(f"  {C_MOSS_1}✦ Akun pertama otomatis jadi akun AKTIF.{C_RESET}")
    print(f"  {C_SILVER}   Bisa punya banyak akun nanti kok.{C_RESET}")
    print()

    # v7.2.6: auto-convert emoji → unicode (kecuali 🌿)
    name = input_prompt("Nama akun", default="Akun Utama")
    if not name or not name.strip():
        name = "Akun Utama"
    name = convert_emoji(name.strip())

    print()
    print(f"  {C_MOSS_1}✦ Userhash Catbox (opsional). Kosongin buat anonymous.{C_RESET}")
    print(f"  {C_SILVER}   Ambil di: https://catbox.moe/user/manage.php{C_RESET}")
    userhash = input_prompt("Userhash", default="", allow_empty=True)

    print()
    judul = input_prompt("Judul project", default=name)
    # v7.2.6: auto-convert emoji → unicode (kecuali 🌿)
    judul = convert_emoji(judul.strip())

    # ── v7.2.2: WAJIB pilih folder media ──
    print()
    print(f"  {C_MOSS_1}{C_BOLD}▸ Pilih folder media (WAJIB){C_RESET}")
    print(f"  {C_SILVER}Foto/video lu bakal di-scan dari folder ini.{C_RESET}")
    print()
    press_enter("Tekan Enter buat mulai scan folder...")

    media_dirs = am.pick_media_folders_onboarding()
    if not media_dirs:
        print_warning_aesthetic("Yaudah, dibatalin deh")
        press_enter()
        return

    # ── Theme picker ──
    print()
    theme_id = _pick_theme_interactive()
    if theme_id is None:
        print_warning_aesthetic("Yaudah, dibatalin deh")
        press_enter()
        return

    # ── Konfirmasi ──
    print()
    divider()
    print()
    kv_line("Nama", name)
    kv_line("Userhash", mask_secret(userhash) if userhash else "(anonymous)", value_color=C_SILVER)
    kv_line("Judul", judul)
    kv_line("Tema", theme_id, value_color=C_MOSS_1)
    kv_line("Folder media", f"{len(media_dirs)} folder", value_color=C_MOSS_2)
    for md in media_dirs:
        print(f"  {C_SILVER}  • {md['path']}{C_RESET}")
    print()
    divider()
    print()

    if not input_yes_no("Gaskan bikin akun ini?", default="y"):
        print_warning_aesthetic("Yaudah, dibatalin deh")
        press_enter()
        return

    print()
    ok, result = am.create_account(name, userhash=userhash, judul=judul, media_dirs=media_dirs)

    if ok:
        slug = result
        try:
            cm.set_theme_default(theme_id)
        except Exception:
            pass

        print_success_aesthetic(f"Akun '{name}' udah jadi nih boss!", emoji="✓")
        print()
        kv_line("Slug", slug, value_color=C_MOSS_2)
        kv_line("Config", f"accounts/{slug}/config.json")
        kv_line("Output", f"output/{slug}/")
        kv_line("Cache", f"cache/{slug}/")
        kv_line("Media", f"{len(media_dirs)} folder", value_color=C_MOSS_1)
        print()
        print(f"  {C_MOSS_1}◆ Next step:{C_RESET}")
        print(f"     {C_SILVER}• Jalankan upload: {C_WHITE}menu 1{C_RESET}")
    else:
        print_error_aesthetic(f"Waduh gagal bro: {result}")

    press_enter()


# ═══════════════════════════════════════════════════════════
# THEME PICKER
# ═══════════════════════════════════════════════════════════

def _print_theme_row(num, emoji, name, desc, marker="", name_col=18, desc_col=30):
    """Cetak 1 baris tema."""
    print(
        f"  {C_MOSS_1}{C_BOLD}{num:>2}{C_RESET}  {emoji}"
        f"\033[{name_col}G{C_WHITE}{name}{C_RESET}"
        f"\033[{desc_col}G{C_SILVER}{desc}{C_RESET}{marker}"
    )


def _pick_theme_interactive():
    """Interactive theme picker."""
    themes = cm.list_available_themes()
    current_default = cm.get_theme_default()

    print()
    section_title("PILIH TEMA GALERI", emoji="◈")
    print()
    print(f"  {C_SILVER}Pilih tema buat galeri lu. Bisa diganti nanti kapan aja.{C_RESET}")
    print()

    for i, t in enumerate(themes, 1):
        marker = f" {C_MOSS_1}← default{C_RESET}" if t["id"] == current_default else ""
        _print_theme_row(i, t["emoji"], t["name"], t["desc"], marker=marker)

    print()
    print(f"  {C_SILVER} 0{C_RESET}  {C_SILVER}↩ Batal{C_RESET}")
    print()

    pilihan = input_int(
        f"Pilih tema (1-{len(themes)})",
        default=0,
        min_val=0,
        max_val=len(themes),
    )

    if pilihan == 0:
        return None

    return themes[pilihan - 1]["id"]


def _menu_quick_tutorial():
    """Tutorial singkat untuk user baru."""
    clear_screen()
    print_banner(compact=True)
    print()
    section_title("TUTORIAL SINGKAT", emoji="?")
    print()

    print(f"""  {C_MOSS_1}Selamat datang di {PROJECT_NAME}! {LUMOSS_SYMBOL}{C_RESET}

  {C_MOSS_1}━━━ APA ITU LUMOSS? ━━━{C_RESET}

  {C_WHITE}Lumoss = tool buat upload otomatis foto/video ke Catbox.moe,
  terus generate galeri HTML cantik yang bisa dibuka di browser.{C_RESET}

  {C_MOSS_1}━━━ LANGKAH PAKE ━━━{C_RESET}

  {C_GREEN}1. Bikin Akun + Pilih Folder Media{C_RESET}
     Menu 5: Account Manager → Setup akun
     {C_SILVER}→ WAJIB pilih folder (DCIM, Pictures, dll){C_RESET}

  {C_GREEN}2. Gas Upload{C_RESET}
     Menu 1: Jalankan Upload & Generate

  {C_GREEN}3. Buka Galeri{C_RESET}
     Buka file {C_WHITE}output/<slug>/index.html{C_RESET} di browser.

  {C_MOSS_1}━━━ FITUR UTAMA ━━━{C_RESET}

  ✓ Multi-akun Catbox (bisa punya banyak akun)
  ✓ Multi-folder media (DCIM + Pictures + dll)
  ✓ Auto-tag dari nama file + folder + EXIF
  ✓ Thumbnail otomatis (WebP foto, JPG video)
  ✓ Galeri interaktif 6 tema
  ✓ 2 layout: Mosaic (Pinterest) + Grid
  ✓ Autoplay video pintar (mode auto)
  ✓ Import Embed (YouTube, IG, TikTok, dll)
  ✓ Upload ke GitHub Pages 1 klik
""")
    press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 1: UPLOAD
# ═══════════════════════════════════════════════════════════

def _menu_upload(callbacks):
    """Jalankan upload."""
    if "run_upload" in callbacks and callbacks["run_upload"]:
        try:
            callbacks["run_upload"]()
            slug = am.get_active_slug()
            if slug:
                try:
                    am.update_account_stats(slug)
                except Exception:
                    pass
        except Exception as e:
            print()
            print_error_aesthetic(f"Waduh error pas upload: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
        press_enter()
    else:
        print_warning_aesthetic("Fungsi upload belum siap bosque")
        print_info_aesthetic("File 'uploader.py' harus ada + callback 'run_upload' di-set.")
        press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 3: CHECK MEDIA — UPLOAD GATE (v7.2.2 multi-folder)
# ═══════════════════════════════════════════════════════════

def _menu_check_media(callbacks=None):
    """Cek isi folder media (multi-folder)."""
    if callbacks is None:
        callbacks = {}

    slug = am.get_active_slug()
    if not slug:
        clear_screen()
        print_banner(compact=True)
        print_breadcrumb(["Menu Utama", "Cek Folder Media"])
        print_warning_aesthetic("Belum ada akun aktif bosque")
        press_enter()
        return

    paths = am.get_account_paths(slug)
    media_dirs = cm.get_enabled_media_dirs(slug)

    if not media_dirs:
        clear_screen()
        print_banner(compact=True)
        print_breadcrumb(["Menu Utama", "Cek Folder Media"])
        print()
        print_warning_aesthetic("Belum ada folder media yang di-set.")
        print_info_aesthetic("Buka menu 7 → Edit Konfigurasi → Kelola Folder Media")
        press_enter()
        return

    while True:
        scan = _scan_media_dirs(slug, paths)

        if scan["total"] == 0:
            clear_screen()
            print_banner(compact=True)
            print_breadcrumb(["Menu Utama", "Cek Folder Media"])
            print()
            print_info_aesthetic("Belum ada media bos. Taruh foto/video di folder media.")
            press_enter()
            return

        clear_screen()
        print_banner(compact=True)
        _render_gate_banner(slug, scan)
        _render_dashboard(scan, media_dirs)
        _render_pipeline_preview(scan)
        _render_verification_gate(scan)

        raw = input(
            f"  {C_MOSS_1}›{C_RESET} Pilihan {C_SILVER}[Enter]{C_RESET}: "
        ).strip().lower()

        if raw in ("", "enter", "y", "ya", "1"):
            if callbacks and callbacks.get("run_upload"):
                print()
                print(f"  {C_MOSS_3}▸{C_RESET} {C_WHITE}Mengeksekusi…{C_RESET}")
                print()
                try:
                    callbacks["run_upload"]()
                    try:
                        am.update_account_stats(slug)
                    except Exception:
                        pass
                except Exception as e:
                    print()
                    print_error_aesthetic(
                        f"Waduh error pas upload: {type(e).__name__}: {e}"
                    )
                    import traceback
                    traceback.print_exc()
            else:
                print_warning_aesthetic("Fungsi upload belum siap bosque")
                print_info_aesthetic("Callback 'run_upload' belum di-set.")
            press_enter()
            return

        elif raw in ("q", "quit", "exit", "keluar"):
            return

        else:
            continue


# ═══════════════════════════════════════════════════════════
# MENU 2: REGENERATE OUTPUT
# ═══════════════════════════════════════════════════════════

def _menu_regenerate(callbacks=None):
    """Regenerate output HTML dari cache."""
    if callbacks is None:
        callbacks = {}

    slug = am.get_active_slug()
    if not slug:
        clear_screen()
        print_banner(compact=True)
        print_breadcrumb(["Menu Utama", "Regenerate Output"])
        print_warning_aesthetic("Belum ada akun aktif bosque")
        press_enter()
        return

    paths = am.get_account_paths(slug)
    media_dirs = cm.get_enabled_media_dirs(slug)

    if not media_dirs:
        clear_screen()
        print_banner(compact=True)
        print_breadcrumb(["Menu Utama", "Regenerate Output"])
        print()
        print_warning_aesthetic("Belum ada folder media yang di-set.")
        press_enter()
        return

    while True:
        scan = _scan_media_dirs(slug, paths)

        if scan["total"] == 0:
            clear_screen()
            print_banner(compact=True)
            print_breadcrumb(["Menu Utama", "Regenerate Output"])
            print()
            print_info_aesthetic("Belum ada media bos.")
            press_enter()
            return

        new_files = scan["not_uploaded_count"]

        clear_screen()
        print_banner(compact=True)
        _render_regenerate_banner(slug, scan)
        _render_dashboard(scan, media_dirs)

        if new_files > 0:
            print(f"  {C_YELLOW}!! Warning:{C_RESET} {C_WHITE}{new_files} file belum diupload{C_RESET}")
            print(f"  {C_SILVER}    File baru gak bakal masuk galeri. Upload dulu via menu 1.{C_RESET}")
            print()

        _render_regenerate_gate(scan)

        raw = input(
            f"  {C_MOSS_1}›{C_RESET} Pilihan {C_SILVER}[Enter]{C_RESET}: "
        ).strip().lower()

        if raw in ("", "enter", "y", "ya", "1"):
            if callbacks and callbacks.get("run_regenerate"):
                print()
                print(f"  {C_MOSS_3}▸{C_RESET} {C_WHITE}Regenerate HTML…{C_RESET}")
                print()
                try:
                    callbacks["run_regenerate"]()
                    try:
                        am.update_account_stats(slug)
                    except Exception:
                        pass
                except Exception as e:
                    print()
                    print_error_aesthetic(
                        f"Waduh error pas regenerate: {type(e).__name__}: {e}"
                    )
                    import traceback
                    traceback.print_exc()
            else:
                print_warning_aesthetic("Fungsi regenerate belum siap bosque")
            press_enter()
            return

        elif raw in ("q", "quit", "exit", "keluar"):
            return

        else:
            continue


def _render_regenerate_banner(slug, scan):
    """Banner regen (v7.2.6 — pake 🌿)."""
    left = f"{C_MOSS_1}{C_BOLD}↻ {LUMOSS_SYMBOL} LUMOSS :: REGENERATE{C_RESET}"
    right = f"build HTML • v{LUMOSS_VERSION[1:]}"

    left_vis = vwidth(f"↻ {LUMOSS_SYMBOL} LUMOSS :: REGENERATE")
    right_vis = vwidth(right)
    total, _, _, _ = layout_widths()
    gap = max(1, total - left_vis - right_vis - 2)

    print(f"  {left}{' ' * gap}{C_MOSS_3}{right}{C_RESET}")
    print(f"  {C_MOSS_1}{'━' * total}{C_RESET}")
    print()
    print(f"  {C_SILVER}▸{C_RESET} {C_WHITE}Menu Utama{C_RESET}  {C_SILVER}›{C_RESET}  {C_WHITE}Regenerate Output{C_RESET}")
    print(f"  {C_SILVER}▸{C_RESET} {C_MOSS_3}output/{slug}/index.html{C_RESET}")
    print()


def _render_regenerate_gate(scan):
    """Gate khusus regen."""
    try:
        cfg = cm.load_config()
    except Exception:
        cfg = {}

    total_cached_bytes = scan["uploaded_size"]
    file_count = scan["uploaded_count"]

    slug = am.get_active_slug()
    embed_count = 0
    if slug:
        paths = am.get_account_paths(slug)
        embed_file = paths["embed_txt"]
        if os.path.exists(embed_file):
            try:
                with open(embed_file, "r", encoding="utf-8") as f:
                    embed_count = sum(
                        1 for ln in f
                        if ln.strip() and not ln.strip().startswith("#")
                    )
            except Exception:
                pass

    print(f"  {C_MOSS_1}{'━' * 60}{C_RESET}")
    print(f"  {C_MOSS_1}{C_BOLD}│  REGENERATE OUTPUT{C_RESET}")
    print()

    print(f"  {C_SILVER}Sistem akan melakukan:{C_RESET}")
    print()
    print(f"    {C_GREEN}✓{C_RESET}  Build index.html dari {file_count} file cache")
    print(f"    {C_GREEN}✓{C_RESET}  Build manager.html")
    if embed_count > 0:
        print(f"    {C_GREEN}✓{C_RESET}  Load {embed_count} embed dari embed.txt")
    print(f"    {C_GREEN}✓{C_RESET}  Apply tema: {C_MOSS_1}{cm.get_theme_default()}{C_RESET}")
    print(f"    {C_GREEN}✓{C_RESET}  Sync cache lokal")
    print()

    print(f"  {C_MOSS_1}{'─' * 52}{C_RESET}")
    print(f"  {C_SILVER}File cache {C_RESET} {C_SILVER}:{C_RESET}  {C_MOSS_1}{file_count} file ({_fmt_size(total_cached_bytes)}){C_RESET}")
    print(f"  {C_SILVER}Embed      {C_RESET} {C_SILVER}:{C_RESET}  {C_MOSS_1}{embed_count} URL{C_RESET}")
    print(f"  {C_SILVER}Target     {C_RESET} {C_SILVER}:{C_RESET}  {C_WHITE}output/<slug>/index.html + manager.html{C_RESET}")
    print(f"  {C_MOSS_1}{'─' * 52}{C_RESET}")
    print()

    print(f"  {C_MOSS_1}│{C_RESET}  {C_WHITE}{C_BOLD}Regenerate, atau batalin?{C_RESET}")
    print()
    print(f"  {C_SILVER}│{C_RESET}  {C_GREEN}[Enter]{C_RESET} {C_SILVER}Regenerate{C_RESET}")
    print(f"  {C_SILVER}│{C_RESET}  {C_YELLOW}[n]{C_RESET}     {C_SILVER}Batalin{C_RESET}")
    print(f"  {C_SILVER}│{C_RESET}  {C_SILVER}[q]{C_RESET}     {C_SILVER}Keluar{C_RESET}")
    print()


# ═══════════════════════════════════════════════════════════
# MENU 4: IMPORT EMBED
# ═══════════════════════════════════════════════════════════

def _menu_embed(callbacks):
    """Buka submenu import embed."""
    if "run_embed" in callbacks and callbacks["run_embed"]:
        try:
            callbacks["run_embed"]()
        except Exception as e:
            print()
            print_error_aesthetic(f"Error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
        press_enter()
    else:
        print_warning_aesthetic("Fungsi import embed belum siap bosque")
        print_info_aesthetic("File 'menu_embed.py' & 'embed_parser.py' harus ada.")
        press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 5: ACCOUNT MANAGER
# ═══════════════════════════════════════════════════════════

def _menu_account(callbacks):
    """Buka submenu account manager."""
    if "run_account" in callbacks and callbacks["run_account"]:
        try:
            callbacks["run_account"]()
        except Exception as e:
            print()
            print_error_aesthetic(f"Error: {type(e).__name__}: {e}")
            press_enter()
    else:
        print_warning_aesthetic("Fungsi account manager belum ada")
        press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 6: TOOLS
# ═══════════════════════════════════════════════════════════

def _menu_tools(callbacks):
    """Buka submenu tools."""
    if "run_tools" in callbacks and callbacks["run_tools"]:
        try:
            callbacks["run_tools"]()
        except Exception as e:
            print()
            print_error_aesthetic(f"Error: {type(e).__name__}: {e}")
            press_enter()
    else:
        print_warning_aesthetic("Fungsi tools belum ada")
        press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 7: EDIT CONFIG
# ═══════════════════════════════════════════════════════════

def _menu_edit_config():
    """Edit config akun aktif."""
    while True:
        clear_screen()
        print_banner(compact=True)
        print_breadcrumb(["Menu Utama", "Edit Konfigurasi"])

        cfg = cm.load_config()

        print()
        section_title("EDIT KONFIGURASI", emoji="✎")
        print()

        print(f"  {C_MOSS_1}Pilih field yang mau diedit:{C_RESET}")
        print()
        menu_item("1", "Userhash Catbox",  "⚿")
        menu_item("2", "Judul Project",    "▪")
        menu_item("3", "Counter Namespace", "▤")
        menu_item("4", "Jumlah Workers (1-4)", "⚙")
        menu_item("5", "Kelola Folder Media", "▸")
        menu_item("6", "GitHub Username",  "⚑")
        menu_item("7", "GitHub Repo",      "▣")
        menu_item("8", "GitHub Token",     "⚿")
        menu_item("9", "GitHub Branch",    "⚒")
        menu_item("0", "Kembali",          "↩")
        print()

        pilihan = input_prompt("Pilih field", default="0")

        if pilihan == "0":
            return

        if pilihan == "1":
            cfg["userhash"] = input_prompt("Userhash", default=cfg.get("userhash", ""), allow_empty=True)
        elif pilihan == "2":
            raw = input_prompt("Judul project", default=cfg.get("judul_project", "lumoss"))
            # v7.2.6: auto-convert emoji → unicode
            cfg["judul_project"] = convert_emoji(raw.strip())
        elif pilihan == "3":
            cfg["counter_namespace"] = input_prompt("Namespace", default=cfg.get("counter_namespace", ""))
        elif pilihan == "4":
            w = input_int("Workers", default=cfg.get("workers", 1), min_val=1, max_val=4)
            cfg["workers"] = w
        elif pilihan == "5":
            _menu_manage_media_dirs()
            continue
        elif pilihan == "6":
            cfg["github_username"] = input_prompt("GitHub username", default=cfg.get("github_username", ""), allow_empty=True)
        elif pilihan == "7":
            cfg["github_repo"] = input_prompt("GitHub repo", default=cfg.get("github_repo", ""), allow_empty=True)
        elif pilihan == "8":
            cfg["github_token"] = input_prompt("GitHub token", default=cfg.get("github_token", ""), allow_empty=True)
        elif pilihan == "9":
            cfg["github_branch"] = input_prompt("GitHub branch", default=cfg.get("github_branch", "main"))
        else:
            print_error_aesthetic("Pilihan lu ngaco cuy")
            press_enter()
            continue

        ok, msg = cm.save_config(cfg)
        if ok:
            print_success_aesthetic("Konfigurasi udah kesave!")
            try:
                if hasattr(am, "sync_active_json"):
                    am.sync_active_json()
            except Exception:
                pass
        else:
            print_error_aesthetic(f"Gagal save: {msg}")

        press_enter()


# ═══════════════════════════════════════════════════════════
# KELOLA FOLDER MEDIA (v7.2.2)
# ═══════════════════════════════════════════════════════════

def _menu_manage_media_dirs():
    """Kelola folder media (tambah/hapus/toggle)."""
    while True:
        clear_screen()
        print_banner(compact=True)
        print_breadcrumb(["Menu Utama", "Edit Konfigurasi", "Kelola Folder Media"])

        slug = am.get_active_slug()
        media_dirs = cm.get_media_dirs(slug)

        print()
        section_title("KELOLA FOLDER MEDIA", emoji="▸")
        print()

        if not media_dirs:
            print_warning_aesthetic("Belum ada folder media.")
        else:
            print(f"  {C_SILVER}Total {len(media_dirs)} folder:{C_RESET}")
            print()

            for i, md in enumerate(media_dirs, 1):
                enabled = md.get("enabled", True)
                rec = md.get("recursive", True)
                status = f"{C_GREEN}✓ ON {C_RESET}" if enabled else f"{C_RED}✗ OFF{C_RESET}"
                rec_str = f"{C_MOSS_3}recursive{C_RESET}" if rec else f"{C_SILVER}top-level{C_RESET}"
                print(f"  {C_MOSS_1}[{i}]{C_RESET} {status}  {C_WHITE}{md['path']}{C_RESET}")
                print(f"      {C_SILVER}label:{C_RESET} {md['label']}  {C_SILVER}•{C_RESET}  {rec_str}")
                print()

        print(f"  {C_MOSS_1}[a]{C_RESET}  ✚ Tambah folder")
        print(f"  {C_MOSS_1}[h]{C_RESET}  ✗  Hapus folder")
        print(f"  {C_MOSS_1}[t]{C_RESET}  ↻ Toggle ON/OFF")
        print(f"  {C_MOSS_1}[r]{C_RESET}  ▸ Toggle recursive")
        print(f"  {C_MOSS_1}[0]{C_RESET}  ↩  Kembali")
        print()

        pilihan = input_prompt("Pilih", default="0").strip().lower()

        if pilihan == "0":
            return

        if pilihan == "a":
            print()
            print(f"  {C_MOSS_1}[1]{C_RESET}  Scan folder umum (DCIM, Pictures, dll)")
            print(f"  {C_MOSS_1}[2]{C_RESET}  Input path manual")
            print(f"  {C_MOSS_1}[0]{C_RESET}  Batal")
            print()

            sub = input_prompt("Pilih", default="1").strip()

            if sub == "0":
                continue

            new_dir = None
            if sub == "1":
                folders = am.scan_available_media_folders()
                if not folders:
                    print_warning_aesthetic("Gak ada folder ke-detect.")
                    press_enter()
                    continue

                print()
                for i, f in enumerate(folders, 1):
                    print(f"  {C_MOSS_1}[{i}]{C_RESET}  {C_WHITE}{f['path']}{C_RESET}")
                    print(f"        {C_SILVER}({f['file_count']} file, {f['size_human']}){C_RESET}")
                print()

                idx = input_int("Pilih folder", default=0, min_val=0, max_val=len(folders))
                if idx == 0:
                    continue
                new_dir = folders[idx - 1]
            elif sub == "2":
                path = input_prompt("Path folder").strip()
                if not path:
                    continue
                new_dir = am.scan_custom_folder(path)
                if not new_dir:
                    print_error_aesthetic("Folder gak valid.")
                    press_enter()
                    continue

            if new_dir:
                existing_paths = [d["path"] for d in media_dirs]
                if new_dir["path"] in existing_paths:
                    print_warning_aesthetic("Folder udah ada di list.")
                    press_enter()
                    continue

                media_dirs.append({
                    "path": new_dir["path"],
                    "recursive": True,
                    "enabled": True,
                    "label": new_dir["label"],
                })
                cm.set_media_dirs(media_dirs)
                print_success_aesthetic(f"Ditambah: {new_dir['path']}")
                press_enter()

        elif pilihan == "h":
            if not media_dirs:
                continue
            idx = input_int("Hapus folder nomor", default=0, min_val=0, max_val=len(media_dirs))
            if idx == 0:
                continue
            removed = media_dirs.pop(idx - 1)
            cm.set_media_dirs(media_dirs)
            print_success_aesthetic(f"Dihapus: {removed['path']}")
            press_enter()

        elif pilihan == "t":
            if not media_dirs:
                continue
            idx = input_int("Toggle folder nomor", default=0, min_val=0, max_val=len(media_dirs))
            if idx == 0:
                continue
            media_dirs[idx - 1]["enabled"] = not media_dirs[idx - 1].get("enabled", True)
            cm.set_media_dirs(media_dirs)
            new_state = "ON" if media_dirs[idx - 1]["enabled"] else "OFF"
            print_success_aesthetic(f"Folder {idx} → {new_state}")
            press_enter()

        elif pilihan == "r":
            if not media_dirs:
                continue
            idx = input_int("Toggle recursive folder nomor", default=0, min_val=0, max_val=len(media_dirs))
            if idx == 0:
                continue
            media_dirs[idx - 1]["recursive"] = not media_dirs[idx - 1].get("recursive", True)
            cm.set_media_dirs(media_dirs)
            new_state = "recursive" if media_dirs[idx - 1]["recursive"] else "top-level"
            print_success_aesthetic(f"Folder {idx} → {new_state}")
            press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 8: PILIH TEMA
# ═══════════════════════════════════════════════════════════

def _menu_pick_theme():
    """Menu pilih tema galeri default."""
    clear_screen()
    print_banner(compact=True)
    print_breadcrumb(["Menu Utama", "Pilih Tema"])

    print()
    section_title("PILIH TEMA GALERI", emoji="◈")
    print()

    themes = cm.list_available_themes()
    current = cm.get_theme_default()

    print(f"  {C_SILVER}Tema saat ini: {C_MOSS_1}{current}{C_RESET}")
    print()

    for i, t in enumerate(themes, 1):
        marker = f" {C_MOSS_1}✓{C_RESET}" if t["id"] == current else "  "
        _print_theme_row(i, t["emoji"], t["name"], t["desc"], marker=marker)

    print()
    print(f"  {C_SILVER} 0{C_RESET}  {C_SILVER}↩ Kembali{C_RESET}")
    print()

    pilihan = input_int(
        f"Pilih tema (1-{len(themes)})",
        default=0,
        min_val=0,
        max_val=len(themes),
    )

    if pilihan == 0:
        return

    theme_id = themes[pilihan - 1]["id"]

    if theme_id == current:
        print_info_aesthetic(f"Tema '{theme_id}' udah jadi default bosque")
        press_enter()
        return

    ok, msg = cm.set_theme_default(theme_id)
    if ok:
        print_success_aesthetic(f"Tema default diubah ke '{theme_id}' ✓")
        print_info_aesthetic("Restart Lumoss atau regenerate galeri buat liat perubahannya")
    else:
        print_error_aesthetic(msg)

    press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 9: ABOUT
# ═══════════════════════════════════════════════════════════

def _menu_about():
    """About Lumoss."""
    clear_screen()
    print_banner(compact=True)
    print_breadcrumb(["Menu Utama", "Tentang Lumoss"])

    print()
    section_title("TENTANG LUMOSS", emoji=LUMOSS_SYMBOL)
    print()

    print(f"  {C_MOSS_1}{C_BOLD}{PROJECT_FULL}{C_RESET}")
    print(f"  {C_SILVER}Media Garden, in bloom{C_RESET}")
    print()

    kv_line("Version",  "7.2.6", value_color=C_GREEN)
    kv_line("Author",   PROJECT_AUTHOR)
    kv_line("License",  "MIT")
    print()
    divider()

    print(f"""
  {C_WHITE}Lumoss adalah tool buat upload otomatis{C_RESET}
  {C_WHITE}foto/video ke Catbox.moe, generate galeri HTML{C_RESET}
  {C_WHITE}interaktif, terus deploy ke GitHub Pages.{C_RESET}
""")

    print(f"  {C_MOSS_1}✦ Fitur utama:{C_RESET}")
    print(f"    {C_GREEN}•{C_RESET} Multi-akun Catbox dengan folder terisolasi")
    print(f"    {C_GREEN}•{C_RESET} Multi-folder media (DCIM + Pictures + dll)")
    print(f"    {C_GREEN}•{C_RESET} Auto-tag & auto-date dari filename + EXIF")
    print(f"    {C_GREEN}•{C_RESET} Thumbnail otomatis (WebP + JPG)")
    print(f"    {C_GREEN}•{C_RESET} Galeri: 6 tema, 2 layout (Mosaic + Grid)")
    print(f"    {C_GREEN}•{C_RESET} Import embed (YouTube, IG, TikTok, dll)")
    print(f"    {C_GREEN}•{C_RESET} Autoplay video Instagram style")
    print(f"    {C_GREEN}•{C_RESET} Upload ke GitHub Pages 1 klik")
    print(f"    {C_GREEN}•{C_RESET} Auto-convert emoji → Unicode symbol")
    print()

    print(f"  {C_MOSS_1}? Info lengkap:{C_RESET}")
    print(f"    {C_SILVER}Buka{C_RESET} {C_WHITE}output/<slug>/index.html{C_RESET} {C_SILVER}di browser → klik tombol{C_RESET} {C_MOSS_3}ℹ About{C_RESET}")
    print()

    press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 10: HELP
# ═══════════════════════════════════════════════════════════

def _menu_help():
    """Menu bantuan (submenu)."""
    while True:
        clear_screen()
        print_banner(compact=True)
        print_breadcrumb(["Menu Utama", "Bantuan"])

        print_menu_card(
            title="BANTUAN",
            emoji="?",
            items=[
                ("1", "Tutorial Singkat",          "?"),
                ("2", "Cara Setup GitHub",         "⚑"),
                ("3", "Struktur Folder",           "▣"),
                ("4", "Install Requirements",      "▣"),
                ("5", "Troubleshooting",           "!!"),
                ("0", "Kembali",                   "↩"),
            ],
        )

        pilihan = input_prompt("Pilih bantuan", default="0")

        if pilihan == "1":
            _menu_quick_tutorial()
        elif pilihan == "2":
            _help_github()
        elif pilihan == "3":
            _help_structure()
        elif pilihan == "4":
            _help_requirements()
        elif pilihan == "5":
            _help_troubleshooting()
        elif pilihan == "0":
            break


def _help_github():
    clear_screen()
    print_banner(compact=True)
    print()
    section_title("CARA SETUP GITHUB", emoji="⚑")
    print()

    print(f"""  {C_MOSS_1}Kenapa GitHub?{C_RESET}
  {C_WHITE}Biar galeri lu bisa diakses online (GitHub Pages),{C_RESET}
  {C_WHITE}bukan cuma di HP sendiri.{C_RESET}

  {C_MOSS_1}━━━ LANGKAH ━━━{C_RESET}

  {C_GREEN}1. Daftar GitHub{C_RESET}
     Buka: {C_MOSS_3}https://github.com/signup{C_RESET}

  {C_GREEN}2. Bikin Repository{C_RESET}
     Klik "+" di kanan atas → "New repository"
     Nama: {C_SILVER}galeri-foto{C_RESET} (atau bebas)
     Public (biar Pages gratis)

  {C_GREEN}3. Bikin Personal Access Token{C_RESET}
     Buka: {C_MOSS_3}https://github.com/settings/tokens{C_RESET}
     Klik "Generate new token (classic)"
     Scope: centang {C_GREEN}repo{C_RESET} (full)
     {C_YELLOW}Salin token (format: ghp_xxx). Cuma muncul SEKALI!{C_RESET}

  {C_GREEN}4. Isi di Lumoss{C_RESET}
     Menu 7: Edit Konfigurasi
       • GitHub Username
       • GitHub Repo
       • GitHub Token
       • GitHub Branch (default: main)

  {C_GREEN}5. Aktifin GitHub Pages{C_RESET}
     Buka repo → Settings → Pages
     Source: main, Folder: / (root)
     Save
     Tunggu 1-2 menit → galeri online di:
     {C_MOSS_3}https://USERNAME.github.io/NAMA-REPO/{C_RESET}

  {C_MOSS_1}━━━ NEXT ━━━{C_RESET}

  Setelah semua siap:
  Menu 6: Tools → 1. Upload HTML ke GitHub
""")
    press_enter()


def _help_structure():
    clear_screen()
    print_banner(compact=True)
    print()
    section_title("STRUKTUR FOLDER", emoji="▣")
    print()

    print(f"""  {C_MOSS_1}Struktur project Lumoss (v7.2.6):{C_RESET}

  {C_SILVER}/storage/emulated/0/Project/lumoss/{C_RESET}
  │
  ├── ▪ lumoss.py             {C_SILVER}# Entry point{C_RESET}
  ├── ▪ menu.py               {C_SILVER}# Menu utama{C_RESET}
  ├── ▪ menu_account.py       {C_SILVER}# Submenu akun{C_RESET}
  ├── ▪ menu_tools.py         {C_SILVER}# Submenu tools{C_RESET}
  ├── ▪ menu_embed.py         {C_SILVER}# Submenu embed{C_RESET}
  ├── ▪ embed_parser.py       {C_SILVER}# Parser URL embed{C_RESET}
  ├── ▪ uploader.py           {C_SILVER}# Mesin upload{C_RESET}
  ├── ▪ media_processor.py    {C_SILVER}# Olah media{C_RESET}
  ├── ▪ html_builder.py       {C_SILVER}# Generate HTML{C_RESET}
  ├── ▪ tools.py              {C_SILVER}# Tools bantu{C_RESET}
  ├── ▪ ui_helpers.py         {C_SILVER}# Warna & tampilan{C_RESET}
  ├── ▪ account_manager.py    {C_SILVER}# Multi-account + onboarding helper{C_RESET}
  ├── ▪ config_manager.py     {C_SILVER}# Config{C_RESET}
  ├── ▪ requirements.txt      {C_SILVER}# Dependency{C_RESET}
  │
  ├── ▸ accounts/             {C_SILVER}# Config per akun{C_RESET}
  │   ├── ▪ active.json
  │   └── ▸ <slug>/
  │       └── ▪ config.json   {C_SILVER}# Config akun (media_dirs array){C_RESET}
  │
  ├── ▸ output/               {C_SILVER}# Hasil generate{C_RESET}
  │   └── ▸ <slug>/
  │       ├── ▪ index.html    {C_SILVER}# Galeri{C_RESET}
  │       ├── ▪ manager.html  {C_SILVER}# Manager{C_RESET}
  │       ├── ▪ embed.txt     {C_SILVER}# List URL embed{C_RESET}
  │       └── ▸ assets/
  │
  ├── ▸ cache/                {C_SILVER}# Cache & state{C_RESET}
  │   └── ▸ <slug>/
  │       ├── ▪ uploads_cache.json
  │       └── ▪ deleted.json
  │
  ├── ▸ templates/            {C_SILVER}# Template HTML{C_RESET}
  ├── ▸ docs/                 {C_SILVER}# Dokumentasi{C_RESET}
  └── ▸ backup/               {C_SILVER}# Backup{C_RESET}

  {C_MOSS_1}▸ Multi-Folder Media (v7.2.2):{C_RESET}

  {C_WHITE}Setiap akun punya array folder media:{C_RESET}

  {C_SILVER}config.json:{C_RESET}
    "media_dirs": [
      {{"path": "/storage/emulated/0/DCIM", "recursive": true}},
      {{"path": "/storage/emulated/0/Pictures", "recursive": true}}
    ]

  {C_WHITE}Cara kelola:{C_RESET}
    Menu 7 → 5. Kelola Folder Media

  {C_MOSS_1}▸ Auto-Convert Emoji (v7.2.6):{C_RESET}

  {C_WHITE}Semua emoji yang di-input user (nama akun, judul project){C_RESET}
  {C_WHITE}otomatis di-convert ke Unicode symbol.{C_RESET}

  {C_GREEN}Contoh:{C_RESET}
    💖 → ♥
    🚀 → ▶
    ✅ → ✓
    ❌ → ✗
    🔥 → ✦

  {C_YELLOW}KECUALI:{C_RESET} {LUMOSS_SYMBOL} — simbol utama Lumoss (gak di-convert)

  {C_MOSS_1}File penting:{C_RESET}

  {C_GREEN}lumoss.py{C_RESET} → File yang DIJALANKAN
  {C_GREEN}accounts/<slug>/config.json{C_RESET} → Config akun
  {C_GREEN}output/<slug>/index.html{C_RESET} → Galeri hasil generate
  {C_GREEN}cache/<slug>/uploads_cache.json{C_RESET} → Cache upload
""")
    press_enter()


def _help_requirements():
    clear_screen()
    print_banner(compact=True)
    print()
    section_title("INSTALL REQUIREMENTS", emoji="▣")
    print()

    print(f"""  {C_MOSS_1}Apa itu requirements.txt?{C_RESET}

  {C_WHITE}File yang isinya daftar library Python yang dibutuhin{C_RESET}
  {C_WHITE}Lumoss biar jalan lancar. Install sekali aja.{C_RESET}

  {C_MOSS_1}━━━ LIBRARY YANG DIBUTUHIN ━━━{C_RESET}

  {C_GREEN}▪ pillow{C_RESET}              {C_SILVER}Buat generate thumbnail{C_RESET}
  {C_GREEN}▪ requests{C_RESET}            {C_SILVER}Buat HTTP request ke Catbox.moe{C_RESET}
  {C_GREEN}▪ requests-toolbelt{C_RESET}  {C_SILVER}Buat upload multipart{C_RESET}

  {C_MOSS_1}━━━ CARA INSTALL ━━━{C_RESET}

  {C_GREEN}1. Buka Termux{C_RESET}

  {C_GREEN}2. Install Python (kalau belum):{C_RESET}
     {C_WHITE}pkg install python{C_RESET}

  {C_GREEN}3. Pindah ke folder Lumoss:{C_RESET}
     {C_WHITE}cd /storage/emulated/0/Project/lumoss{C_RESET}

  {C_GREEN}4. Install semua library:{C_RESET}
     {C_MOSS_3}pip install -r requirements.txt{C_RESET}

  {C_GREEN}5. Cek udah keinstall bener:{C_RESET}
     {C_WHITE}pip list | grep -E "pillow|requests"{C_RESET}

  {C_MOSS_1}━━━ TROUBLESHOOTING ━━━{C_RESET}

  {C_RED}✗ pip not found{C_RESET}
  {C_SILVER}Solusi:{C_RESET} pkg install python-pip

  {C_RED}✗ Permission denied{C_RESET}
  {C_SILVER}Solusi:{C_RESET} pip install --user -r requirements.txt

  {C_RED}✗ pillow error build{C_RESET}
  {C_SILVER}Solusi:{C_RESET} pkg install libjpeg-turbo libpng
                    pip install --upgrade pip wheel
                    pip install pillow
""")
    press_enter()


def _help_troubleshooting():
    clear_screen()
    print_banner(compact=True)
    print()
    section_title("TROUBLESHOOTING", emoji="!!")
    print()

    print(f"""  {C_RED}✗ ModuleNotFoundError{C_RESET}
  {C_SILVER}Penyebab:{C_RESET} Folder salah / dependency belum install
  {C_SILVER}Solusi:{C_RESET}
    • {C_WHITE}cd /storage/emulated/0/Project/lumoss{C_RESET}
    • {C_WHITE}pip install -r requirements.txt{C_RESET}

  {C_RED}✗ SyntaxError / IndentationError{C_RESET}
  {C_SILVER}Penyebab:{C_RESET} Copy-paste rusak
  {C_SILVER}Solusi:{C_RESET}
    • Cek indentasi (4 spasi konsisten)
    • Cek tanda kutip seimbang

  {C_RED}✗ Upload gagal / timeout{C_RESET}
  {C_SILVER}Penyebab:{C_RESET} Koneksi atau rate limit Catbox
  {C_SILVER}Solusi:{C_RESET}
    • Cek koneksi: {C_WHITE}ping catbox.moe{C_RESET}
    • Tunggu 1-2 menit
    • Fix cache: Tools → 3

  {C_RED}✗ Izin storage belum aktif{C_RESET}
  {C_SILVER}Penyebab:{C_RESET} Termux belum di-setup
  {C_SILVER}Solusi:{C_RESET} {C_WHITE}termux-setup-storage{C_RESET}

  {C_RED}✗ Folder media gak ketemu{C_RESET}
  {C_SILVER}Penyebab:{C_RESET} Folder dihapus / path berubah
  {C_SILVER}Solusi:{C_RESET}
    • Menu 7 → 5: cek/ubah folder media

  {C_MOSS_1}RESET TOTAL{C_RESET}
  Kalau bingung karena banyak error:
    {C_WHITE}rm -rf accounts/{C_RESET}    {C_SILVER}# hapus semua akun{C_RESET}
    {C_WHITE}rm -rf output/{C_RESET}      {C_SILVER}# hapus output{C_RESET}
    {C_WHITE}rm -rf cache/{C_RESET}       {C_SILVER}# hapus cache{C_RESET}
    {C_WHITE}python lumoss.py{C_RESET}    {C_SILVER}# mulai dari awal{C_RESET}
""")
    press_enter()


# ═══════════════════════════════════════════════════════════
# EXIT
# ═══════════════════════════════════════════════════════════

def _menu_exit():
    """Keluar dari Lumoss (v7.2.6 — pake 🌿)."""
    print()
    print(f"  {LUMOSS_SYMBOL} {C_MOSS_1}Sampai jumpa boss!{C_RESET}")
    print(f"  {C_SILVER}Makasih udah pake {PROJECT_NAME} {LUMOSS_SYMBOL}{C_RESET}")
    print()
    sys.exit(0)


# ═══════════════════════════════════════════════════════════
# SCAN MEDIA (v7.2.2 — multi-folder)
# ═══════════════════════════════════════════════════════════

def _scan_media_dirs(slug, paths=None):
    """Scan folder media (multi-folder)."""
    import json

    try:
        from media_processor import SUPPORTED_EXTENSIONS
    except ImportError:
        SUPPORTED_EXTENSIONS = {
            ".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp",
            ".mp4", ".mkv", ".webm", ".mov", ".avi",
        }

    from account_manager import _should_skip_path

    if paths is None:
        paths = am.get_account_paths(slug)

    cache_file = paths["cache"]
    media_dirs = cm.get_enabled_media_dirs(slug)

    cache = {}
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cache = json.load(f)
        except Exception:
            cache = {}

    total = 0
    total_size = 0
    ext_count = {}
    subfolders = {}
    subfolder_size = {}
    uploaded_count = 0
    uploaded_size = 0
    uploaded_list = []
    not_uploaded_count = 0
    not_uploaded_size = 0
    not_uploaded_list = []

    for md in media_dirs:
        source_path = md["path"]
        source_label = md.get("label", os.path.basename(source_path.rstrip("/")) or source_path)
        recursive = md.get("recursive", True)

        if not os.path.isdir(source_path):
            continue

        try:
            if recursive:
                walker = os.walk(source_path, followlinks=False)
            else:
                files_only = [
                    f for f in os.listdir(source_path)
                    if os.path.isfile(os.path.join(source_path, f))
                    and not _should_skip_path(os.path.join(source_path, f), is_dir=False)
                ]
                walker = [(source_path, [], files_only)]

            for root, dirs, files in walker:
                dirs[:] = [
                    d for d in dirs
                    if not _should_skip_path(os.path.join(root, d), is_dir=True)
                ]
                files = [
                    f for f in files
                    if not _should_skip_path(os.path.join(root, f), is_dir=False)
                ]

                rel = os.path.relpath(root, source_path)
                if rel != ".":
                    sub_key = f"{source_label}/{rel}"
                    subfolders.setdefault(sub_key, 0)
                    subfolder_size.setdefault(sub_key, 0)

                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    if ext not in SUPPORTED_EXTENSIONS:
                        continue

                    fpath = os.path.join(root, f)
                    try:
                        size = os.path.getsize(fpath)
                    except Exception:
                        size = 0

                    total += 1
                    total_size += size
                    ext_count[ext] = ext_count.get(ext, 0) + 1

                    if rel != ".":
                        sub_key = f"{source_label}/{rel}"
                        subfolders[sub_key] = subfolders.get(sub_key, 0) + 1
                        subfolder_size[sub_key] = subfolder_size.get(sub_key, 0) + size

                    rel_path_in_source = os.path.relpath(fpath, source_path).replace("\\", "/")
                    cache_key = f"{source_label}/{rel_path_in_source}"
                    cached_entry = cache.get(cache_key)
                    is_uploaded = False
                    if isinstance(cached_entry, dict):
                        is_uploaded = bool(cached_entry.get("url"))
                    elif isinstance(cached_entry, str):
                        is_uploaded = bool(cached_entry)

                    if is_uploaded:
                        uploaded_count += 1
                        uploaded_size += size
                        uploaded_list.append((cache_key, size, f))
                    else:
                        not_uploaded_count += 1
                        not_uploaded_size += size
                        not_uploaded_list.append((cache_key, size, f))
        except Exception:
            continue

    return {
        "total": total,
        "total_size": total_size,
        "ext_count": ext_count,
        "subfolders": subfolders,
        "subfolder_size": subfolder_size,
        "uploaded_count": uploaded_count,
        "uploaded_size": uploaded_size,
        "uploaded_list": uploaded_list,
        "not_uploaded_count": not_uploaded_count,
        "not_uploaded_size": not_uploaded_size,
        "not_uploaded_list": not_uploaded_list,
        "source_count": len(media_dirs),
    }


# ═══════════════════════════════════════════════════════════
# HELPER — FORMAT & ICON
# ═══════════════════════════════════════════════════════════

def _fmt_size(b):
    """Format bytes: MB / KB."""
    if b < 1024:
        return f"{b} B"
    elif b < 1024 ** 2:
        return f"{b / 1024:.0f} KB" if b >= 10240 else f"{b / 1024:.1f} KB"
    elif b < 1024 ** 3:
        return f"{b / (1024 ** 2):.1f} MB"
    else:
        return f"{b / (1024 ** 3):.2f} GB"


def _icon_for_ext(ext):
    ext = ext.lower()
    if ext in (".mp4", ".mkv", ".webm", ".mov", ".avi"):
        return "▶"
    if ext in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"):
        return "▣"
    if ext in (".html", ".htm"):
        return "◐"
    return "▪"


def _short_name(name, max_len=34):
    if len(name) <= max_len:
        return name
    stem, ext = os.path.splitext(name)
    keep = max(8, max_len - len(ext) - 3)
    return f"{stem[:keep]}...{ext}"


def _short_path(path, max_len=40):
    parts = path.replace("\\", "/").split("/")
    if len(parts) <= 1:
        return _short_name(path, max_len)
    filename = _short_name(parts[-1], max_len - min(12, len(parts[0]) + 2))
    prefix = f"{parts[-2]}/" if len(parts) >= 2 else ""
    result = prefix + filename
    if len(result) > max_len:
        result = _short_name(result, max_len)
    return result


# ═══════════════════════════════════════════════════════════
# HELPER — ROUNDED BOX (legacy — dipake di submenu)
# ═══════════════════════════════════════════════════════════

def _box_top(title, emoji="", width=30, color=None):
    color = color or C_MOSS_1
    label = f" {emoji} {title} " if emoji else f" {title} "
    visible_w = vwidth(label)
    dashes = max(0, width - visible_w - 2)
    return f"{color}╭─{label}{'─' * dashes}╮{C_RESET}"


def _box_line(content, width=30, color=None, prefix="│ "):
    color = color or C_SILVER
    visible_w = vwidth(content)
    inner_w = width - 2
    prefix_vis = vwidth(prefix)
    pad = inner_w - prefix_vis - visible_w
    return f"{color}│{C_RESET} {prefix}{content}{' ' * max(0, pad)}{color}│{C_RESET}"


def _box_bot(width=30, color=None):
    color = color or C_MOSS_1
    return f"{color}╰{'─' * (width - 2)}╯{C_RESET}"


def _box_empty(width=30, color=None):
    color = color or C_SILVER
    return f"{color}│{' ' * (width - 2)}│{C_RESET}"


def _two_column_box(
    title_l, emoji_l, lines_l,
    title_r, emoji_r, lines_r,
    width_l=32, width_r=33, gap=1,
):
    top_l = _box_top(title_l, emoji_l, width_l)
    top_r = _box_top(title_r, emoji_r, width_r)
    print(f"  {top_l}{' ' * gap}{top_r}")

    max_lines = max(len(lines_l), len(lines_r))
    for i in range(max_lines):
        content_l = lines_l[i] if i < len(lines_l) else ""
        content_r = lines_r[i] if i < len(lines_r) else ""
        line_l = _box_line(content_l, width_l)
        line_r = _box_line(content_r, width_r)
        print(f"  {line_l}{' ' * gap}{line_r}")

    bot_l = _box_bot(width_l)
    bot_r = _box_bot(width_r)
    print(f"  {bot_l}{' ' * gap}{bot_r}")


# ═══════════════════════════════════════════════════════════
# HELPER — SMOOTH BAR
# ═══════════════════════════════════════════════════════════

def _smooth_bar(pct, width=20):
    pct = max(0, min(100, pct))
    filled = int(width * pct / 100)
    empty = width - filled

    if pct >= 100:
        bar_fill = f"{C_MOSS_1}{'█' * filled}{C_RESET}"
    elif pct >= 50:
        bar_fill = f"{C_MOSS_1}{'█' * filled}{C_RESET}"
    else:
        bar_fill = f"{C_MOSS_2}{'█' * filled}{C_RESET}"

    bar_empty = f"{C_SILVER}{'░' * empty}{C_RESET}"
    return f"{bar_fill}{bar_empty}"


# ═══════════════════════════════════════════════════════════
# HELPER — ESTIMASI WAKTU
# ═══════════════════════════════════════════════════════════

def _estimate_time(total_bytes, file_count=1, cfg=None):
    if total_bytes <= 0 or file_count <= 0:
        return "—"

    upload_cfg = (cfg or {}).get("upload", {}) if isinstance(cfg, dict) else {}

    rate_kbps = upload_cfg.get("assumed_rate_kbps", 500)
    thumb_time = upload_cfg.get("thumbnail_time_estimate", 2.5)
    overhead = upload_cfg.get("overhead_estimate", 5)
    delay_between = upload_cfg.get("delay_between_files", 2)
    batch_every = upload_cfg.get("batch_pause_every", 30)
    batch_seconds = upload_cfg.get("batch_pause_seconds", 60)

    rate_bps = rate_kbps * 1024
    upload_secs = total_bytes / max(1, rate_bps)
    thumb_secs = thumb_time * file_count
    delay_secs = delay_between * file_count
    batch_pauses = file_count // max(1, batch_every)
    batch_secs = batch_seconds * batch_pauses

    total_secs = upload_secs + thumb_secs + delay_secs + batch_secs + overhead

    if total_secs < 60:
        return f"~{int(total_secs)} detik"
    mins = int(total_secs) // 60
    secs = int(total_secs) % 60
    if mins < 60:
        return f"~{mins}m {secs}s"
    hours = mins // 60
    mins = mins % 60
    return f"~{hours}j {mins}m"


# ═══════════════════════════════════════════════════════════
# HELPER — CHECKLIST
# ═══════════════════════════════════════════════════════════

def _build_checklist(scan, cfg):
    items = [
        f"Upload {scan['not_uploaded_count']} file ke Catbox.moe",
        "Generate thumbnail otomatis",
        "Update galeri index.html",
        "Sync cache lokal",
        "Verify URL aktif",
    ]

    gh_auto = cfg.get("github_auto_upload", False)
    gh_user = (cfg.get("github_username") or "").strip()
    gh_repo = (cfg.get("github_repo") or "").strip()

    if gh_auto and gh_user and gh_repo:
        items.append("Upload ke GitHub Pages")

    return items


# ═══════════════════════════════════════════════════════════
# RENDER — GATE BANNER
# ═══════════════════════════════════════════════════════════

def _render_gate_banner(slug, scan):
    n_wait = scan["not_uploaded_count"]
    if n_wait > 0:
        right = f"{n_wait} file nunggu • {LUMOSS_VERSION}"
    else:
        right = f"semua udah keupload • {LUMOSS_VERSION}"

    left = f"{C_MOSS_1}{C_BOLD}{LUMOSS_SYMBOL} {LUMOSS_GATE_TITLE}{C_RESET}"
    left_vis = vwidth(f"{LUMOSS_SYMBOL} {LUMOSS_GATE_TITLE}")
    right_vis = vwidth(right)

    total, _, _, _ = layout_widths()
    gap = max(1, total - left_vis - right_vis - 2)

    print(f"  {left}{' ' * gap}{C_MOSS_3}{right}{C_RESET}")
    print(f"  {C_MOSS_1}{'━' * total}{C_RESET}")
    print()

    print(f"  {C_SILVER}▸{C_RESET} {C_WHITE}Menu Utama{C_RESET}  {C_SILVER}›{C_RESET}  {C_WHITE}Cek Folder Media{C_RESET}")
    print(f"  {C_SILVER}▸{C_RESET} {C_MOSS_3}{scan['source_count']} folder media{C_RESET}")
    print()


# ═══════════════════════════════════════════════════════════
# RENDER — DASHBOARD
# ═══════════════════════════════════════════════════════════

def _render_dashboard(scan, media_dirs):
    left_lines = [
        f"{C_SILVER}▪ Total file {C_RESET} {C_SILVER}:{C_RESET} {C_WHITE}{scan['total']}{C_RESET}",
        f"{C_SILVER}= Total size {C_RESET} {C_SILVER}:{C_RESET} {C_MOSS_1}{_fmt_size(scan['total_size'])}{C_RESET}",
        f"{C_SILVER}▸ Sumber     {C_RESET} {C_SILVER}:{C_RESET} {C_WHITE}{scan['source_count']} folder{C_RESET}",
    ]
    subs = sorted(scan["subfolders"].items(), key=lambda x: -x[1])[:3]
    for i, (sub, cnt) in enumerate(subs):
        branch = "├─" if i < len(subs) - 1 else "└─"
        name = sub if len(sub) <= 14 else sub[:13] + "…"
        left_lines.append(
            f"{C_SILVER}  {branch}{C_RESET} {C_MOSS_3}{name}{C_RESET}  {C_SILVER}({cnt} file){C_RESET}"
        )

    pct = int((scan["uploaded_count"] / scan["total"]) * 100) if scan["total"] > 0 else 0
    bar = _smooth_bar(pct, 21)

    right_lines = [
        f"{C_GREEN}✓ Sudah {C_RESET} {C_SILVER}:{C_RESET} {C_WHITE}{scan['uploaded_count']} file{C_RESET} {C_SILVER}({_fmt_size(scan['uploaded_size'])}){C_RESET}",
        f"{C_YELLOW}◷ Belum {C_RESET} {C_SILVER}:{C_RESET} {C_WHITE}{scan['not_uploaded_count']} file{C_RESET} {C_SILVER}({_fmt_size(scan['not_uploaded_size'])}){C_RESET}",
        "",
        f"{C_SILVER}Progress upload:{C_RESET}",
        f"{bar} {C_BOLD}{C_WHITE}{pct}%{C_RESET}",
    ]

    render_merged_box(
        title="STATISTIK & STATUS",
        emoji="▤",
        sections=[
            {"title": "STATISTIK MEDIA", "emoji": "▤", "lines": left_lines},
            {"title": "STATUS UPLOAD",   "emoji": "~", "lines": right_lines},
        ],
    )
    print()

    _render_rincian_file(scan)
    _render_kategori(scan)
    _render_belum_upload(scan)


def _render_rincian_file(scan):
    print(f"  {C_MOSS_1}▪ Rincian file{C_RESET} {C_SILVER}(max 10 dari {scan['total']}){C_RESET}")
    print(f"  {C_MOSS_1}{'─' * 60}{C_RESET}")

    all_files = []
    for rel_path, size, fname in scan["not_uploaded_list"][:10]:
        ext = os.path.splitext(fname)[1]
        all_files.append((rel_path, size, fname, ext, False))
    remaining_slots = 10 - len(all_files)
    if remaining_slots > 0:
        for rel_path, size, fname in scan["uploaded_list"][:remaining_slots]:
            ext = os.path.splitext(fname)[1]
            all_files.append((rel_path, size, fname, ext, True))

    if not all_files:
        print(f"  {C_SILVER}(belum ada file){C_RESET}")
        print()
        return

    for rel_path, size, fname, ext, is_up in all_files[:10]:
        icon = _icon_for_ext(ext)
        short = _short_path(rel_path, 34)
        size_str = _fmt_size(size)
        status = f"{C_GREEN}✓{C_RESET}" if is_up else f"{C_YELLOW}◷{C_RESET}"
        print(
            f"  {icon}  {C_WHITE}{short:<34}{C_RESET} "
            f"{status}   "
            f"{C_SILVER}{size_str:>8}{C_RESET}"
        )

    remaining = scan["total"] - len(all_files[:10])
    if remaining > 0:
        print(f"  {C_SILVER}…{C_RESET}  {C_SILVER}+{remaining} file lainnya{C_RESET}")
    print()


def _render_kategori(scan):
    if not scan["subfolders"]:
        return

    print(f"  {C_MOSS_1}▸ Kategori{C_RESET}")
    print(f"  {C_MOSS_1}{'─' * 60}{C_RESET}")

    subs = sorted(scan["subfolders"].items(), key=lambda x: -x[1])
    max_cnt = max(cnt for _, cnt in subs) if subs else 1

    for sub, cnt in subs[:6]:
        name = sub if len(sub) <= 14 else sub[:13] + "…"
        bar_w = 14
        filled = int(bar_w * cnt / max_cnt)
        bar = f"{C_MOSS_1}{'█' * filled}{C_SILVER}{'░' * (bar_w - filled)}{C_RESET}"
        sub_size = scan.get("subfolder_size", {}).get(sub, 0)
        print(
            f"  {C_MOSS_3}▸ {name:<14}{C_RESET} "
            f"{C_SILVER}({cnt:>2} file){C_RESET}  "
            f"{C_SILVER}{_fmt_size(sub_size):>8}{C_RESET}  "
            f"{bar}"
        )
    print()


def _render_belum_upload(scan):
    if scan["not_uploaded_count"] == 0:
        print(f"  {C_GREEN}✓ Semua file udah keupload bosque!{C_RESET}")
        print()
        return

    print(f"  {C_MOSS_1}▪ Belum diupload{C_RESET} {C_SILVER}({scan['not_uploaded_count']} file){C_RESET}")
    print(f"  {C_MOSS_1}{'─' * 60}{C_RESET}")

    for rel_path, size, fname in scan["not_uploaded_list"][:10]:
        short = _short_path(rel_path, 40)
        size_str = _fmt_size(size)
        print(
            f"  {C_YELLOW}•{C_RESET} {C_WHITE}{short:<40}{C_RESET} "
            f"{C_SILVER}{size_str:>8}{C_RESET}"
        )

    remaining = scan["not_uploaded_count"] - 10
    if remaining > 0:
        print(f"  {C_SILVER}… (+{remaining} file lainnya){C_RESET}")
    print()


# ═══════════════════════════════════════════════════════════
# RENDER — PIPELINE PREVIEW
# ═══════════════════════════════════════════════════════════

def _render_pipeline_preview(scan):
    n = scan["not_uploaded_count"]
    if n == 0:
        return

    print(f"  {C_MOSS_1}▶ PIPELINE :: UPLOAD{C_RESET} {C_SILVER}— {n} file bakal diupload{C_RESET}")
    print(f"  {C_MOSS_1}{'─' * 60}{C_RESET}")
    print()

    WINDOW = 15
    files = scan["not_uploaded_list"]

    if n <= WINDOW:
        shown = files
    else:
        shown = files[:WINDOW]

    for i, (rel_path, size, fname) in enumerate(shown, start=1):
        short = _short_path(rel_path, 30)
        size_str = _fmt_size(size)
        print(
            f"  {C_SILVER}○━━━{C_RESET} "
            f"{C_SILVER}{i:>3}/{n}{C_RESET}  "
            f"{C_WHITE}{short:<30}{C_RESET}  "
            f"{C_SILVER}{size_str:>8}{C_RESET}"
        )

    if n > WINDOW:
        print(f"  {C_SILVER}…{C_RESET}  {C_SILVER}+{n - WINDOW} file lainnya{C_RESET}")

    print()
    print(f"  {C_SILVER}▸{C_RESET} {C_SILVER}0 selesai  •  {n} antri{C_RESET}")
    print()


# ═══════════════════════════════════════════════════════════
# RENDER — VERIFICATION GATE
# ═══════════════════════════════════════════════════════════

def _render_verification_gate(scan):
    try:
        cfg = cm.load_config()
    except Exception:
        cfg = {}

    checklist = _build_checklist(scan, cfg)
    total_bytes = scan["not_uploaded_size"]
    file_count = scan["not_uploaded_count"]
    est = _estimate_time(total_bytes, file_count, cfg)

    print(f"  {C_MOSS_1}{'━' * 60}{C_RESET}")
    print(f"  {C_MOSS_1}{C_BOLD}│  VERIFIKASI OPERASI{C_RESET}")
    print()

    print(f"  {C_SILVER}Sistem akan melakukan:{C_RESET}")
    print()
    for item in checklist:
        print(f"    {C_GREEN}✓{C_RESET}  {C_WHITE}{item}{C_RESET}")
    print()

    print(f"  {C_MOSS_1}{'─' * 52}{C_RESET}")
    print(f"  {C_SILVER}Total     {C_RESET} {C_SILVER}:{C_RESET}  {C_MOSS_1}{_fmt_size(total_bytes)}{C_RESET}")
    print(f"  {C_SILVER}Estimasi  {C_RESET} {C_SILVER}:{C_RESET}  {C_MOSS_2}{est}{C_RESET}")
    print(f"  {C_SILVER}Target    {C_RESET} {C_SILVER}:{C_RESET}  {C_WHITE}catbox.moe{C_RESET}")
    print(f"  {C_MOSS_1}{'─' * 52}{C_RESET}")
    print()

    print(f"  {C_MOSS_1}│{C_RESET}  {C_WHITE}{C_BOLD}Upload, atau batalin?{C_RESET}")
    print()
    print(f"  {C_SILVER}│{C_RESET}  {C_GREEN}[Enter]{C_RESET} {C_SILVER}Eksekusi{C_RESET}")
    print(f"  {C_SILVER}│{C_RESET}  {C_YELLOW}[n]{C_RESET}     {C_SILVER}Batalin{C_RESET}")
    print(f"  {C_SILVER}│{C_RESET}  {C_SILVER}[q]{C_RESET}     {C_SILVER}Keluar{C_RESET}")
    print()


# ═══════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════

__all__ = [
    "run_menu",
    "LUMOSS_VERSION",
    "_menu_regenerate",
    "_render_regenerate_banner",
    "_render_regenerate_gate",
]