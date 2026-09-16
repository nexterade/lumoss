"""
lumoss — Menu Import Embed (v7.2.2 MEDIA GARDEN)
Submenu buat kelola embed.txt (list URL dari source lain: YouTube, IG, FB, TikTok, dll).

Changelog v7.2.2:
- REBRANDING: amuv7 → lumoss
- UPDATE: Path display pake output/<slug>/embed.txt
- UPDATE: Banner LUMOSS (bukan AMUV7)

Fitur:
- Lihat isi embed.txt (formatted)
- Tambah URL baru (1 per baris, validasi)
- Hapus URL (by index)
- Clear semua
- Preview embed di browser (buat test)
- Auto-format dari share link (YouTube watch → embed, dll)

Format file: 1 URL per baris, komentar pake # (skip)
"""

import os
import sys

from ui_helpers import (
    C_RESET, C_BOLD, C_GREEN, C_YELLOW, C_RED, C_WHITE,
    C_MOSS_1, C_MOSS_2, C_MOSS_3, C_SILVER,
    clear_screen, print_banner, print_breadcrumb, print_section,
    print_success, print_error, print_warning, print_info,
    input_prompt, input_yes_no, input_int,
    press_enter, confirm_action,
    divider, section_title, kv_line, menu_item,
    print_menu_card,
    print_success_aesthetic, print_error_aesthetic,
    print_warning_aesthetic, print_info_aesthetic,
)

import account_manager as am


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════

def run_embed_menu():
    """Menu utama import embed."""
    while True:
        clear_screen()
        print_banner(compact=True)
        print_breadcrumb(["Menu Utama", "Import Embed"])

        slug = am.get_active_slug()
        if not slug:
            print_warning_aesthetic("Belum ada akun aktif bosque 😅")
            press_enter()
            return

        paths = am.get_account_paths(slug)
        embed_file = paths["embed_txt"]

        _render_embed_header(slug, embed_file)
        _render_embed_stats(embed_file)
        print()

        print_menu_card(
            title="IMPORT EMBED",
            emoji="◐",
            items=[
                ("1", "Lihat List URL",         "📋"),
                ("2", "Tambah URL Baru",        "➕"),
                ("3", "Hapus URL",              "🗑️"),
                ("4", "Bersihkan Semua",        "🧹"),
                ("5", "Test Preview",           "🔍"),
                ("6", "Buka embed.txt (editor)", "✎"),
                ("0", "Kembali ke Menu Utama",  "↩️"),
            ],
        )

        pilihan = input_prompt("Pilih menu", default="0")

        if pilihan == "1":
            _menu_list_urls(embed_file)
        elif pilihan == "2":
            _menu_add_url(embed_file)
        elif pilihan == "3":
            _menu_delete_url(embed_file)
        elif pilihan == "4":
            _menu_clear_all(embed_file)
        elif pilihan == "5":
            _menu_test_preview(embed_file)
        elif pilihan == "6":
            _menu_open_editor(embed_file)
        elif pilihan == "0":
            break
        else:
            print_error_aesthetic("Pilihan lu ngaco cuy 😂")
            press_enter()


# ═══════════════════════════════════════════════════════════
# HEADER & STATS
# ═══════════════════════════════════════════════════════════

def _render_embed_header(slug, embed_file):
    """Header: breadcrumb + path file."""
    print()
    print(f"  {C_MOSS_1}{C_BOLD}◐ LUMOSS :: IMPORT EMBED{C_RESET}  {C_MOSS_3}v7.2.2{C_RESET}")
    print(f"  {C_MOSS_1}{'━' * 60}{C_RESET}")
    print()
    print(f"  {C_SILVER}▸{C_RESET} {C_WHITE}Menu Utama{C_RESET}  {C_SILVER}›{C_RESET}  {C_WHITE}Import Embed{C_RESET}")
    print(f"  {C_SILVER}▪{C_RESET} {C_MOSS_3}output/{slug}/embed.txt{C_RESET}")
    print()
    print(f"  {C_SILVER}Tambah URL dari YouTube, Instagram, Facebook, TikTok,{C_RESET}")
    print(f"  {C_SILVER}atau direct link (jpg/mp4). 1 URL per baris.{C_RESET}")
    print()


