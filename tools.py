"""
lumoss — Tools (v7.2.2 MEDIA GARDEN)
Kotak alat bantu: GitHub upload, backup, fix cache, dll.

Changelog v7.2.2:
- BREAKING: Semua fungsi terima `slug` (default: akun aktif)
- Path diambil dari account_manager.get_account_paths()
- backup_project() backup ke backup/ folder
- upload_to_github() pake output/<slug>/
- clear_upload_cache(), reset_blacklist(), fix_broken_cache() pake cache/<slug>/

Tools tersedia:
- upload_to_github(): Push index.html + manager.html ke GitHub
- backup_project(): Zip backup file penting
- fix_broken_cache(): Bersihkan cache entri rusak
- cleanup_thumbnails(): Hapus thumbnail lama
- clear_upload_cache(): Hapus uploads_cache.json
- reset_blacklist(): Hapus deleted.json
"""

import os
import re
import json
import time
import shutil
import zipfile
import tempfile
import subprocess
from datetime import datetime
from pathlib import Path

from ui_helpers import (
    C_RESET, C_BOLD, C_GREEN, C_YELLOW, C_RED, C_WHITE,
    C_MOSS_1, C_MOSS_2, C_MOSS_3, C_SILVER,
    print_success, print_error, print_warning, print_info,
    input_prompt, input_yes_no, press_enter, format_bytes, mask_secret,
)

import account_manager as am


BACKUP_DIR = "backup"


# ═══════════════════════════════════════════════════════════
# GITHUB UPLOAD
# ═══════════════════════════════════════════════════════════

