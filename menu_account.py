"""
lumoss — Menu Account Manager (v7.2.2 MEDIA GARDEN)
Submenu buat kelola akun Catbox dengan cursor-positioning & aesthetic styling.

Changelog v7.2.2:
- REBRANDING: amuv7 → lumoss
- FIX: _menu_create_account() — WAJIB pilih folder media (panggil am.pick_media_folders_onboarding)
- FIX: _menu_account_stats() — hapus paths["about_html"] (udah gak ada)
- UPDATE: display path — tambah output/, cache/
- UPDATE: create_account() panggil dengan media_dirs
"""

import os

from ui_helpers import (
    C_RESET, C_BOLD, C_GREEN, C_YELLOW, C_RED, C_WHITE,
    C_MOSS_1, C_MOSS_2, C_MOSS_3, C_SILVER, C_SILVER_LIGHT,
    clear_screen, print_banner, print_breadcrumb, print_section,
    print_success, print_error, print_warning, print_info,
    input_prompt, input_yes_no, input_int,
    press_enter, confirm_action, print_table, mask_secret,
    divider, section_title, kv_line, menu_item,
    print_account_card, print_menu_card,
    print_success_aesthetic, print_error_aesthetic,
    print_warning_aesthetic, print_info_aesthetic,
)

import account_manager as am
import config_manager as cm


# ═══════════════════════════════════════════════════════════
# MENU UTAMA ACCOUNT
# ═══════════════════════════════════════════════════════════

def run_account_menu():
    """Menu utama account manager (aesthetic mode)."""
    while True:
        clear_screen()
        print_banner(compact=True)
        print_breadcrumb(["Menu Utama", "Account Manager"])

        _print_active_account()

        print_menu_card(
            title="ACCOUNT MANAGER",
            emoji="❖",
            items=[
                ("1", "List Semua Akun",       "📋"),
                ("2", "Buat Akun Baru",        "➕"),
                ("3", "Ganti Akun Aktif",      "↻"),
                ("4", "Ganti Nama Akun",       "✏️"),
                ("5", "Hapus Akun",            "🗑️"),
                ("6", "Statistik Akun",        "▤"),
                ("0", "Kembali ke Menu Utama", "↩️"),
            ],
        )

        pilihan = input_prompt("Pilih menu", default="0")

        if pilihan == "1":
            _menu_list_accounts()
        elif pilihan == "2":
            _menu_create_account()
        elif pilihan == "3":
            _menu_switch_account()
        elif pilihan == "4":
            _menu_rename_account()
        elif pilihan == "5":
            _menu_delete_account()
        elif pilihan == "6":
            _menu_account_stats()
        elif pilihan == "0":
            break
        else:
            print_error_aesthetic("Pilihan lu ngaco cuy 😂")
            press_enter()


# ═══════════════════════════════════════════════════════════
# TAMPILAN AKUN AKTIF
# ═══════════════════════════════════════════════════════════

def _print_active_account():
    """Tampilkan card akun aktif."""
    slug = am.get_active_slug()

    if not slug:
        print()
        section_title("AKUN AKTIF", emoji="◉")
        print()
        print(f"  {C_YELLOW}⚠\033[7GBelum ada akun aktif bosque{C_RESET}")
        print(f"  {C_SILVER}    Bikin akun baru (menu 2) buat mulai{C_RESET}")
        print()
        divider()
        print()
        return

    info = am.get_account_info(slug) or {}
    stats = am.get_account_stats(slug)

    name = info.get("name", slug)
    uh = info.get("userhash_masked", "") or "(anonymous)"
    files_str = f"{stats['files']} ({stats['size_human']})"

    print_account_card(
        name=name,
        slug=slug,
        userhash=uh,
        files_str=files_str,
    )


# ═══════════════════════════════════════════════════════════
# MENU 1: LIST ACCOUNTS
# ═══════════════════════════════════════════════════════════

