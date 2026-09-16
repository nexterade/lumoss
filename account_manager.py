"""
lumoss — Account Manager (v7.2.2)
Mengelola multi-akun Catbox dengan folder terisolasi.

Changelog v7.2.2:
- BREAKING: Struktur folder baru — accounts/ (config), output/ (HTML), cache/ (state)
- get_account_paths() — tambah output_dir, cache_dir, embed_txt di output/
- create_account() — bikin folder output/ & cache/ juga
- delete_account() — hapus folder output/ & cache/ juga
- Tambah helper: _ensure_output_dir(), _ensure_cache_dir()
- Tambah fungsi: scan_available_media_folders() — auto-detect folder umum
- Tambah fungsi: scan_custom_folder() — scan folder manual
- Tambah fungsi: check_storage_permission() — cek izin Termux
- Tambah fungsi: pick_media_folders_onboarding() — onboarding pilih folder
- Tambah fungsi: _handle_no_folders() — handle kalau gak ada folder
- FIX: Skip folder & file hidden/sampah (.thumbnails, .cache, Android, dll)

Struktur:
    accounts/
    ├── active.json
    └── <slug>/
        └── config.json              # config akun (media_dirs array)
    
    output/
    └── <slug>/
        ├── index.html
        ├── manager.html
        └── embed.txt
    
    cache/
    └── <slug>/
        ├── uploads_cache.json
        └── deleted.json
"""

import os
import json
import re
import shutil
from datetime import datetime

# ═══════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════

ACCOUNTS_DIR = "accounts"
OUTPUT_DIR = "output"
CACHE_DIR = "cache"
ACTIVE_FILE = os.path.join(ACCOUNTS_DIR, "active.json")

ACCOUNT_FILES = {
    "config": "config.json",
}

OUTPUT_FILES = {
    "index_html": "index.html",
    "manager_html": "manager.html",
    "embed_txt": "embed.txt",
}

CACHE_FILES = {
    "cache": "uploads_cache.json",
    "deleted": "deleted.json",
}

# Placeholder strings yang bakal di-anggap anonymous
USERHASH_PLACEHOLDERS = {
    "",
    "harap diisi",
    "harap diisi agar tidak anonym",
    "harap diisi agar tidak anonim",
    "isi userhash",
    "isi userhash catbox",
    "kosong",
    "none",
    "null",
    "anonymous",
    "anon",
    "-",
    "n/a",
    "na",
    "belum diisi",
    "belum",
    "default",
}

# Folder umum Android yang di-scan buat onboarding
COMMON_MEDIA_FOLDERS = [
    "/storage/emulated/0/DCIM",
    "/storage/emulated/0/Pictures",
    "/storage/emulated/0/Movies",
    "/storage/emulated/0/Download",
    "/storage/emulated/0/WhatsApp/Media",
    "/storage/emulated/0/Telegram",
    "/storage/emulated/0/Instagram",
    "/storage/emulated/0/DCIM/Camera",
    "/storage/emulated/0/DCIM/Screenshots",
]

# v7.2.2 FIX: Folder & file yang di-SKIP saat scan
SKIP_FOLDER_NAMES = {
    ".thumbnails", ".thumbnail", ".cache", ".trash", ".temp", ".tmp",
    "Android", "LOST.DIR", "log", "logs", "cache", "temp", "tmp",
    "$RECYCLE.BIN", "System Volume Information", "node_modules",
    "__pycache__", ".git", ".svn", ".gradle", ".idea", ".vscode",
    "thumbnails", "thumbnail_cache", ".nomedia_cache",
}

SKIP_FILE_PREFIXES = (
    ".",  # semua file hidden (mulai titik)
)

SKIP_FILE_NAMES = {
    ".nomedia", "thumbs.db", "desktop.ini", "ehthumbs.db",
}


# ═══════════════════════════════════════════════════════════
# SKIP HELPER (v7.2.2 FIX)
# ═══════════════════════════════════════════════════════════