def upload_to_github(cfg, files_to_upload=None, slug=None):
    """Upload file HTML ke GitHub via git clone + push."""
    print(f"\n{C_MOSS_1}━━━ 📤\033[8GUPLOAD KE GITHUB ━━━{C_RESET}\n")

    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False, "Git tidak terinstall. Install dulu: pkg install git"

    if slug is None:
        slug = am.get_active_slug()
    if not slug:
        return False, "Belum ada akun aktif."

    paths = am.get_account_paths(slug)
    if not paths:
        return False, f"Akun '{slug}' tidak ditemukan."

    output_dir = paths["output_dir"]

    gh_user = cfg.get("github_username", "").strip()
    gh_repo = cfg.get("github_repo", "").strip()
    gh_token = cfg.get("github_token", "").strip()
    gh_branch = cfg.get("github_branch", "main").strip() or "main"

    if not gh_user or not gh_repo:
        return False, "GitHub username / repo belum diisi di config."

    if gh_token:
        repo_url = f"https://{gh_user}:{gh_token}@github.com/{gh_user}/{gh_repo}.git"
        display_url = f"https://github.com/{gh_user}/{gh_repo}.git"
    else:
        repo_url = f"https://github.com/{gh_user}/{gh_repo}.git"
        display_url = repo_url

    print_info(f"Repo\033[14G: {display_url}")
    print_info(f"Branch\033[14G: {gh_branch}")
    print_info(f"Token\033[14G: {mask_secret(gh_token) if gh_token else '(tidak ada)'}")
    print()

    if files_to_upload is None:
        files_to_upload = ["index.html", "manager.html"]

    existing_files = []
    for f in files_to_upload:
        full_path = os.path.join(output_dir, f)
        if os.path.exists(full_path):
            existing_files.append((f, full_path))

    if not existing_files:
        return False, f"Tidak ada file HTML di {output_dir}. Jalankan upload dulu (menu 1)."

    print(f"{C_MOSS_1}File yang akan di-upload:{C_RESET}")
    for f, full_path in existing_files:
        size_kb = os.path.getsize(full_path) / 1024
        print(f"  {C_GREEN}✓{C_RESET}\033[7G{C_WHITE}{f}{C_RESET} {C_SILVER}({size_kb:.1f} KB){C_RESET}")
    print()

    commit_msg = input_prompt(
        "Commit message",
        default=f"Update galeri {datetime.now().strftime('%Y-%m-%d %H:%M')}",
    )

    deploy_dir = tempfile.mkdtemp(prefix="lumoss_deploy_")
    print_info(f"Working dir\033[16G: {deploy_dir}")

    try:
        print(f"\n{C_MOSS_2}[1/5]\033[10G{C_WHITE}Clone repository...{C_RESET}")
        result = subprocess.run(
            ["git", "clone", "--depth", "1", "-b", gh_branch, repo_url, deploy_dir],
            capture_output=True, text=True, timeout=180,
        )
        if result.returncode != 0:
            result = subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, deploy_dir],
                capture_output=True, text=True, timeout=180,
            )
            if result.returncode != 0:
                return False, f"Gagal clone: {result.stderr[:300]}"

        print(f"{C_MOSS_2}[2/5]\033[10G{C_WHITE}Copy file...{C_RESET}")
        for f, full_path in existing_files:
            dst = os.path.join(deploy_dir, os.path.basename(f))
            shutil.copy(full_path, dst)
            print_success(f"Copy {f}")

        print(f"{C_MOSS_2}[3/5]\033[10G{C_WHITE}Setup git...{C_RESET}")
        subprocess.run(
            ["git", "-C", deploy_dir, "config", "user.email", "bot@lumoss.local"],
            capture_output=True,
        )
        subprocess.run(
            ["git", "-C", deploy_dir, "config", "user.name", "lumoss-bot"],
            capture_output=True,
        )

        print(f"{C_MOSS_2}[4/5]\033[10G{C_WHITE}Commit...{C_RESET}")
        subprocess.run(["git", "-C", deploy_dir, "add", "-A"], capture_output=True)
        commit_result = subprocess.run(
            ["git", "-C", deploy_dir, "commit", "-m", commit_msg],
            capture_output=True, text=True,
        )
        if "nothing to commit" in (commit_result.stdout + commit_result.stderr):
            return True, "Tidak ada perubahan (file sudah sama)."

        print(f"{C_MOSS_2}[5/5]\033[10G{C_WHITE}Push ke {gh_branch}...{C_RESET}")
        push_result = subprocess.run(
            ["git", "-C", deploy_dir, "push", "origin", gh_branch],
            capture_output=True, text=True, timeout=180,
        )

        if push_result.returncode == 0:
            print()
            print_success("Berhasil upload ke GitHub!")
            print_info(f"Repo\033[12G: {display_url}")
            print_info(f"Branch\033[12G: {gh_branch}")
            pages_url = f"https://{gh_user}.github.io/{gh_repo}/"
            print_info(f"Pages\033[12G: {pages_url}")
            return True, f"Success: {pages_url}"
        else:
            err = push_result.stderr[:300]
            return False, f"Gagal push: {err}"

    except subprocess.TimeoutExpired:
        return False, "Timeout. Cek koneksi internet."
    except Exception as e:
        return False, f"Error: {e}"
    finally:
        shutil.rmtree(deploy_dir, ignore_errors=True)


# ═══════════════════════════════════════════════════════════
# BACKUP PROJECT
# ═══════════════════════════════════════════════════════════

def backup_project(output_dir=None, slug=None):
    """Zip file penting project ke folder backup/."""
    print(f"\n{C_MOSS_1}━━━ 💾\033[8GBACKUP PROJECT ━━━{C_RESET}\n")

    if output_dir is None:
        output_dir = BACKUP_DIR

    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"lumoss_backup_{timestamp}.zip"
    out_path = os.path.join(output_dir, filename)

    # File source code yang di-backup
    files_to_backup = [
        "global_config.json",
        "account_manager.py",
        "config_manager.py",
        "ui_helpers.py",
        "uploader.py",
        "media_processor.py",
        "html_builder.py",
        "tools.py",
        "lumoss.py",
        "menu.py",
        "menu_account.py",
        "menu_embed.py",
        "menu_tools.py",
        "embed_parser.py",
        "requirements.txt",
    ]

    count = 0
    total_bytes = 0

    try:
        with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in files_to_backup:
                if os.path.exists(f):
                    zf.write(f, os.path.basename(f))
                    count += 1
                    total_bytes += os.path.getsize(f)

            # Backup config semua akun
            for acc_slug in am.list_accounts().keys():
                paths = am.get_account_paths(acc_slug)
                if not paths:
                    continue
                config_path = paths["config"]
                if os.path.exists(config_path):
                    arcname = os.path.join("accounts", acc_slug, "config.json")
                    zf.write(config_path, arcname)
                    count += 1
                    total_bytes += os.path.getsize(config_path)

        size_str = format_bytes(os.path.getsize(out_path))
        print()
        print_success(f"Backup {count} file → {out_path}")
        print_info(f"Total: {size_str}")
        return True, out_path

    except Exception as e:
        if os.path.exists(out_path):
            os.remove(out_path)
        return False, f"Gagal backup: {e}"


