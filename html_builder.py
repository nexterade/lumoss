"""
lumoss — HTML Builder (v7.2.2 MEDIA GARDEN)
Generate file HTML untuk galeri dari template dengan cursor-positioning & aesthetic styling.

Changelog v7.2.0:
- HAPUS: build_about_html() — About digabung ke gallery (Opsi C)
- HAPUS: ABOUT_TEMPLATE — template about.html udah gak dipake
- ADD: param default_theme di build_gallery_html() → inject DEFAULT_THEME ke JS
- ADD: param theme di build_manager_html() → konsisten sama gallery
- UPDATE: build_all() → cuma build 2 file (index + manager), pass theme
- FIX: import dibersihin (buang Path, datetime yang gak kepake)

Fitur:
- Load template dari templates/gallery.html, manager.html
- Inject data media (JSON) ke dalam script
- Generate index.html + manager.html
- Handle placeholder: DATA, ITEMS_PER_PAGE, PROJECT_TITLE, AUTOPLAY_CONFIG,
  DELETED, STATS, GITHUB_REPO, DEFAULT_THEME
"""

import os
import json

from ui_helpers import (
    C_RESET, C_GREEN, C_YELLOW, C_RED, C_WHITE,
    C_MOSS_1, C_MOSS_2, C_MOSS_3, C_SILVER,
    print_success, print_error, print_warning, print_info,
    format_bytes,
)


# ═══════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════

TEMPLATES_DIR = "templates"
GALLERY_TEMPLATE = os.path.join(TEMPLATES_DIR, "gallery.html")
MANAGER_TEMPLATE = os.path.join(TEMPLATES_DIR, "manager.html")

# v7.2.0: ABOUT_TEMPLATE udah gak dipake (About digabung ke gallery)


# ═══════════════════════════════════════════════════════════
# JSON ESCAPING (untuk inject di <script>)
# ═══════════════════════════════════════════════════════════

def escape_json_for_inline_script(obj):
    """Escape JSON biar aman dimasukin ke <script> tag."""
    s = json.dumps(obj, ensure_ascii=False)
    s = s.replace("</", "<\\/")
    s = s.replace("<!--", "<\\!--")
    s = s.replace("*/", "*\\/")
    s = s.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    return s


def escape_html(text):
    """Escape HTML entities."""
    if text is None:
        return ""
    s = str(text)
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace('"', "&quot;")
    s = s.replace("'", "&#39;")
    return s


# ═══════════════════════════════════════════════════════════
# TEMPLATE LOADING
# ═══════════════════════════════════════════════════════════

def _load_template(template_path):
    """Load template HTML dari file. Return string atau None."""
    if not os.path.exists(template_path):
        return None
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print_error(f"Gagal baca template\033[24G: {e}")
        return None


def _ensure_templates_dir():
    """Pastikan folder templates/ ada."""
    os.makedirs(TEMPLATES_DIR, exist_ok=True)


def _check_templates_exist():
    """Cek template yang dibutuhin ada. Return list missing.
    
    v7.2.0: about.html udah gak dicek (udah dihapus).
    """
    missing = []
    for name, path in [
        ("gallery.html", GALLERY_TEMPLATE),
        ("manager.html", MANAGER_TEMPLATE),
    ]:
        if not os.path.exists(path):
            missing.append(name)
    return missing


# ═══════════════════════════════════════════════════════════
# PLACEHOLDER REPLACEMENT
# ═══════════════════════════════════════════════════════════

def _replace_placeholders(html, replacements):
    """
    Replace placeholder `/*KEY*/` dengan value.
    
    Args:
        html: string template
        replacements: dict {key: value}
    
    Returns:
        string hasil
    """
    result = html
    for key, value in replacements.items():
        placeholder = f"/*{key}*/"
        result = result.replace(placeholder, str(value))
    return result


# ═══════════════════════════════════════════════════════════
# GALLERY BUILDER
# ═══════════════════════════════════════════════════════════