def _menu_list_accounts():
    """Tampilkan semua akun dalam tabel."""
    print()
    section_title("DAFTAR SEMUA AKUN", emoji="📋")
    print()

    accounts = am.list_accounts()

    if not accounts:
        print_warning_aesthetic("Belum ada akun bos. Bikin akun baru dulu (menu 2)")
        press_enter()
        return

    active_slug = am.get_active_slug()

    headers = ["", "Slug", "Nama", "Files", "Size"]
    rows = []

    for slug, info in accounts.items():
        marker = "✓" if slug == active_slug else "  "
        name = info.get("name", slug)[:20]
        stats = am.get_account_stats(slug)
        rows.append([
            marker,
            slug[:20],
            name,
            str(stats["files"]),
            stats["size_human"],
        ])

    print_table(headers, rows, col_widths=[2, 22, 22, 6, 10])
    print()
    print_info_aesthetic(f"Total: {len(accounts)} akun")
    print_info_aesthetic("✓ = akun yang lagi aktif")
    press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 2: CREATE ACCOUNT (v7.2.2 — WAJIB media_dirs)
# ═══════════════════════════════════════════════════════════

def _menu_create_account():
    """Form bikin akun baru (v7.2.2 — WAJIB pilih folder media)."""
    print()
    section_title("BUAT AKUN BARU", emoji="➕")
    print()

    print_info_aesthetic("Akun baru punya folder terisolasi sendiri")
    print_info_aesthetic("Config: accounts/<slug>/  •  Output: output/<slug>/  •  Cache: cache/<slug>/")
    print()

    name = input_prompt("🏷️  Nama akun (contoh: Catbox Utama)")
    if not name or not name.strip():
        print_error_aesthetic("Nama gak boleh kosong bosque 😅")
        press_enter()
        return
    name = name.strip()

    print()
    print(f"  {C_MOSS_1}✦ Userhash Catbox (opsional){C_RESET}")
    print(f"  {C_SILVER}   Kosongin buat anonymous{C_RESET}")
    print(f"  {C_SILVER}   Ambil di: https://catbox.moe/user/manage.php{C_RESET}")
    userhash = input_prompt("⚿ Userhash", default="", allow_empty=True)

    print()
    judul = input_prompt("✎ Judul project", default=name)

    # ── v7.2.2: WAJIB pilih folder media ──
    print()
    print(f"  {C_MOSS_1}{C_BOLD}▣ Pilih folder media (WAJIB){C_RESET}")
    print(f"  {C_SILVER}Foto/video lu bakal di-scan dari folder ini.{C_RESET}")
    print()
    press_enter("Tekan Enter buat mulai scan folder...")

    media_dirs = am.pick_media_folders_onboarding()
    if not media_dirs:
        print_warning_aesthetic("Yaudah dibatalin 😴")
        press_enter()
        return

    # ── Konfirmasi ──
    print()
    divider()
    print()
    kv_line("Nama", name)
    kv_line("Userhash", mask_secret(userhash) if userhash else "(anonymous)", value_color=C_SILVER)
    kv_line("Judul", judul)
    kv_line("Folder media", f"{len(media_dirs)} folder", value_color=C_MOSS_2)
    for md in media_dirs:
        print(f"  {C_SILVER}  • {md['path']}{C_RESET}")
    print()
    divider()
    print()

    if not input_yes_no("Gaskan bikin akun ini?", default="y"):
        print_warning_aesthetic("Yaudah dibatalin 😴")
        press_enter()
        return

    print()
    ok, result = am.create_account(name, userhash=userhash, judul=judul, media_dirs=media_dirs)

    if ok:
        slug = result
        print_success_aesthetic(f"Akun '{name}' udah jadi! ✦")
        print()
        kv_line("Slug", slug, value_color=C_MOSS_2)
        kv_line("Config", f"accounts/{slug}/config.json")
        kv_line("Output", f"output/{slug}/")
        kv_line("Cache", f"cache/{slug}/")
        kv_line("Media", f"{len(media_dirs)} folder", value_color=C_MOSS_1)

        if am.get_active_slug() == slug:
            print()
            print_info_aesthetic("Akun ini otomatis jadi AKTIF (akun pertama) 💪")
        else:
            print()
            print_info_aesthetic(f"Akun aktif sekarang: {am.get_active_slug()}")
            print_info_aesthetic("Ganti akun aktif lewat menu 3 kalau mau pake akun ini")
    else:
        print_error_aesthetic(f"Gagal bikin akun: {result}")

    press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 3: SWITCH ACCOUNT