def _should_skip_path(path, is_dir=False):
    """
    Cek apakah path harus di-skip saat scan.
    
    Skip:
    - Folder/ file hidden (prefix .)
    - Folder sampah umum (Android, .thumbnails, dll)
    - File sampah (thumbs.db, .nomedia)
    """
    name = os.path.basename(path.rstrip("/"))

    if not name:
        return True

    if name.startswith("."):
        return True

    if is_dir and name in SKIP_FOLDER_NAMES:
        return True

    if not is_dir and name.lower() in SKIP_FILE_NAMES:
        return True

    return False


# ═══════════════════════════════════════════════════════════
# USERHASH CLEANER
# ═══════════════════════════════════════════════════════════

def _clean_userhash(userhash):
    """Bersihin userhash dari placeholder → return "" kalau placeholder."""
    if not userhash:
        return ""

    cleaned = str(userhash).strip()
    if not cleaned:
        return ""

    if cleaned.lower() in USERHASH_PLACEHOLDERS:
        return ""

    lower = cleaned.lower()
    if "harap diisi" in lower or "isi userhash" in lower or "placeholder" in lower:
        return ""

    if len(cleaned) < 6:
        return ""

    return cleaned


def _mask_hash(userhash):
    """Mask userhash untuk display."""
    if not userhash:
        return ""
    if len(userhash) <= 10:
        return "•" * len(userhash)
    return f"{userhash[:6]}...{userhash[-4:]}"


# ═══════════════════════════════════════════════════════════
# LOW-LEVEL FILE OPS
# ═══════════════════════════════════════════════════════════

def _ensure_accounts_dir():
    os.makedirs(ACCOUNTS_DIR, exist_ok=True)


def _ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def _ensure_cache_dir():
    os.makedirs(CACHE_DIR, exist_ok=True)


def _load_active_json():
    _ensure_accounts_dir()
    if not os.path.exists(ACTIVE_FILE):
        return {"version": 3, "active_account": None, "accounts": {}}
    try:
        with open(ACTIVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "accounts" not in data:
            data["accounts"] = {}
        if "active_account" not in data:
            data["active_account"] = None
        return data
    except Exception:
        return {"version": 3, "active_account": None, "accounts": {}}


def _save_active_json(data):
    _ensure_accounts_dir()
    tmp = ACTIVE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, ACTIVE_FILE)


def _slugify(name):
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "account"


def _unique_slug(base_slug):
    data = _load_active_json()
    if base_slug not in data["accounts"]:
        return base_slug
    i = 2
    while f"{base_slug}_{i}" in data["accounts"]:
        i += 1
    return f"{base_slug}_{i}"


# ═══════════════════════════════════════════════════════════
# PUBLIC API — READ
# ═══════════════════════════════════════════════════════════

def list_accounts():
    data = _load_active_json()
    return data.get("accounts", {})


def get_active_slug():
    data = _load_active_json()
    return data.get("active_account")


def has_accounts():
    return len(list_accounts()) > 0


def get_account_info(slug):
    accounts = list_accounts()
    return accounts.get(slug)


def get_account_paths(slug=None):
    """
    Return semua path untuk akun.
    
    Struktur baru (v7.2.2):
        accounts/<slug>/config.json      → config
        output/<slug>/index.html         → galeri
        output/<slug>/manager.html       → manager
        output/<slug>/embed.txt          → embed list
        cache/<slug>/uploads_cache.json  → cache upload
        cache/<slug>/deleted.json        → blacklist
    """
    if slug is None:
        slug = get_active_slug()
    if not slug:
        return None

    acc_dir = os.path.join(ACCOUNTS_DIR, slug)
    out_dir = os.path.join(OUTPUT_DIR, slug)
    cache_dir = os.path.join(CACHE_DIR, slug)

    return {
        "slug": slug,
        # Config (accounts/)
        "dir": acc_dir,
        "config": os.path.join(acc_dir, ACCOUNT_FILES["config"]),
        # Output (output/)
        "output_dir": out_dir,
        "index_html": os.path.join(out_dir, OUTPUT_FILES["index_html"]),
        "manager_html": os.path.join(out_dir, OUTPUT_FILES["manager_html"]),
        "embed_txt": os.path.join(out_dir, OUTPUT_FILES["embed_txt"]),
        # Cache (cache/)
        "cache": os.path.join(cache_dir, CACHE_FILES["cache"]),
        "deleted": os.path.join(cache_dir, CACHE_FILES["deleted"]),
        "cache_dir": cache_dir,
    }