# ═══════════════════════════════════════════════════════════
# CACHE & BLACKLIST
# ═══════════════════════════════════════════════════════════

def clear_upload_cache(slug=None):
    """Hapus file cache upload."""
    print(f"\n{C_MOSS_1}━━━ 🗑️\033[8GHAPUS CACHE UPLOAD ━━━{C_RESET}\n")

    if slug is None:
        slug = am.get_active_slug()
    if not slug:
        return False, "Belum ada akun aktif."

    paths = am.get_account_paths(slug)
    cache_file = paths["cache"]

    if not os.path.exists(cache_file):
        print_warning(f"Cache tidak ditemukan: {cache_file}")
        return False, "File tidak ada."

    backup_name = cache_file + ".bak"
    try:
        shutil.copy(cache_file, backup_name)
        print_info(f"Backup: {backup_name}")
    except Exception:
        pass

    try:
        os.remove(cache_file)
        print_success(f"Cache dihapus: {cache_file}")
        return True, "Cache dihapus."
    except Exception as e:
        return False, f"Gagal hapus: {e}"


def reset_blacklist(slug=None):
    """Hapus file blacklist (deleted.json)."""
    print(f"\n{C_MOSS_1}━━━ 🔄\033[8GRESET BLACKLIST ━━━{C_RESET}\n")

    if slug is None:
        slug = am.get_active_slug()
    if not slug:
        return False, "Belum ada akun aktif."

    paths = am.get_account_paths(slug)
    deleted_file = paths["deleted"]

    if not os.path.exists(deleted_file):
        print_warning(f"Blacklist tidak ditemukan: {deleted_file}")
        return False, "File tidak ada."

    try:
        with open(deleted_file, "r", encoding="utf-8") as f:
            deleted = json.load(f)
        count = len(deleted)
    except Exception:
        count = 0

    if count == 0:
        print_info("Blacklist kosong.")
        return True, "Sudah kosong."

    print_info(f"Total item di blacklist: {count}")
    konfirm = input_yes_no(f"{C_YELLOW}Hapus semua blacklist?{C_RESET}", default="n")
    if not konfirm:
        return False, "Dibatalkan."

    backup_name = deleted_file + ".bak"
    try:
        shutil.copy(deleted_file, backup_name)
        print_info(f"Backup: {backup_name}")
    except Exception:
        pass

    try:
        os.remove(deleted_file)
        print_success(f"Blacklist dihapus ({count} item).")
        return True, f"Hapus {count} item."
    except Exception as e:
        return False, f"Gagal hapus: {e}"


