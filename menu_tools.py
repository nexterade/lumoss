"""
lumoss — Menu Tools & Utilities (v7.2.2 MEDIA GARDEN)
Submenu buat tools bantu dengan cursor-positioning & visual alignment.

Changelog v7.2.2:
- REBRANDING: amuv7 → lumoss
- FIX: Panggilan tools.*() pake slug (bukan path)
- FIX: Hapus paths["about_html"]
- FIX: bot@amuv7.local → bot@lumoss.local
"""

import os

from ui_helpers import (
    C_RESET, C_BOLD, C_GREEN, C_YELLOW, C_RED, C_WHITE,
    C_MOSS_1, C_MOSS_2, C_MOSS_3, C_SILVER,
    clear_screen, print_banner, print_breadcrumb, print_section,
    print_success, print_error, print_warning, print_info,
    input_prompt, input_yes_no, input_int,
    press_enter, confirm_action, print_table, format_bytes, mask_secret,
    divider, section_title, kv_line, menu_item,
    print_account_card, print_menu_card,
    print_success_aesthetic, print_error_aesthetic,
    print_warning_aesthetic, print_info_aesthetic,
)

import account_manager as am
import config_manager as cm
import tools


# ═══════════════════════════════════════════════════════════
# MENU UTAMA TOOLS
# ═══════════════════════════════════════════════════════════

def run_tools_menu():
    """Menu utama tools."""
    while True:
        clear_screen()
        print_banner(compact=True)
        print_breadcrumb(["Menu Utama", "Tools & Utilities"])

        _print_active_summary()

        print_menu_card(
            title="TOOLS & UTILITIES",
            emoji="⚒",
            items=[
                ("1", "Upload HTML ke GitHub",   "📤"),
                ("2", "Backup Project (zip)",    "="),
                ("3", "Fix Broken Cache",        "🔧"),
                ("4", "Cleanup Thumbnail Lama",  "🧹"),
                ("5", "Hapus Cache Upload",      "🗑️"),
                ("6", "Reset Blacklist",         "↻"),
                ("7", "Statistik Cache",         "▤"),
                ("0", "Kembali ke Menu Utama",   "↩️"),
            ],
        )

        pilihan = input_prompt("Pilih tool", default="0")

        if pilihan == "1":
            _menu_upload_github()
        elif pilihan == "2":
            _menu_backup_project()
        elif pilihan == "3":
            _menu_fix_cache()
        elif pilihan == "4":
            _menu_cleanup_thumbnails()
        elif pilihan == "5":
            _menu_clear_cache()
        elif pilihan == "6":
            _menu_reset_blacklist()
        elif pilihan == "7":
            _menu_cache_stats()
        elif pilihan == "0":
            break
        else:
            print_error_aesthetic("Pilihan lu ngaco cuy 😅")
            press_enter()


# ═══════════════════════════════════════════════════════════
# TAMPILAN AKUN AKTIF
# ═══════════════════════════════════════════════════════════

def _print_active_summary():
    """Tampilkan ringkasan akun aktif."""
    slug = am.get_active_slug()

    if not slug:
        print(f"  {C_YELLOW}⚠\033[7GBelum ada akun aktif. Bikin dulu di Account Manager.{C_RESET}\n")
        return

    info = am.get_account_info(slug) or {}
    stats = am.get_account_stats(slug)
    name = info.get("name", slug)

    print(
        f"  {C_MOSS_1}◉\033[6GAkun aktif{C_RESET}  {C_SILVER}›{C_RESET}  "
        f"{C_WHITE}{C_BOLD}{name}{C_RESET}  "
        f"{C_SILVER}({slug}) — {stats['files']} file · {stats['size_human']}{C_RESET}\n"
    )


# ═══════════════════════════════════════════════════════════
# MENU 1: UPLOAD GITHUB
# ═══════════════════════════════════════════════════════════