def _render_embed_stats(embed_file):
    """Statistik: total URL, file ada/tidak."""
    lines = _read_embed_lines(embed_file)
    urls = [ln for ln in lines if ln and not ln.startswith("#")]
    comments = [ln for ln in lines if ln.startswith("#")]

    exists = os.path.exists(embed_file)
    size_kb = 0
    if exists:
        try:
            size_kb = os.path.getsize(embed_file) / 1024
        except Exception:
            pass

    print(f"  {C_MOSS_1}▤ Statistik embed.txt{C_RESET}")
    print(f"  {C_MOSS_1}{'─' * 60}{C_RESET}")
    if exists:
        print(f"  {C_SILVER}Status file  {C_RESET} {C_SILVER}:{C_RESET} {C_GREEN}✓ ada{C_RESET}")
        print(f"  {C_SILVER}Ukuran       {C_RESET} {C_SILVER}:{C_RESET} {C_WHITE}{size_kb:.1f} KB{C_RESET}")
    else:
        print(f"  {C_SILVER}Status file  {C_RESET} {C_SILVER}:{C_RESET} {C_YELLOW}▫️ belum dibuat{C_RESET}")
    print(f"  {C_SILVER}Total URL    {C_RESET} {C_SILVER}:{C_RESET} {C_MOSS_1}{len(urls)}{C_RESET}")
    if comments:
        print(f"  {C_SILVER}Komentar     {C_RESET} {C_SILVER}:{C_RESET} {C_SILVER}{len(comments)}{C_RESET}")


# ═══════════════════════════════════════════════════════════
# READ / WRITE
# ═══════════════════════════════════════════════════════════

def _read_embed_lines(embed_file):
    """Baca embed.txt → list baris (raw)."""
    if not os.path.exists(embed_file):
        return []
    try:
        with open(embed_file, "r", encoding="utf-8") as f:
            return [ln.rstrip("\n").rstrip("\r") for ln in f.readlines()]
    except Exception:
        return []


def _write_embed_lines(embed_file, lines):
    """Tulis embed.txt (atomic)."""
    os.makedirs(os.path.dirname(embed_file) or ".", exist_ok=True)
    tmp = embed_file + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        if lines:
            f.write("\n")
    os.replace(tmp, embed_file)


# ═══════════════════════════════════════════════════════════
# MENU 1: LIST URL
# ═══════════════════════════════════════════════════════════

def _menu_list_urls(embed_file):
    """Tampilkan list URL (formatted)."""
    clear_screen()
    print_banner(compact=True)
    print()
    section_title("LIST URL EMBED", emoji="📋")
    print()

    lines = _read_embed_lines(embed_file)
    if not lines:
        print_warning_aesthetic("embed.txt masih kosong bosque")
        print_info_aesthetic(f"Tambah URL via menu 2, atau edit manual: {embed_file}")
        press_enter()
        return

    url_idx = 0
    for i, ln in enumerate(lines, 1):
        stripped = ln.strip()
        if not stripped:
            print(f"  {C_SILVER}   {i:>3}.  (baris kosong){C_RESET}")
            continue
        if stripped.startswith("#"):
            print(f"  {C_SILVER}   {i:>3}.  {stripped}{C_RESET}")
            continue

        url_idx += 1
        url_type = _detect_url_type(stripped)
        type_icon = _type_icon(url_type)
        type_color = {
            "youtube": C_RED,
            "instagram": C_YELLOW,
            "facebook": C_MOSS_3,
            "tiktok": C_MOSS_1,
            "image": C_MOSS_2,
            "video": C_MOSS_2,
            "unknown": C_SILVER,
        }.get(url_type, C_SILVER)

        short_url = stripped if len(stripped) <= 60 else stripped[:57] + "..."
        print(f"  {C_MOSS_1}{url_idx:>3}.{C_RESET} {type_icon} {type_color}{short_url}{C_RESET}")

    print()
    total = sum(1 for ln in lines if ln.strip() and not ln.strip().startswith("#"))
    print_info_aesthetic(f"Total: {total} URL aktif")
    press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 2: ADD URL
# ═══════════════════════════════════════════════════════════