# ═══════════════════════════════════════════════════════════

def _menu_switch_account():
    """Ganti akun aktif."""
    print()
    section_title("GANTI AKUN AKTIF", emoji="↻")
    print()

    accounts = am.list_accounts()

    if not accounts:
        print_warning_aesthetic("Belum ada akun bosque")
        press_enter()
        return

    current = am.get_active_slug()

    if len(accounts) == 1:
        print_warning_aesthetic("Cuma ada 1 akun. Bikin akun baru dulu buat switch")
        press_enter()
        return

    print_info_aesthetic(f"Akun aktif sekarang: {current}")
    print()

    slug_list = list(accounts.keys())
    for i, slug in enumerate(slug_list, 1):
        info = accounts[slug]
        marker = f" {C_MOSS_1}✓{C_RESET}" if slug == current else ""
        print(
            f"  {C_MOSS_1}{C_BOLD}{i:>2}{C_RESET}."
            f"\033[8G{C_WHITE}{info.get('name', slug)}{C_RESET}"
            f" {C_SILVER}({slug}){marker}{C_RESET}"
        )

    print()
    print(f"  {C_SILVER} 0.\033[8GBatal{C_RESET}")
    print()

    pilihan = input_int(f"Pilih akun (1-{len(slug_list)})", default=0, min_val=0, max_val=len(slug_list))

    if pilihan == 0:
        return

    target_slug = slug_list[pilihan - 1]

    if target_slug == current:
        print_info_aesthetic("Akun itu udah aktif bosque 😅")
        press_enter()
        return

    ok, msg = am.switch_account(target_slug)
    if ok:
        print_success_aesthetic(msg)
    else:
        print_error_aesthetic(msg)

    press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 4: RENAME ACCOUNT
# ═══════════════════════════════════════════════════════════

def _menu_rename_account():
    """Ganti nama tampilan akun."""
    print()
    section_title("GANTI NAMA AKUN", emoji="✏️")
    print()

    accounts = am.list_accounts()

    if not accounts:
        print_warning_aesthetic("Belum ada akun bosque")
        press_enter()
        return

    slug_list = list(accounts.keys())
    for i, slug in enumerate(slug_list, 1):
        info = accounts[slug]
        print(
            f"  {C_MOSS_1}{C_BOLD}{i:>2}{C_RESET}."
            f"\033[8G{C_WHITE}{info.get('name', slug)}{C_RESET}"
            f" {C_SILVER}({slug}){C_RESET}"
        )

    print()
    pilihan = input_int(f"Pilih akun (1-{len(slug_list)})", default=0, min_val=0, max_val=len(slug_list))

    if pilihan == 0:
        return

    slug = slug_list[pilihan - 1]
    old_name = accounts[slug].get("name", slug)

    print()
    print_info_aesthetic(f"Nama lama: {old_name}")
    new_name = input_prompt("Nama baru", default=old_name)

    if new_name == old_name:
        print_info_aesthetic("Nama gak berubah bosque")
        press_enter()
        return

    ok, msg = am.rename_account(slug, new_name)
    if ok:
        print_success_aesthetic(msg)
    else:
        print_error_aesthetic(msg)

    press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 5: DELETE ACCOUNT
# ═══════════════════════════════════════════════════════════