def build_gallery_html(
    media_data,
    project_title="amuv7",
    items_per_page=24,
    autoplay_config=None,
    theme="moss",
    default_theme=None,
    output_path="index.html",
    template_path=None,
):
    """
    Build file index.html dari template galeri.
    
    Args:
        media_data: list of dict item media
        project_title: judul project
        items_per_page: item per halaman
        autoplay_config: dict config autoplay
        theme: tema yang dipake (buat data-theme di <html>)
        default_theme: tema default buat JS fallback (kalau beda sama theme)
        output_path: path output
        template_path: override path template (optional)
    """
    if template_path is None:
        template_path = GALLERY_TEMPLATE

    if not media_data:
        return False, "Tidak ada data media untuk di-render."

    template = _load_template(template_path)
    if template is None:
        return False, f"Template tidak ditemukan\033[28G: {template_path}"

    if autoplay_config is None:
        autoplay_config = {
            "gallery_enabled": True,
            "gallery_mode": "auto",
            "gallery_visibility_threshold": 0.6,
            "gallery_debounce_ms": 300,
            "gallery_max_concurrent": 1,
            "lightbox_enabled": True,
            "muted": True,
            "loop": True,
            "video_preload": "metadata",
        }

    # v7.2.0: default_theme buat JS fallback (kalau beda dari theme yg dipake)
    if default_theme is None:
        default_theme = theme or "moss"

    json_data = escape_json_for_inline_script(media_data)
    json_autoplay = escape_json_for_inline_script(autoplay_config)
    json_title = json.dumps(project_title, ensure_ascii=False)
    json_default_theme = json.dumps(default_theme, ensure_ascii=False)

    replacements = {
        "DATA_PLACEHOLDER": json_data,
        "ITEMS_PER_PAGE_PLACEHOLDER": str(items_per_page),
        "PROJECT_TITLE_JS": json_title,
        "PROJECT_TITLE": escape_html(project_title),
        "AUTOPLAY_CONFIG_PLACEHOLDER": json_autoplay,
        "DEFAULT_THEME_PLACEHOLDER": json_default_theme,
    }

    rendered = _replace_placeholders(template, replacements)

    # Sinkronisasi tema awal: pastikan data-theme di <html> sesuai config
    target_theme = theme or "moss"
    for old_theme in ('data-theme="dark"', 'data-theme="light"', 'data-theme="moss"',
                      'data-theme="amoled"', 'data-theme="midnight"', 'data-theme="sunset"'):
        if old_theme in rendered:
            rendered = rendered.replace(old_theme, f'data-theme="{target_theme}"', 1)
            break

    # Save
    try:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        tmp = output_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(rendered)
        os.replace(tmp, output_path)

        size_kb = os.path.getsize(output_path) / 1024
        return True, f"{output_path} ({size_kb:.1f} KB, {len(media_data)} item)"
    except Exception as e:
        return False, f"Gagal simpan HTML\033[20G: {e}"


# ═══════════════════════════════════════════════════════════
# MANAGER BUILDER
# ═══════════════════════════════════════════════════════════

def build_manager_html(
    media_data,
    deleted_data=None,
    project_title="amuv7",
    theme="moss",
    output_path="manager.html",
    template_path=None,
):
    """
    Build file manager.html dari template.
    
    v7.2.0: tambah param `theme` biar konsisten sama gallery.
    """
    if template_path is None:
        template_path = MANAGER_TEMPLATE

    if not media_data:
        return False, "Tidak ada data media untuk di-render."

    template = _load_template(template_path)
    if template is None:
        return False, f"Template tidak ditemukan\033[28G: {template_path}"

    if deleted_data is None:
        deleted_data = {}

    json_data = escape_json_for_inline_script(media_data)
    json_deleted = escape_json_for_inline_script(deleted_data)
    json_title = json.dumps(project_title, ensure_ascii=False)

    replacements = {
        "DATA_PLACEHOLDER": json_data,
        "DELETED_PLACEHOLDER": json_deleted,
        "PROJECT_TITLE_JS": json_title,
        "PROJECT_TITLE": escape_html(project_title),
    }

    rendered = _replace_placeholders(template, replacements)

    # v7.2.0: sinkron tema
    target_theme = theme or "moss"
    for old_theme in ('data-theme="dark"', 'data-theme="light"', 'data-theme="moss"',
                      'data-theme="amoled"', 'data-theme="midnight"', 'data-theme="sunset"'):
        if old_theme in rendered:
            rendered = rendered.replace(old_theme, f'data-theme="{target_theme}"', 1)
            break

    try:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        tmp = output_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(rendered)
        os.replace(tmp, output_path)

        size_kb = os.path.getsize(output_path) / 1024
        return True, f"{output_path} ({size_kb:.1f} KB)"
    except Exception as e:
        return False, f"Gagal simpan manager HTML\033[28G: {e}"


# ═══════════════════════════════════════════════════════════
# BUILD ALL (CONVENIENCE)
# ═══════════════════════════════════════════════════════════

def build_all(
    media_data,
    output_dir,
    project_title="amuv7",
    items_per_page=24,
    autoplay_config=None,
    theme="moss",
    deleted_data=None,
    account_info=None,
    github_repo="",
):
    """
    Build 2 file (index + manager) sekaligus.
    
    v7.2.0: about.html udah gak di-build (digabung ke gallery).
    
    Returns:
        dict {filename: (success, message)}
    """
    missing = _check_templates_exist()
    if missing:
        return {
            "error": (False, f"Template missing: {', '.join(missing)}")
        }

    os.makedirs(output_dir, exist_ok=True)

    results = {}

    # 1. index.html (gallery + about section)
    index_path = os.path.join(output_dir, "index.html")
    ok, msg = build_gallery_html(
        media_data,
        project_title=project_title,
        items_per_page=items_per_page,
        autoplay_config=autoplay_config,
        theme=theme,
        default_theme=theme,
        output_path=index_path,
    )
    results["index.html"] = (ok, msg)

    # 2. manager.html
    manager_path = os.path.join(output_dir, "manager.html")
    ok, msg = build_manager_html(
        media_data,
        deleted_data=deleted_data,
        project_title=project_title,
        theme=theme,
        output_path=manager_path,
    )
    results["manager.html"] = (ok, msg)

    return results


# ═══════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════

__all__ = [
    "TEMPLATES_DIR", "GALLERY_TEMPLATE", "MANAGER_TEMPLATE",
    "escape_json_for_inline_script", "escape_html",
    "build_gallery_html", "build_manager_html", "build_all",
]