def _menu_add_url(embed_file):
    """Tambah URL baru."""
    clear_screen()
    print_banner(compact=True)
    print()
    section_title("TAMBAH URL BARU", emoji="➕")
    print()

    print(f"  {C_SILVER}Support:{C_RESET}")
    print(f"    {C_MOSS_3}•{C_RESET} {C_WHITE}YouTube:{C_RESET}    https://www.youtube.com/watch?v=xxx")
    print(f"    {C_MOSS_3}•{C_RESET} {C_WHITE}Instagram:{C_RESET}  https://www.instagram.com/p/xxx/")
    print(f"    {C_MOSS_3}•{C_RESET} {C_WHITE}Facebook:{C_RESET}   https://www.facebook.com/watch?v=xxx")
    print(f"    {C_MOSS_3}•{C_RESET} {C_WHITE}TikTok:{C_RESET}     https://www.tiktok.com/@user/video/xxx")
    print(f"    {C_MOSS_3}•{C_RESET} {C_WHITE}Direct IMG:{C_RESET} https://example.com/foto.jpg")
    print(f"    {C_MOSS_3}•{C_RESET} {C_WHITE}Direct VID:{C_RESET} https://example.com/video.mp4")
    print()

    url = input_prompt("🔗 URL", default="", allow_empty=True).strip()
    if not url:
        print_warning_aesthetic("URL kosong, dibatalin")
        press_enter()
        return

    if not (url.startswith("http://") or url.startswith("https://")):
        print_error_aesthetic("URL harus dimulai dengan http:// atau https://")
        press_enter()
        return

    url_type = _detect_url_type(url)
    print()
    kv_line("Tipe", url_type.upper(), value_color=C_MOSS_1)
    print()

    if not input_yes_no("Tambah URL ini?", default="y"):
        print_info_aesthetic("Dibatalin 😌")
        press_enter()
        return

    lines = _read_embed_lines(embed_file)

    if not lines:
        lines = [
            "# lumoss — embed.txt",
            "# 1 URL per baris. Baris mulai dengan # = komentar.",
            "# Format: URL langsung atau share link (YouTube/IG/FB/TikTok)",
            "",
        ]

    for ln in lines:
        if ln.strip() == url:
            print_warning_aesthetic("URL udah ada di list bosque")
            press_enter()
            return

    lines.append(url)
    try:
        _write_embed_lines(embed_file, lines)
        print_success_aesthetic("URL ditambah! ✓")
    except Exception as e:
        print_error_aesthetic(f"Gagal nulis: {e}")

    press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 3: DELETE URL
# ═══════════════════════════════════════════════════════════

def _menu_delete_url(embed_file):
    """Hapus URL by index."""
    clear_screen()
    print_banner(compact=True)
    print()
    section_title("HAPUS URL", emoji="🗑️")
    print()

    lines = _read_embed_lines(embed_file)
    urls_with_idx = []
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s and not s.startswith("#"):
            urls_with_idx.append((i, s))

    if not urls_with_idx:
        print_warning_aesthetic("Belum ada URL buat dihapus")
        press_enter()
        return

    for n, (real_idx, url) in enumerate(urls_with_idx, 1):
        short = url if len(url) <= 60 else url[:57] + "..."
        print(f"  {C_MOSS_1}{n:>3}.{C_RESET} {C_WHITE}{short}{C_RESET}")

    print()
    print(f"  {C_SILVER} 0.{C_RESET} {C_SILVER}Batal{C_RESET}")
    print()

    pilihan = input_int(
        f"Pilih nomor (1-{len(urls_with_idx)})",
        default=0,
        min_val=0,
        max_val=len(urls_with_idx),
    )

    if pilihan == 0:
        return

    real_idx, url = urls_with_idx[pilihan - 1]
    print()
    print_info_aesthetic(f"URL: {url[:70]}")

    if not input_yes_no(f"{C_YELLOW}Yakin hapus?{C_RESET}", default="n"):
        print_info_aesthetic("Dibatalin 😌")
        press_enter()
        return

    del lines[real_idx]
    try:
        _write_embed_lines(embed_file, lines)
        print_success_aesthetic("URL dihapus! 🗑️")
    except Exception as e:
        print_error_aesthetic(f"Gagal nulis: {e}")

    press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 4: CLEAR ALL
# ═══════════════════════════════════════════════════════════

def _menu_clear_all(embed_file):
    """Hapus semua URL (simpen komentar aja)."""
    clear_screen()
    print_banner(compact=True)
    print()
    section_title("BERSIHKAN SEMUA", emoji="🧹")
    print()

    lines = _read_embed_lines(embed_file)
    if not lines:
        print_info_aesthetic("embed.txt udah kosong / belum ada")
        press_enter()
        return

    urls = [ln for ln in lines if ln.strip() and not ln.strip().startswith("#")]
    if not urls:
        print_info_aesthetic("Gak ada URL aktif, cuma komentar")
        press_enter()
        return

    print_warning_aesthetic(f"Bakal hapus {len(urls)} URL dari embed.txt")
    print_info_aesthetic("Komentar (#) tetap disimpen")

    if not input_yes_no(f"{C_RED}Yakin?{C_RESET}", default="n"):
        print_info_aesthetic("Dibatalin 😌")
        press_enter()
        return

    try:
        import shutil as _sh
        _sh.copy(embed_file, embed_file + ".bak")
        print_info_aesthetic(f"Backup: embed.txt.bak")
    except Exception:
        pass

    new_lines = [ln for ln in lines if ln.strip().startswith("#") or not ln.strip()]
    try:
        _write_embed_lines(embed_file, new_lines)
        print_success_aesthetic(f"Bersih! {len(urls)} URL dihapus")
    except Exception as e:
        print_error_aesthetic(f"Gagal nulis: {e}")

    press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 5: TEST PREVIEW