def fix_broken_cache(slug=None):
    """Bersihkan cache entri rusak."""
    print(f"\n{C_MOSS_1}━━━ 🔧\033[8GFIX BROKEN CACHE ━━━{C_RESET}\n")

    if slug is None:
        slug = am.get_active_slug()
    if not slug:
        return False, "Belum ada akun aktif."

    paths = am.get_account_paths(slug)
    cache_file = paths["cache"]

    if not os.path.exists(cache_file):
        print_warning(f"Cache tidak ditemukan: {cache_file}")
        return False, "File tidak ada."

    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            cache = json.load(f)
    except Exception as e:
        return False, f"Gagal baca cache: {e}"

    if not isinstance(cache, dict):
        return False, "Format cache tidak valid."

    before = len(cache)
    cleaned = {}
    removed_entries = []

    for rel_path, entry in cache.items():
        if not isinstance(entry, dict):
            removed_entries.append((rel_path, "bukan dict"))
            continue

        if not entry.get("url"):
            removed_entries.append((rel_path, "URL kosong"))
            continue

        url = entry.get("url", "")
        if not isinstance(url, str) or not url.startswith("http"):
            removed_entries.append((rel_path, f"URL tidak valid: {url[:30]}"))
            continue

        cleaned[rel_path] = entry

    removed = before - len(cleaned)

    if removed == 0:
        print_success("Cache sehat. Tidak ada yang perlu dibersihkan.")
        return True, "Cache sehat."

    print_warning(f"Ditemukan {removed} entri rusak:")
    for path, reason in removed_entries[:20]:
        print(f"  {C_RED}✗{C_RESET}\033[7G{C_WHITE}{path}{C_RESET} {C_SILVER}({reason}){C_RESET}")

    if len(removed_entries) > 20:
        print(f"  ... dan {len(removed_entries) - 20} lagi")
    print()

    konfirm = input_yes_no(f"{C_YELLOW}Hapus {removed} entri rusak?{C_RESET}", default="y")
    if not konfirm:
        return False, "Dibatalkan."

    backup_name = cache_file + ".bak"
    try:
        shutil.copy(cache_file, backup_name)
        print_info(f"Backup: {backup_name}")
    except Exception:
        pass

    try:
        tmp = cache_file + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(cleaned, f, indent=2, ensure_ascii=False)
        os.replace(tmp, cache_file)
        print_success(f"Cache dibersihkan. {len(cleaned)} entri tersisa.")
        return True, f"Hapus {removed} entri."
    except Exception as e:
        return False, f"Gagal simpan: {e}"


def cleanup_thumbnails(max_age_days=30):
    """Hapus thumbnail lama (>N hari)."""
    print(f"\n{C_MOSS_1}━━━ 🧹\033[8GCLEANUP THUMBNAIL ━━━{C_RESET}\n")

    try:
        from media_processor import cleanup_old_thumbnails
        removed = cleanup_old_thumbnails(max_age_days)
        if removed > 0:
            print_success(f"Hapus {removed} thumbnail lama.")
            return True, f"Hapus {removed} file."
        else:
            print_info("Tidak ada thumbnail lama.")
            return True, "Tidak ada yang dihapus."
    except Exception as e:
        return False, f"Error: {e}"


# ═══════════════════════════════════════════════════════════
# STATISTIK
# ═══════════════════════════════════════════════════════════

def cache_stats(slug=None):
    """Hitung statistik cache."""
    if slug is None:
        slug = am.get_active_slug()
    if not slug:
        return {"files": 0, "size_bytes": 0, "size_human": "0 B", "valid": 0, "broken": 0}

    paths = am.get_account_paths(slug)
    cache_file = paths["cache"]

    if not os.path.exists(cache_file):
        return {"files": 0, "size_bytes": 0, "size_human": "0 B", "valid": 0, "broken": 0}

    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            cache = json.load(f)
    except Exception:
        return {"files": 0, "size_bytes": 0, "size_human": "0 B", "valid": 0, "broken": 0}

    total_bytes = 0
    valid = 0
    broken = 0

    for rel_path, entry in cache.items():
        if isinstance(entry, dict):
            if entry.get("url"):
                valid += 1
                total_bytes += entry.get("file_size", 0)
            else:
                broken += 1
        else:
            broken += 1

    return {
        "files": len(cache),
        "size_bytes": total_bytes,
        "size_human": format_bytes(total_bytes),
        "valid": valid,
        "broken": broken,
    }


# ═══════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════

__all__ = [
    "BACKUP_DIR",
    "upload_to_github",
    "backup_project",
    "clear_upload_cache",
    "reset_blacklist",
    "fix_broken_cache",
    "cleanup_thumbnails",
    "cache_stats",
]