def _menu_upload_github():
    """Upload file HTML ke GitHub."""
    print()
    section_title("UPLOAD KE GITHUB", emoji="📤")
    print()

    slug = am.get_active_slug()
    if not slug:
        print_warning_aesthetic("Belum ada akun aktif bosque")
        press_enter()
        return

    cfg = cm.load_config()

    gh_user = cfg.get("github_username", "").strip()
    gh_repo = cfg.get("github_repo", "").strip()
    gh_token = cfg.get("github_token", "").strip()
    gh_branch = cfg.get("github_branch", "main")

    if not gh_user or not gh_repo:
        print_warning_aesthetic("GitHub username / repo belum diisi di config")
        print_info_aesthetic("Setup GitHub di menu 7 (Edit Konfigurasi)")
        press_enter()
        return

    kv_line("Username", gh_user)
    kv_line("Repo", gh_repo)
    kv_line("Branch", gh_branch)
    kv_line("Token", "(ada)" if gh_token else "(TIDAK ADA — perlu untuk private repo)", value_color=C_SILVER)
    print()
    divider()

    paths = am.get_account_paths(slug)
    files_check = {
        "index.html": paths["index_html"],
        "manager.html": paths["manager_html"],
    }

    existing_files = {k: v for k, v in files_check.items() if os.path.exists(v)}

    if not existing_files:
        print_warning_aesthetic("Belum ada file HTML. Jalankan upload dulu (menu 1)")
        press_enter()
        return

    print()
    print(f"  {C_MOSS_1}File yang bakal di-upload:{C_RESET}")
    print()
    for name, path in existing_files.items():
        size_kb = os.path.getsize(path) / 1024
        print(f"    {C_GREEN}✓{C_RESET}\033[10G{C_WHITE}{name}{C_RESET} {C_SILVER}({size_kb:.1f} KB){C_RESET}")
    print()

    if not input_yes_no("Gas upload ke GitHub?", default="y"):
        print_info_aesthetic("Yaudah dibatalin 😴")
        press_enter()
        return

    print()
    ok, msg = tools.upload_to_github(cfg, files_to_upload=list(existing_files.keys()), slug=slug)

    print()
    if ok:
        print_success_aesthetic(msg)
    else:
        print_error_aesthetic(msg)

    press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 2: BACKUP PROJECT
# ═══════════════════════════════════════════════════════════

def _menu_backup_project():
    """Backup file penting ke zip."""
    print()
    section_title("BACKUP PROJECT", emoji="=")
    print()

    print_info_aesthetic("Backup berisi: file .py + config akun")
    print_info_aesthetic("TIDAK termasuk media (biar ringan)")
    print()

    if not input_yes_no("Gas backup?", default="y"):
        print_info_aesthetic("Yaudah dibatalin 😴")
        press_enter()
        return

    print()
    slug = am.get_active_slug()
    ok, msg = tools.backup_project(slug=slug)

    print()
    if ok:
        print_success_aesthetic(f"Backup berhasil: {msg}")
    else:
        print_error_aesthetic(msg)

    press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 3: FIX CACHE
# ═══════════════════════════════════════════════════════════

def _menu_fix_cache():
    """Fix cache entri rusak."""
    print()
    section_title("FIX BROKEN CACHE", emoji="🔧")
    print()

    slug = am.get_active_slug()
    if not slug:
        print_warning_aesthetic("Belum ada akun aktif bosque")
        press_enter()
        return

    paths = am.get_account_paths(slug)
    cache_file = paths["cache"]

    if not os.path.exists(cache_file):
        print_warning_aesthetic(f"File cache gak ada: {cache_file}")
        print_info_aesthetic("Belum ada upload. Jalankan upload dulu")
        press_enter()
        return

    print()
    ok, msg = tools.fix_broken_cache(slug=slug)

    print()
    if ok:
        print_success_aesthetic(msg)
    else:
        print_error_aesthetic(msg)

    press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 4: CLEANUP THUMBNAILS
# ═══════════════════════════════════════════════════════════

def _menu_cleanup_thumbnails():
    """Hapus thumbnail lama."""
    print()
    section_title("CLEANUP THUMBNAIL LAMA", emoji="🧹")
    print()

    print_info_aesthetic("Thumbnail lama (>30 hari) bakal dihapus")
    print_info_aesthetic("Thumbnail bakal digenerate ulang otomatis saat upload berikutnya")
    print()

    max_age = input_int(
        "Hapus thumbnail lebih lama dari (hari)",
        default=30,
        min_val=1,
        max_val=365,
    )

    print()
    if not input_yes_no(f"Hapus thumbnail >{max_age} hari?", default="y"):
        print_info_aesthetic("Yaudah dibatalin 😴")
        press_enter()
        return

    print()
    ok, msg = tools.cleanup_thumbnails(max_age)

    print()
    if ok:
        print_success_aesthetic(msg)
    else:
        print_error_aesthetic(msg)

    press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 5: CLEAR CACHE