def _menu_delete_account():
    """Hapus akun (dengan konfirmasi)."""
    print()
    section_title("HAPUS AKUN", emoji="🗑️")
    print()

    accounts = am.list_accounts()

    if not accounts:
        print_warning_aesthetic("Belum ada akun bosque")
        press_enter()
        return

    if len(accounts) == 1:
        print_warning_aesthetic("Cuma ada 1 akun, gak bisa dihapus")
        print_info_aesthetic("Bikin akun baru dulu (menu 2), baru hapus yang lama")
        press_enter()
        return

    slug_list = list(accounts.keys())
    for i, slug in enumerate(slug_list, 1):
        info = accounts[slug]
        stats = am.get_account_stats(slug)
        print(
            f"  {C_MOSS_1}{C_BOLD}{i:>2}{C_RESET}."
            f"\033[8G{C_WHITE}{info.get('name', slug)}{C_RESET} "
            f"{C_SILVER}({slug}, {stats['files']} file, {stats['size_human']}){C_RESET}"
        )

    print()
    pilihan = input_int(f"Pilih akun (1-{len(slug_list)})", default=0, min_val=0, max_val=len(slug_list))

    if pilihan == 0:
        return

    slug = slug_list[pilihan - 1]
    info = accounts[slug]
    stats = am.get_account_stats(slug)

    print()
    print(f"  {C_RED}⚠\033[7GKONFIRMASI HAPUS AKUN{C_RESET}")
    print()
    kv_line("Nama", info.get("name", slug))
    kv_line("Slug", slug, value_color=C_MOSS_2)
    kv_line("Files", f"{stats['files']} file ({stats['size_human']})")
    print()

    if not input_yes_no(f"{C_YELLOW}Yakin hapus akun ini?{C_RESET}", default="n"):
        print_info_aesthetic("Yaudah dibatalin 😌")
        press_enter()
        return

    print()
    delete_files = input_yes_no(
        f"{C_YELLOW}Hapus folder akun juga? (config, cache, output){C_RESET}",
        default="y",
    )

    if delete_files:
        print_warning_aesthetic("FOLDER + semua file di dalemnya bakal DIHAPUS PERMANEN!")
        if not input_yes_no(f"{C_RED}Yakin 100%?{C_RESET}", default="n"):
            print_info_aesthetic("Yaudah dibatalin 😌")
            press_enter()
            return

    print()
    ok, msg = am.delete_account(slug, delete_files=delete_files)
    if ok:
        print_success_aesthetic(msg)
        if delete_files:
            print_info_aesthetic(f"Folder accounts/{slug}/, output/{slug}/, cache/{slug}/ udah dihapus")
        else:
            print_info_aesthetic(f"Folder {slug}/ disimpen (bisa restore manual)")
    else:
        print_error_aesthetic(msg)

    press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 6: ACCOUNT STATS (v7.2.2 — fix about_html)
# ═══════════════════════════════════════════════════════════

def _menu_account_stats():
    """Tampilkan statistik detail akun."""
    print()
    section_title("STATISTIK AKUN", emoji="▤")
    print()

    slug = am.get_active_slug()

    if not slug:
        print_warning_aesthetic("Belum ada akun aktif bosque")
        press_enter()
        return

    info = am.get_account_info(slug) or {}
    stats = am.get_account_stats(slug)

    kv_line("Nama", info.get("name", slug))
    kv_line("Slug", slug, value_color=C_MOSS_2)
    kv_line("Files", f"{stats['files']} file")
    kv_line("Total size", stats["size_human"], value_color=C_MOSS_1)
    kv_line("Created", info.get("created_at", "-"))
    kv_line("Last used", info.get("last_used") or "Belum pernah")
    print()
    divider()

    paths = am.get_account_paths(slug)
    if paths:
        print()
        print(f"  {C_MOSS_1}▣\033[7GFile penting:{C_RESET}")
        print()

        files_check = [
            ("config.json", paths["config"]),
            ("uploads_cache.json", paths["cache"]),
            ("deleted.json", paths["deleted"]),
            ("index.html", paths["index_html"]),
            ("manager.html", paths["manager_html"]),
            ("embed.txt", paths["embed_txt"]),
        ]

        for label, path in files_check:
            exists = os.path.exists(path)
            icon = f"{C_GREEN}✓{C_RESET}" if exists else f"{C_SILVER}▫️{C_RESET}"
            print(f"    {icon}\033[12G{C_WHITE}{label}{C_RESET}")

    # Media dirs info
    media_dirs = cm.get_enabled_media_dirs(slug)
    print()
    print(f"  {C_MOSS_1}▸\033[7GFolder media:{C_RESET}")
    print()
    for md in media_dirs:
        rec = "recursive" if md.get("recursive", True) else "top-level"
        print(f"    {C_GREEN}•{C_RESET} {C_WHITE}{md['path']}{C_RESET} {C_SILVER}({rec}){C_RESET}")

    press_enter()


# ═══════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════

__all__ = ["run_account_menu"]