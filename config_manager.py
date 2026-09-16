"""
lumoss — Config Manager (v7.2.2)
Mengelola config.json per akun + global_config.json.

Changelog v7.2.2:
- BREAKING: Tambah field `media_dirs` (array) — ganti `photos_dir` (string)
- Tambah field: `photos_mode` (single/multiple)
- Tambah field: `output_mode` (auto/custom/legacy)
- Tambah field: `output_custom_dir`
- Tambah helper: get_media_dirs(), set_media_dirs()
- Backward compat: `photos_dir` masih dibaca kalau `media_dirs` kosong
"""

import os
import json

from account_manager import (
    get_account_paths,
    get_active_slug,
    has_accounts,
)

# ═══════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════

GLOBAL_CONFIG_FILE = "global_config.json"

# Default config untuk setiap akun (kalau config.json tidak ada)
DEFAULT_ACCOUNT_CONFIG = {
    "userhash": "",
    "judul_project": "lumoss",
    "counter_namespace": "lumoss-default",
    "media_dirs": [],                 # v7.2.2: array folder media
    "photos_mode": "multiple",        # single | multiple
    "photos_dir": "",                 # legacy — fallback kalau media_dirs kosong
    "output_mode": "auto",            # auto | custom | legacy
    "output_custom_dir": "",          # dipake kalau output_mode = custom
    "workers": 1,
    "verify_cached_urls": False,
    "upload_thumbnails": True,
    "output_html": "index.html",
    "output_manager": "manager.html",
    "items_per_page": 24,
    "github_username": "",
    "github_repo": "",
    "github_token": "",
    "github_branch": "main",
    "github_auto_upload": False,
}

# Default global config
DEFAULT_GLOBAL_CONFIG = {
    "version": "7.2.2",
    "build_date": "2026-09-15",
    "theme": {
        "default": "moss",
        "available": ["moss", "dark", "light", "amoled", "midnight", "sunset"],
    },
    "layout": {
        "default": "mosaic",
        "available": ["mosaic", "grid"],
    },
    "gallery": {
        "items_per_page": 24,
        "infinite_scroll_default": True,
        "mosaic_row_unit_px": 8,
        "mosaic_min_column_px": 160,
    },
    "autoplay": {
        "gallery_enabled": True,
        "gallery_mode": "auto",
        "gallery_visibility_threshold": 0.6,
        "gallery_debounce_ms": 300,
        "gallery_max_concurrent": 1,
        "lightbox_enabled": True,
        "muted": True,
        "loop": True,
        "video_preload": "metadata",
    },
    "features": {
        "enable_ocr": False,
        "enable_face_detect": False,
        "enable_color_tag": True,
        "enable_thumbnail": True,
        "enable_exif": True,
        "enable_auto_tag": True,
        "enable_embed_import": True,
    },
    "ocr": {
        "max_words": 3,
        "lang": "ind+eng",
        "min_image_size": 800,
    },
    "thumbnail": {
        "max_size_px": 720,
        "quality": 80,
        "format": "webp",
        "cleanup_max_age_days": 30,
    },
    "upload": {
        "workers": 1,
        "verify_cached_urls": False,
        "catbox_max_size_mb": 200,
        "batch_pause_every": 30,
        "batch_pause_seconds": 60,
        "retry_max": 3,
        "delay_between_files": 2,
        "thumbnail_time_estimate": 2.5,
        "overhead_estimate": 5,
        "assumed_rate_kbps": 500,
    },
}


# ═══════════════════════════════════════════════════════════
# LOW-LEVEL FILE OPS
# ═══════════════════════════════════════════════════════════