def get_account_stats(slug):
    """Hitung statistik akun: file count, total size, dll (dari cache)."""
    paths = get_account_paths(slug)
    if not paths:
        return {"files": 0, "size_bytes": 0, "size_human": "0 B"}

    cache_file = paths["cache"]
    if not os.path.exists(cache_file):
        return {"files": 0, "size_bytes": 0, "size_human": "0 B"}

    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            cache = json.load(f)

        files = 0
        total_bytes = 0
        for entry in cache.values():
            if isinstance(entry, dict):
                files += 1
                total_bytes += entry.get("file_size", 0)
            elif isinstance(entry, str):
                files += 1

        if total_bytes < 1024:
            size_h = f"{total_bytes} B"
        elif total_bytes < 1024 ** 2:
            size_h = f"{total_bytes / 1024:.1f} kB"
        elif total_bytes < 1024 ** 3:
            size_h = f"{total_bytes / (1024 ** 2):.1f} MB"
        else:
            size_h = f"{total_bytes / (1024 ** 3):.2f} GB"

        return {
            "files": files,
            "size_bytes": total_bytes,
            "size_human": size_h,
        }
    except Exception:
        return {"files": 0, "size_bytes": 0, "size_human": "0 B"}


# ═══════════════════════════════════════════════════════════
# PUBLIC API — WRITE
# ═══════════════════════════════════════════════════════════