# ═══════════════════════════════════════════════════════════

def _menu_test_preview(embed_file):
    """Test preview: tampilin URL yang bakal jadi embed."""
    clear_screen()
    print_banner(compact=True)
    print()
    section_title("TEST PREVIEW", emoji="🔍")
    print()

    try:
        from embed_parser import parse_embed_line
    except ImportError:
        print_error_aesthetic("embed_parser.py belum ada")
        print_info_aesthetic("Bikin dulu file embed_parser.py")
        press_enter()
        return

    lines = _read_embed_lines(embed_file)
    urls = [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("#")]

    if not urls:
        print_warning_aesthetic("Belum ada URL")
        press_enter()
        return

    print_info_aesthetic(f"Parse {len(urls)} URL...\n")

    ok_count = 0
    fail_count = 0

    for i, url in enumerate(urls, 1):
        try:
            parsed = parse_embed_line(url, index=i, slug="preview")
            if parsed:
                ok_count += 1
                embed_url = parsed.get("url", "")
                short_embed = embed_url if len(embed_url) <= 55 else embed_url[:52] + "..."
                print(f"  {C_GREEN}✓{C_RESET} {C_MOSS_1}{i:>3}.{C_RESET} {C_WHITE}{parsed.get('type', '?'):>7}{C_RESET}  {C_MOSS_3}{short_embed}{C_RESET}")
            else:
                fail_count += 1
                print(f"  {C_RED}✗{C_RESET} {C_MOSS_1}{i:>3}.{C_RESET} {C_SILVER}parse return None{C_RESET}")
        except Exception as e:
            fail_count += 1
            print(f"  {C_RED}✗{C_RESET} {C_MOSS_1}{i:>3}.{C_RESET} {C_RED}{type(e).__name__}: {str(e)[:50]}{C_RESET}")

    print()
    print(f"  {C_MOSS_1}✓ OK:{C_RESET} {C_WHITE}{ok_count}{C_RESET}")
    if fail_count:
        print(f"  {C_RED}✗ Gagal:{C_RESET} {C_WHITE}{fail_count}{C_RESET}")

    press_enter()


# ═══════════════════════════════════════════════════════════
# MENU 6: OPEN EDITOR
# ═══════════════════════════════════════════════════════════

def _menu_open_editor(embed_file):
    """Kasih info path embed.txt biar bisa diedit manual."""
    clear_screen()
    print_banner(compact=True)
    print()
    section_title("BUKA DI EDITOR", emoji="✎")
    print()

    if not os.path.exists(embed_file):
        print_warning_aesthetic("embed.txt belum ada")
        print_info_aesthetic("Bikin via menu 2, atau bikin manual")
        press_enter()
        return

    print(f"  {C_SILVER}Buka file ini di editor manapun:{C_RESET}")
    print()
    print(f"  {C_MOSS_1}{embed_file}{C_RESET}")
    print()
    print(f"  {C_SILVER}Atau via Termux:{C_RESET}")
    print(f"    {C_WHITE}nano {embed_file}{C_RESET}")
    print(f"    {C_WHITE}vim {embed_file}{C_RESET}")
    print()

    if input_yes_no("Coba buka pake nano?", default="n"):
        try:
            os.system(f"nano {embed_file}")
        except Exception as e:
            print_error_aesthetic(f"Gagal buka editor: {e}")
            press_enter()

    press_enter()


# ═══════════════════════════════════════════════════════════
# HELPERS — URL DETECTION
# ═══════════════════════════════════════════════════════════

def _detect_url_type(url):
    """Deteksi tipe URL sederhana (buat display)."""
    u = url.lower()
    if "youtube.com" in u or "youtu.be" in u:
        return "youtube"
    if "instagram.com" in u:
        return "instagram"
    if "facebook.com" in u or "fb.watch" in u:
        return "facebook"
    if "tiktok.com" in u:
        return "tiktok"
    if u.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp")):
        return "image"
    if u.endswith((".mp4", ".mkv", ".webm", ".mov", ".avi")):
        return "video"
    return "unknown"


def _type_icon(url_type):
    """Icon per tipe URL."""
    return {
        "youtube": "▶️",
        "instagram": "📷",
        "facebook": "📘",
        "tiktok": "🎵",
        "image": "🖼️",
        "video": "🎬",
        "unknown": "◐",
    }.get(url_type, "◐")


# ═══════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════

__all__ = ["run_embed_menu"]