# ═══════════════════════════════════════════════════════════

def _menu_clear_cache():
    """Hapus cache upload."""
    print()
    section_title("HAPUS CACHE UPLOAD", emoji="🗑️")
    print()

    slug = am.get_active_slug()
    if not slug:
        print_warning_aesthetic("Belum ada akun aktif bosque")
        press_enter()
        return

    paths = am.get_account_paths(slug)
    cache_file = paths["cache"]

    if not os.path.exists(cache_file):
        print_warning_aesthetic(f"File cache gak ada: {cache_file}")
        press_enter()
        return

    stats = tools.cache_stats(slug=slug)

    kv_line("Total file", str(stats["files"]))
    kv_line("Valid", str(stats["valid"]), value_color=C_GREEN)
    kv_line("Broken", str(stats["broken"]), value_color=C_RED)
    kv_line("Total size", stats["size_human"])
    print()
    divider()

    print()
    print_warning_aesthetic("Kalau cache dihapus, semua file bakal di-upload ULANG")
    print_warning_aesthetic("Ini bisa makan waktu & kuota. Yakin?")
    print()

    if not input_yes_no(f"{C_RED}Hapus cache {slug}?{C_RESET}", default="n"):
        print_info_aesthetic("Yaudah dibatalin 😌")
        press_enter()
        return

    if not input_yes_no(f"{C_RED}Yakin 100%? (cache bakal hilang){C_RESET}", default="n"):
        print_info_aesthetic("Yaudah dibatalin 😌")
        press_enter()
        return

    print()
    ok, msg = tools.clear_upload_cache(slug=slug)

    print()
    if ok:
        print_success_aesthetic(msg)
        print_info_aesthetic("Backup disimpen di: uploads_cache.json.bak")
    else:
        print_error_aesthetic(msg)

    press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 6: RESET BLACKLIST
# ═══════════════════════════════════════════════════════════

def _menu_reset_blacklist():
    """Reset blacklist (deleted.json)."""
    print()
    section_title("RESET BLACKLIST", emoji="↻")
    print()

    slug = am.get_active_slug()
    if not slug:
        print_warning_aesthetic("Belum ada akun aktif bosque")
        press_enter()
        return

    paths = am.get_account_paths(slug)
    deleted_file = paths["deleted"]

    if not os.path.exists(deleted_file):
        print_info_aesthetic("Blacklist kosong / belum ada file")
        press_enter()
        return

    import json
    try:
        with open(deleted_file, "r", encoding="utf-8") as f:
            deleted = json.load(f)
        count = len(deleted)
    except Exception:
        count = 0

    if count == 0:
        print_info_aesthetic("Blacklist kosong bosque")
        press_enter()
        return

    print_warning_aesthetic(f"Blacklist berisi {count} item")
    print_info_aesthetic("Item ini bakal muncul lagi di galeri setelah reset")
    print()
    print_info_aesthetic("File blacklist bakal di-backup ke: deleted.json.bak")
    print()

    ok, msg = tools.reset_blacklist(slug=slug)

    print()
    if ok:
        print_success_aesthetic(msg)
    else:
        print_error_aesthetic(msg)

    press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 7: CACHE STATS
# ═══════════════════════════════════════════════════════════

def _menu_cache_stats():
    """Tampilkan statistik cache."""
    print()
    section_title("STATISTIK CACHE", emoji="▤")
    print()

    slug = am.get_active_slug()
    if not slug:
        print_warning_aesthetic("Belum ada akun aktif bosque")
        press_enter()
        return

    paths = am.get_account_paths(slug)
    cache_file = paths["cache"]

    if not os.path.exists(cache_file):
        print_warning_aesthetic("File cache belum ada (belum upload)")
        press_enter()
        return

    stats = tools.cache_stats(slug=slug)

    kv_line("Akun", slug, value_color=C_MOSS_2)
    kv_line("Total file", str(stats["files"]))
    kv_line("Valid", str(stats["valid"]), value_color=C_GREEN)
    kv_line("Broken", str(stats["broken"]), value_color=C_RED)
    kv_line("Total size", stats["size_human"])
    print()
    divider()

    if stats["broken"] > 0:
        print()
        print_warning_aesthetic(f"Ada {stats['broken']} entri rusak. Jalankan menu 3 (Fix Cache)")

    press_enter()


# ═══════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════

__all__ = ["run_tools_menu"]