def create_account(name, userhash="", judul="lumoss", media_dirs=None):
    """
    Buat akun baru.
    
    Args:
        name: nama akun (display)
        userhash: Catbox userhash (opsional)
        judul: judul project
        media_dirs: list folder media (WAJIB diisi dari onboarding)
    
    Returns:
        (success: bool, message: str)
    """
    if not name or not name.strip():
        return False, "Nama akun tidak boleh kosong."

    if not media_dirs or not isinstance(media_dirs, list) or len(media_dirs) == 0:
        return False, "Minimal pilih 1 folder media."

    name = name.strip()
    data = _load_active_json()

    for slug, info in data["accounts"].items():
        if info.get("name", "").lower() == name.lower():
            return False, f"Akun dengan nama '{name}' sudah ada."

    userhash = _clean_userhash(userhash)

    base_slug = _slugify(name)
    slug = _unique_slug(base_slug)

    acc_dir = os.path.join(ACCOUNTS_DIR, slug)
    out_dir = os.path.join(OUTPUT_DIR, slug)
    cache_dir = os.path.join(CACHE_DIR, slug)

    try:
        os.makedirs(acc_dir, exist_ok=True)
        os.makedirs(out_dir, exist_ok=True)
        os.makedirs(cache_dir, exist_ok=True)
    except Exception as e:
        return False, f"Gagal buat folder: {e}"

    # Normalisasi media_dirs
    normalized_dirs = []
    for item in media_dirs:
        if isinstance(item, str):
            normalized_dirs.append({
                "path": item,
                "recursive": True,
                "enabled": True,
                "label": os.path.basename(item.rstrip("/")) or item,
            })
        elif isinstance(item, dict):
            path = item.get("path", "").strip()
            if not path:
                continue
            normalized_dirs.append({
                "path": path,
                "recursive": item.get("recursive", True),
                "enabled": item.get("enabled", True),
                "label": item.get("label", os.path.basename(path.rstrip("/")) or path),
            })

    if not normalized_dirs:
        return False, "Format media_dirs tidak valid."

    acc_config = {
        "userhash": userhash,
        "judul_project": judul or name,
        "counter_namespace": f"lumoss-{slug}",
        "media_dirs": normalized_dirs,
        "photos_mode": "multiple",
        "output_mode": "auto",
        "output_custom_dir": "",
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

    config_path = os.path.join(acc_dir, ACCOUNT_FILES["config"])
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(acc_config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        shutil.rmtree(acc_dir, ignore_errors=True)
        shutil.rmtree(out_dir, ignore_errors=True)
        shutil.rmtree(cache_dir, ignore_errors=True)
        return False, f"Gagal buat config: {e}"

    data["accounts"][slug] = {
        "name": name,
        "userhash_masked": _mask_hash(userhash) if userhash else "(anonymous)",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "last_used": None,
        "enabled": True,
        "total_files": 0,
        "total_size": "0 B",
        "media_dirs_count": len(normalized_dirs),
    }

    if data["active_account"] is None:
        data["active_account"] = slug

    try:
        _save_active_json(data)
    except Exception as e:
        shutil.rmtree(acc_dir, ignore_errors=True)
        shutil.rmtree(out_dir, ignore_errors=True)
        shutil.rmtree(cache_dir, ignore_errors=True)
        return False, f"Gagal simpan registry: {e}"

    return True, slug


def switch_account(slug):
    data = _load_active_json()
    if slug not in data["accounts"]:
        return False, f"Akun '{slug}' tidak ditemukan."

    data["active_account"] = slug
    data["accounts"][slug]["last_used"] = datetime.now().isoformat(timespec="seconds")

    try:
        _save_active_json(data)
        return True, f"Akun aktif: {data['accounts'][slug]['name']}"
    except Exception as e:
        return False, f"Gagal switch: {e}"


def rename_account(slug, new_name):
    if not new_name or not new_name.strip():
        return False, "Nama tidak boleh kosong."

    data = _load_active_json()
    if slug not in data["accounts"]:
        return False, f"Akun '{slug}' tidak ditemukan."

    for s, info in data["accounts"].items():
        if s != slug and info.get("name", "").lower() == new_name.lower():
            return False, f"Nama '{new_name}' sudah dipakai akun lain."

    data["accounts"][slug]["name"] = new_name.strip()
    try:
        _save_active_json(data)
        return True, "Nama akun diubah."
    except Exception as e:
        return False, f"Gagal rename: {e}"


def delete_account(slug, delete_files=False):
    data = _load_active_json()

    if slug not in data["accounts"]:
        return False, f"Akun '{slug}' tidak ditemukan."

    remaining = [s for s in data["accounts"].keys() if s != slug]
    if not remaining:
        return False, "Tidak bisa hapus akun terakhir. Buat akun baru dulu."

    if delete_files:
        for d in (
            os.path.join(ACCOUNTS_DIR, slug),
            os.path.join(OUTPUT_DIR, slug),
            os.path.join(CACHE_DIR, slug),
        ):
            if os.path.exists(d):
                try:
                    shutil.rmtree(d)
                except Exception as e:
                    return False, f"Gagal hapus folder {d}: {e}"

    del data["accounts"][slug]

    if data["active_account"] == slug:
        data["active_account"] = remaining[0]

    try:
        _save_active_json(data)
        return True, f"Akun dihapus. Akun aktif sekarang: {data['active_account']}"
    except Exception as e:
        return False, f"Gagal simpan: {e}"


def update_account_stats(slug):
    """Update stats akun + sync userhash_masked."""
    data = _load_active_json()
    if slug not in data["accounts"]:
        return False

    stats = get_account_stats(slug)
    data["accounts"][slug]["total_files"] = stats["files"]
    data["accounts"][slug]["total_size"] = stats["size_human"]
    data["accounts"][slug]["last_used"] = datetime.now().isoformat(timespec="seconds")

    try:
        paths = get_account_paths(slug)
        if paths and os.path.exists(paths["config"]):
            with open(paths["config"], "r", encoding="utf-8") as f:
                cfg = json.load(f)
            uh = _clean_userhash(cfg.get("userhash", ""))
            new_masked = _mask_hash(uh) if uh else "(anonymous)"
            data["accounts"][slug]["userhash_masked"] = new_masked
            if uh != cfg.get("userhash", ""):
                cfg["userhash"] = uh
                with open(paths["config"], "w", encoding="utf-8") as f:
                    json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

    try:
        _save_active_json(data)
        return True
    except Exception:
        return False


def clean_all_accounts_userhash():
    """Clean userhash di SEMUA akun yang ada."""
    cleaned = []
    for slug in list_accounts().keys():
        paths = get_account_paths(slug)
        if not paths:
            continue
        config_path = paths["config"]
        if not os.path.exists(config_path):
            continue
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            old_uh = cfg.get("userhash", "")
            new_uh = _clean_userhash(old_uh)
            if new_uh != old_uh:
                cfg["userhash"] = new_uh
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(cfg, f, indent=2, ensure_ascii=False)
                cleaned.append(slug)
        except Exception:
            continue
    return len(cleaned), cleaned


def sync_active_json():
    """Sync field userhash_masked, total_files, total_size di active.json."""
    data = _load_active_json()
    updated = []

    for slug, info in data.get("accounts", {}).items():
        paths = get_account_paths(slug)
        if not paths:
            continue

        config_path = paths["config"]
        if not os.path.exists(config_path):
            continue

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)

            uh = cfg.get("userhash", "")
            uh_cleaned = _clean_userhash(uh)
            new_masked = _mask_hash(uh_cleaned) if uh_cleaned else "(anonymous)"

            old_masked = info.get("userhash_masked", "")
            if old_masked != new_masked:
                data["accounts"][slug]["userhash_masked"] = new_masked
                updated.append(slug)

            stats = get_account_stats(slug)
            if (info.get("total_files") != stats["files"]
                    or info.get("total_size") != stats["size_human"]):
                data["accounts"][slug]["total_files"] = stats["files"]
                data["accounts"][slug]["total_size"] = stats["size_human"]
                if slug not in updated:
                    updated.append(slug)

            if uh != uh_cleaned:
                cfg["userhash"] = uh_cleaned
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(cfg, f, indent=2, ensure_ascii=False)
        except Exception:
            continue

    if updated:
        try:
            _save_active_json(data)
        except Exception:
            pass

    return len(updated), updated


# ═══════════════════════════════════════════════════════════
# MEDIA FOLDER SCANNER (untuk onboarding)
# ═══════════════════════════════════════════════════════════

def scan_available_media_folders():
    """
    Scan folder umum di Android buat onboarding.
    
    v7.2.2 FIX: Skip folder & file hidden/sampah.
    """
    from media_processor import SUPPORTED_EXTENSIONS

    results = []
    for path in COMMON_MEDIA_FOLDERS:
        if not os.path.isdir(path):
            continue

        if _should_skip_path(path, is_dir=True):
            continue

        try:
            count = 0
            total_size = 0
            for root, dirs, files in os.walk(path, followlinks=False):
                dirs[:] = [
                    d for d in dirs
                    if not _should_skip_path(os.path.join(root, d), is_dir=True)
                ]
                files = [
                    f for f in files
                    if not _should_skip_path(os.path.join(root, f), is_dir=False)
                ]

                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    if ext in SUPPORTED_EXTENSIONS:
                        count += 1
                        try:
                            total_size += os.path.getsize(os.path.join(root, f))
                        except Exception:
                            pass
                if count > 5000:
                    break

            if count == 0:
                continue

            if total_size < 1024:
                size_h = f"{total_size} B"
            elif total_size < 1024 ** 2:
                size_h = f"{total_size / 1024:.0f} KB"
            elif total_size < 1024 ** 3:
                size_h = f"{total_size / (1024 ** 2):.1f} MB"
            else:
                size_h = f"{total_size / (1024 ** 3):.2f} GB"

            results.append({
                "path": path,
                "label": os.path.basename(path.rstrip("/")) or path,
                "exists": True,
                "file_count": count,
                "size_bytes": total_size,
                "size_human": size_h,
            })
        except Exception:
            continue

    return results


def scan_custom_folder(path):
    """
    Scan 1 folder custom (buat user yang mau pilih manual).
    
    v7.2.2 FIX: Skip folder & file hidden/sampah.
    """
    from media_processor import SUPPORTED_EXTENSIONS

    path = os.path.expanduser(path.strip())
    if not os.path.isdir(path):
        return None

    try:
        count = 0
        total_size = 0
        for root, dirs, files in os.walk(path, followlinks=False):
            dirs[:] = [
                d for d in dirs
                if not _should_skip_path(os.path.join(root, d), is_dir=True)
            ]
            files = [
                f for f in files
                if not _should_skip_path(os.path.join(root, f), is_dir=False)
            ]

            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in SUPPORTED_EXTENSIONS:
                    count += 1
                    try:
                        total_size += os.path.getsize(os.path.join(root, f))
                    except Exception:
                        pass

        if total_size < 1024:
            size_h = f"{total_size} B"
        elif total_size < 1024 ** 2:
            size_h = f"{total_size / 1024:.0f} KB"
        elif total_size < 1024 ** 3:
            size_h = f"{total_size / (1024 ** 2):.1f} MB"
        else:
            size_h = f"{total_size / (1024 ** 3):.2f} GB"

        return {
            "path": path,
            "label": os.path.basename(path.rstrip("/")) or path,
            "exists": True,
            "file_count": count,
            "size_bytes": total_size,
            "size_human": size_h,
        }
    except Exception:
        return None


def check_storage_permission():
    """
    Cek apakah Termux punya akses ke /storage/emulated/0/.
    
    Returns:
        (has_access: bool, message: str)
    """
    test_path = "/storage/emulated/0/"
    try:
        os.listdir(test_path)
        return True, "Akses storage OK"
    except PermissionError:
        return False, "Izin storage belum aktif"
    except FileNotFoundError:
        return False, "Folder /storage/emulated/0/ gak ketemu"
    except Exception as e:
        return False, f"Error cek izin: {e}"


# ═══════════════════════════════════════════════════════════
# ONBOARDING HELPERS (v7.2.2 — shared menu.py + menu_account.py)
# ═══════════════════════════════════════════════════════════

def _check_storage_permission_onboarding():
    """
    Cek izin storage + kasih instruksi kalau belum.
    Return True kalau OK, False kalau gagal.
    """
    from ui_helpers import (
        C_MOSS_1, C_YELLOW, C_SILVER, C_RESET, C_BOLD,
        clear_screen, print_banner, section_title,
        print_success_aesthetic, print_warning_aesthetic,
        print_info_aesthetic,
    )

    has_access, msg = check_storage_permission()
    if has_access:
        return True

    clear_screen()
    print_banner(compact=True)
    print()
    section_title("IZIN STORAGE BELUM AKTIF", emoji="⚠️")
    print()

    print(f"  {C_YELLOW}Lumoss butuh akses ke folder foto di HP lu.{C_RESET}")
    print(f"  {C_SILVER}Jalankan command ini di Termux:{C_RESET}")
    print()
    print(f"    {C_MOSS_1}{C_BOLD}termux-setup-storage{C_RESET}")
    print()
    print(f"  {C_SILVER}Terus balik ke sini, tekan Enter buat lanjut.{C_RESET}")
    print()

    try:
        input(f"  {C_MOSS_1}›{C_RESET} Tekan Enter setelah setup... ")
    except (EOFError, KeyboardInterrupt):
        print()

    has_access, msg = check_storage_permission()
    if has_access:
        print()
        print_success_aesthetic("Izin storage OK! ✅")
        import time
        time.sleep(1)
        return True
    else:
        print()
        print_warning_aesthetic(f"Masih belum bisa akses: {msg}")
        print_info_aesthetic("Coba lagi nanti, atau skip dulu.")
        return False


def pick_media_folders_onboarding():
    """
    Onboarding: WAJIB pilih folder media.
    
    Returns:
        list dict [{path, recursive, enabled, label}, ...] atau None kalau batal.
    """
    from ui_helpers import (
        C_MOSS_1, C_MOSS_2, C_MOSS_3, C_WHITE, C_SILVER, C_RESET, C_BOLD,
        clear_screen, print_banner, section_title, press_enter,
        input_prompt, input_yes_no,
        print_success_aesthetic, print_error_aesthetic,
        print_warning_aesthetic, print_info_aesthetic,
    )

    if not _check_storage_permission_onboarding():
        return None

    clear_screen()
    print_banner(compact=True)
    print()
    section_title("PILIH FOLDER MEDIA", emoji="📂")
    print()

    print(f"  {C_SILVER}Scan folder umum di HP lu...{C_RESET}")
    print()

    folders = scan_available_media_folders()

    if not folders:
        return _handle_no_folders()

    for f in folders:
        f["_selected"] = False

    while True:
        clear_screen()
        print_banner(compact=True)
        print()
        section_title("PILIH FOLDER MEDIA", emoji="📂")
        print()

        print(f"  {C_SILVER}Ditemukan {len(folders)} folder:{C_RESET}")
        print()

        for i, f in enumerate(folders, 1):
            marker = "✅" if f.get("_selected") else "⬜"
            print(
                f"  {C_MOSS_1}[{i}]{C_RESET} {marker}  "
                f"{C_WHITE}{f['path']}{C_RESET}"
            )
            print(f"        {C_SILVER}({f['file_count']} file, {f['size_human']}){C_RESET}")

        print()
        print(f"  {C_MOSS_1}[c]{C_RESET}  ➕ Tambah folder manual")
        print(f"  {C_MOSS_1}[d]{C_RESET}  ✔  Selesai (wajib min. 1 folder)")
        print(f"  {C_MOSS_1}[u]{C_RESET}  ✖  Unselect folder (contoh: u1,2)")
        print(f"  {C_MOSS_1}[0]{C_RESET}  ↩  Batal")
        print()

        raw = input_prompt("Pilih (bisa multiple: 1,2,3)", default="d").strip().lower()

        if raw == "0":
            return None

        if raw == "c":
            path = input_prompt("Path folder manual").strip()
            if not path:
                continue
            scan = scan_custom_folder(path)
            if not scan:
                print_error_aesthetic("Folder gak valid.")
                press_enter()
                continue
            existing_paths = [f["path"] for f in folders]
            if scan["path"] in existing_paths:
                print_warning_aesthetic("Folder udah ada di list.")
                press_enter()
                continue
            scan["_selected"] = True
            folders.append(scan)
            print_success_aesthetic(f"Ditambah: {scan['path']}")
            press_enter()
            continue

        if raw == "d":
            selected = [f for f in folders if f.get("_selected")]
            if not selected:
                print_error_aesthetic("Pilih minimal 1 folder dulu!")
                print_info_aesthetic("Ketik nomor folder (contoh: 1,2), terus 'd' buat selesai.")
                press_enter()
                continue

            return [
                {
                    "path": f["path"],
                    "recursive": True,
                    "enabled": True,
                    "label": f["label"],
                }
                for f in selected
            ]

        if raw.startswith("u"):
            nums_str = raw[1:].replace(" ", "")
            try:
                nums = [int(x.strip()) for x in nums_str.split(",") if x.strip()]
            except ValueError:
                print_error_aesthetic("Format salah. Contoh: u1,2")
                press_enter()
                continue
            changed = 0
            for n in nums:
                if 1 <= n <= len(folders):
                    folders[n - 1]["_selected"] = False
                    changed += 1
            if changed > 0:
                print_success_aesthetic(f"Unselect {changed} folder.")
            press_enter()
            continue

        try:
            nums = [int(x.strip()) for x in raw.replace(" ", "").split(",") if x.strip()]
        except ValueError:
            print_error_aesthetic("Format salah. Contoh: 1,2,3")
            press_enter()
            continue

        if not nums:
            print_error_aesthetic("Input kosong.")
            press_enter()
            continue

        changed = 0
        for n in nums:
            if 1 <= n <= len(folders):
                folders[n - 1]["_selected"] = True
                changed += 1

        if changed == 0:
            print_error_aesthetic("Nomor folder gak valid.")
            press_enter()


def _handle_no_folders():
    """Handle case: gak ada folder ke-detect."""
    from ui_helpers import (
        C_MOSS_1, C_WHITE, C_SILVER, C_YELLOW, C_RESET,
        clear_screen, print_banner, section_title, press_enter,
        input_prompt,
        print_success_aesthetic, print_error_aesthetic,
        print_info_aesthetic,
    )

    while True:
        clear_screen()
        print_banner(compact=True)
        print()
        section_title("Gak Ada Folder Ke-Detect", emoji="⚠️")
        print()

        print(f"  {C_YELLOW}Lumoss gak nemu folder media di HP lu.{C_RESET}")
        print()
        print(f"  {C_MOSS_1}[1]{C_RESET}  Input path manual")
        print(f"  {C_MOSS_1}[2]{C_RESET}  Bikin folder baru di /Pictures/Lumoss/")
        print(f"  {C_MOSS_1}[0]{C_RESET}  Batal")
        print()

        pilihan = input_prompt("Pilih", default="2")

        if pilihan == "0":
            return None
        elif pilihan == "1":
            path = input_prompt("Path folder media").strip()
            if not path:
                continue
            scan = scan_custom_folder(path)
            if not scan:
                print_error_aesthetic("Folder gak valid atau gak ada.")
                press_enter()
                continue
            return [{
                "path": scan["path"],
                "recursive": True,
                "enabled": True,
                "label": scan["label"],
            }]
        elif pilihan == "2":
            new_path = "/storage/emulated/0/Pictures/Lumoss"
            try:
                os.makedirs(new_path, exist_ok=True)
                print_success_aesthetic(f"Folder dibuat: {new_path}")
                print_info_aesthetic("Taruh foto/video di situ, terus balik ke sini.")
                press_enter()
                return [{
                    "path": new_path,
                    "recursive": True,
                    "enabled": True,
                    "label": "Lumoss",
                }]
            except Exception as e:
                print_error_aesthetic(f"Gagal bikin folder: {e}")
                press_enter()
                continue


# ═══════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════

def ensure_active_account():
    """Pastikan ada akun aktif."""
    if has_accounts():
        slug = get_active_slug()
        if slug and slug in list_accounts():
            return slug
        accounts = list_accounts()
        if accounts:
            first_slug = list(accounts.keys())[0]
            switch_account(first_slug)
            return first_slug
    return None


# ═══════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════

__all__ = [
    "ACCOUNTS_DIR", "OUTPUT_DIR", "CACHE_DIR", "ACTIVE_FILE",
    "COMMON_MEDIA_FOLDERS",
    "SKIP_FOLDER_NAMES", "SKIP_FILE_PREFIXES", "SKIP_FILE_NAMES",
    "_should_skip_path",
    "_check_storage_permission_onboarding",
    "pick_media_folders_onboarding",
    "_handle_no_folders",
    "list_accounts", "get_active_slug", "has_accounts", "get_account_info",
    "get_account_paths", "get_account_stats",
    "create_account", "switch_account", "rename_account", "delete_account",
    "update_account_stats", "ensure_active_account",
    "clean_all_accounts_userhash", "sync_active_json",
    "scan_available_media_folders", "scan_custom_folder",
    "check_storage_permission",
]