def _read_json(path, default=None):
    """Baca file JSON, return default kalau gagal."""
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _write_json(path, data):
    """Tulis file JSON secara atomic."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def _deep_merge(base, override):
    """Merge 2 dict secara rekursif."""
    result = dict(base)
    for key, val in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(val, dict):
            result[key] = _deep_merge(result[key], val)
        else:
            result[key] = val
    return result


# ═══════════════════════════════════════════════════════════
# GLOBAL CONFIG
# ═══════════════════════════════════════════════════════════

def load_global_config():
    """Baca global_config.json. Kalau gak ada → buat otomatis."""
    data = _read_json(GLOBAL_CONFIG_FILE)
    if data is None:
        try:
            _write_json(GLOBAL_CONFIG_FILE, DEFAULT_GLOBAL_CONFIG)
        except Exception:
            pass
        return dict(DEFAULT_GLOBAL_CONFIG)

    merged = _deep_merge(DEFAULT_GLOBAL_CONFIG, data)
    return merged


def save_global_config(cfg):
    """Simpan global config."""
    _write_json(GLOBAL_CONFIG_FILE, cfg)


def get_global_value(key_path, default=None):
    """Ambil nilai dari global config dengan dot notation."""
    cfg = load_global_config()
    keys = key_path.split(".")
    cur = cfg
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def set_global_value(key_path, value):
    """Set nilai global config dengan dot notation."""
    cfg = load_global_config()
    keys = key_path.split(".")
    cur = cfg
    for k in keys[:-1]:
        if k not in cur or not isinstance(cur[k], dict):
            cur[k] = {}
        cur = cur[k]
    cur[keys[-1]] = value
    save_global_config(cfg)


# ═══════════════════════════════════════════════════════════
# ACCOUNT CONFIG
# ═══════════════════════════════════════════════════════════

def get_config_path(slug=None):
    """Return path config.json untuk akun (atau akun aktif)."""
    paths = get_account_paths(slug)
    if not paths:
        return None
    return paths["config"]


def load_config(slug=None):
    """Baca config untuk akun (default: akun aktif)."""
    paths = get_account_paths(slug)
    if not paths:
        return dict(DEFAULT_ACCOUNT_CONFIG)

    config_path = paths["config"]
    if not os.path.exists(config_path):
        try:
            _write_json(config_path, DEFAULT_ACCOUNT_CONFIG)
        except Exception:
            pass
        return dict(DEFAULT_ACCOUNT_CONFIG)

    data = _read_json(config_path, default={})
    merged = _deep_merge(DEFAULT_ACCOUNT_CONFIG, data)
    return merged


def save_config(cfg, slug=None):
    """Simpan config untuk akun (default: akun aktif)."""
    config_path = get_config_path(slug)
    if not config_path:
        return False, "Belum ada akun aktif. Buat akun dulu."

    try:
        _write_json(config_path, cfg)
        return True, config_path
    except Exception as e:
        return False, f"Gagal simpan config: {e}"


def get_config_value(key, default=None, slug=None):
    """Ambil 1 nilai dari config akun."""
    cfg = load_config(slug)
    return cfg.get(key, default)


def set_config_value(key, value, slug=None):
    """Set 1 nilai di config akun + save."""
    cfg = load_config(slug)
    cfg[key] = value
    return save_config(cfg, slug)


def update_config(updates, slug=None):
    """Update beberapa key sekaligus."""
    cfg = load_config(slug)
    cfg.update(updates)
    return save_config(cfg, slug)


# ═══════════════════════════════════════════════════════════
# MEDIA DIRS (v7.2.2)
# ═══════════════════════════════════════════════════════════

def get_media_dirs(slug=None):
    """
    Ambil list folder media dari config.
    
    Returns:
        list dict [{path, recursive, enabled, label}, ...]
    """
    cfg = load_config(slug)
    media_dirs = cfg.get("media_dirs", [])

    if isinstance(media_dirs, list) and media_dirs:
        # Normalisasi
        result = []
        for item in media_dirs:
            if isinstance(item, str):
                result.append({
                    "path": item,
                    "recursive": True,
                    "enabled": True,
                    "label": os.path.basename(item.rstrip("/")) or item,
                })
            elif isinstance(item, dict):
                path = item.get("path", "").strip()
                if not path:
                    continue
                result.append({
                    "path": path,
                    "recursive": item.get("recursive", True),
                    "enabled": item.get("enabled", True),
                    "label": item.get("label", os.path.basename(path.rstrip("/")) or path),
                })
        return result

    # Backward compat: kalau media_dirs kosong, cek photos_dir
    legacy = cfg.get("photos_dir", "").strip()
    if legacy:
        return [{
            "path": legacy,
            "recursive": True,
            "enabled": True,
            "label": os.path.basename(legacy.rstrip("/")) or legacy,
        }]

    return []


def set_media_dirs(media_dirs, slug=None):
    """
    Set list folder media di config.
    
    Args:
        media_dirs: list dict atau list string
    """
    cfg = load_config(slug)

    # Normalisasi
    normalized = []
    for item in media_dirs:
        if isinstance(item, str):
            normalized.append({
                "path": item,
                "recursive": True,
                "enabled": True,
                "label": os.path.basename(item.rstrip("/")) or item,
            })
        elif isinstance(item, dict):
            path = item.get("path", "").strip()
            if not path:
                continue
            normalized.append({
                "path": path,
                "recursive": item.get("recursive", True),
                "enabled": item.get("enabled", True),
                "label": item.get("label", os.path.basename(path.rstrip("/")) or path),
            })

    cfg["media_dirs"] = normalized
    return save_config(cfg, slug)


def get_enabled_media_dirs(slug=None):
    """Ambil cuma folder media yang enabled."""
    dirs = get_media_dirs(slug)
    return [d for d in dirs if d.get("enabled", True)]


# ═══════════════════════════════════════════════════════════
# EFFECTIVE CONFIG
# ═══════════════════════════════════════════════════════════

def get_effective_config(slug=None):
    """Gabungkan global config + account config."""
    acc_cfg = load_config(slug)
    glob_cfg = load_global_config()
    effective = _deep_merge(glob_cfg, acc_cfg)
    return {
        "account": acc_cfg,
        "global": glob_cfg,
        "effective": effective,
    }


def get_items_per_page(slug=None):
    """Ambil items_per_page dari config akun (fallback ke global)."""
    acc_cfg = load_config(slug)
    if "items_per_page" in acc_cfg and acc_cfg["items_per_page"]:
        return acc_cfg["items_per_page"]
    return get_global_value("gallery.items_per_page", 24)


def get_photos_dir(slug=None):
    """
    DEPRECATED — pake get_media_dirs().
    Fallback: return folder pertama dari media_dirs.
    """
    dirs = get_enabled_media_dirs(slug)
    if dirs:
        return dirs[0]["path"]
    return ""


def get_output_paths(slug=None):
    """Return dict path output (index, manager, embed)."""
    paths = get_account_paths(slug)
    if not paths:
        return {
            "index": "index.html",
            "manager": "manager.html",
            "embed": "embed.txt",
        }
    return {
        "index": paths["index_html"],
        "manager": paths["manager_html"],
        "embed": paths["embed_txt"],
    }


# ═══════════════════════════════════════════════════════════
# VALIDATION & HELPERS
# ═══════════════════════════════════════════════════════════

def validate_config(cfg):
    """Validasi config akun. Return list warning (kosong = OK)."""
    warnings = []

    if not isinstance(cfg, dict):
        return ["Config bukan dict"]

    uh = cfg.get("userhash", "")
    if uh and not isinstance(uh, str):
        warnings.append("userhash harus string")
    elif uh and len(uh) < 10:
        warnings.append(f"userhash kelihatan terlalu pendek ({len(uh)} char)")

    w = cfg.get("workers", 1)
    if not isinstance(w, int) or w < 1 or w > 4:
        warnings.append(f"workers harus 1-4 (dapat: {w})")

    if not cfg.get("judul_project"):
        warnings.append("judul_project kosong")

    media_dirs = cfg.get("media_dirs", [])
    if not media_dirs:
        warnings.append("media_dirs kosong — minimal 1 folder")

    output_mode = cfg.get("output_mode", "auto")
    if output_mode not in ("auto", "custom", "legacy"):
        warnings.append(f"output_mode tidak valid: {output_mode}")

    if output_mode == "custom" and not cfg.get("output_custom_dir"):
        warnings.append("output_mode=custom tapi output_custom_dir kosong")

    return warnings


def config_summary(cfg):
    """Return string ringkasan config untuk display."""
    uh = cfg.get("userhash", "")
    if uh:
        uh_display = f"{uh[:6]}...{uh[-4:]}" if len(uh) > 10 else "•" * len(uh)
    else:
        uh_display = "(anonymous)"

    media_dirs = cfg.get("media_dirs", [])
    media_count = len(media_dirs) if isinstance(media_dirs, list) else 0

    lines = [
        f"Userhash    : {uh_display}",
        f"Judul       : {cfg.get('judul_project', '-')}",
        f"Media dirs  : {media_count} folder",
        f"Output mode : {cfg.get('output_mode', 'auto')}",
        f"Workers     : {cfg.get('workers', 1)}",
        f"Thumbnail   : {'ON' if cfg.get('upload_thumbnails') else 'OFF'}",
    ]
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
# THEME MANAGEMENT
# ═══════════════════════════════════════════════════════════

AVAILABLE_THEMES = [
    {"id": "moss",     "name": "Moss",      "emoji": "💚", "desc": "Luminous Moss (#2BEE34) — Default"},
    {"id": "dark",     "name": "Dark",      "emoji": "🌙", "desc": "Hitam elegan"},
    {"id": "light",    "name": "Light",     "emoji": "☀️", "desc": "Putih terang"},
    {"id": "amoled",   "name": "AMOLED",    "emoji": "⚫", "desc": "Hitam pekat (hemat baterai)"},
    {"id": "midnight", "name": "Midnight",  "emoji": "🌌", "desc": "Biru gelap malam"},
    {"id": "sunset",   "name": "Sunset",    "emoji": "🌅", "desc": "Oranye-pink hangat"},
]


def get_theme_default():
    """Ambil default theme dari global config."""
    return get_global_value("theme.default", "moss")


def set_theme_default(theme_id):
    """Set default theme di global config."""
    valid_ids = [t["id"] for t in AVAILABLE_THEMES]
    if theme_id not in valid_ids:
        return False, f"Tema '{theme_id}' tidak valid. Pilih: {', '.join(valid_ids)}"

    set_global_value("theme.default", theme_id)
    return True, f"Tema default: {theme_id}"


def list_available_themes():
    """Return list of available themes."""
    return AVAILABLE_THEMES


# ═══════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════

__all__ = [
    "GLOBAL_CONFIG_FILE",
    "DEFAULT_ACCOUNT_CONFIG", "DEFAULT_GLOBAL_CONFIG",
    # Global
    "load_global_config", "save_global_config",
    "get_global_value", "set_global_value",
    # Account
    "get_config_path", "load_config", "save_config",
    "get_config_value", "set_config_value", "update_config",
    # Media dirs (v7.2.2)
    "get_media_dirs", "set_media_dirs", "get_enabled_media_dirs",
    # Effective
    "get_effective_config",
    "get_items_per_page", "get_photos_dir", "get_output_paths",
    # Validation
    "validate_config", "config_summary",
    # Theme
    "AVAILABLE_THEMES", "get_theme_default", "set_theme_default", "list_available_themes",
]