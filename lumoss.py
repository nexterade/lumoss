"""
lumoss — Entry Point (v7.2.2 MEDIA GARDEN)
File utama yang dijalankan user dengan cursor-positioning & aesthetic terminal.

Cara pakai:
    python lumoss.py

Atau langsung jalankan upload (kalau ada akun aktif):
    python lumoss.py upload

Changelog v7.2.2:
- BREAKING: Output HTML sekarang di output/<slug>/ (bukan accounts/<slug>/)
- BREAKING: Cache & deleted sekarang di cache/<slug>/
- NEW: Support multi-folder media (media_dirs array)
- NEW: _scan_media_dirs() — scan multiple folder sekaligus
- UPDATE: _load_embed_items() baca dari output/<slug>/embed.txt
- UPDATE: _copy_assets_to_output() copy ke output/<slug>/assets
- UPDATE: Rebranding amuv7 → lumoss
"""

import os
import sys
import json
import time
import hashlib
from pathlib import Path


# ═══════════════════════════════════════════════════════════
# ENSURE PROJECT DIR
# ═══════════════════════════════════════════════════════════

def _ensure_project_dir():
    """Pastikan working directory = folder lumoss."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.getcwd() != script_dir:
        os.chdir(script_dir)


_ensure_project_dir()


# ═══════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════

from ui_helpers import (
    C_RESET, C_BOLD, C_GREEN, C_RED, C_WHITE, C_YELLOW,
    C_MOSS_1, C_MOSS_2, C_MOSS_3, C_SILVER,
    clear_screen, print_banner, print_success, print_error, print_warning,
    print_info, press_enter,
    PROJECT_NAME, PROJECT_VERSION,
)

import account_manager as am
import config_manager as cm
import menu


# ═══════════════════════════════════════════════════════════
# HELPER: SCAN MULTI-FOLDER MEDIA (v7.2.2)
# ═══════════════════════════════════════════════════════════

def _scan_media_dirs(media_dirs, supported_exts):
    """
    Scan multiple folder media.
    
    Args:
        media_dirs: list dict [{path, recursive, enabled, label}, ...]
        supported_exts: set of supported extensions
    
    Returns:
        list of (file_path, source_label, rel_path) — rel_path relatif ke source
    """
    results = []

    for entry in media_dirs:
        if not entry.get("enabled", True):
            continue

        source_path = entry["path"]
        source_label = entry.get("label", os.path.basename(source_path.rstrip("/")) or source_path)
        recursive = entry.get("recursive", True)

        if not os.path.isdir(source_path):
            continue

        try:
            if recursive:
                for root, dirs, files in os.walk(source_path, followlinks=False):
                    for f in files:
                        ext = os.path.splitext(f)[1].lower()
                        if ext in supported_exts:
                            full = os.path.join(root, f)
                            rel = os.path.relpath(full, source_path).replace("\\", "/")
                            results.append((full, source_label, rel))
            else:
                for f in os.listdir(source_path):
                    full = os.path.join(source_path, f)
                    if os.path.isfile(full):
                        ext = os.path.splitext(f)[1].lower()
                        if ext in supported_exts:
                            results.append((full, source_label, f))
        except Exception:
            continue

    return results


# ═══════════════════════════════════════════════════════════
# CALLBACK: RUN UPLOAD
# ═══════════════════════════════════════════════════════════

def _callback_run_upload():
    """Callback: jalankan upload untuk akun aktif."""
    slug = am.get_active_slug()
    if not slug:
        print_error("Belum ada akun aktif. Bikin akun dulu di menu Account Manager.")
        return

    # ── Lazy import ──
    try:
        from uploader import (
            stats_reset, stats_snapshot,
            upload_to_catbox, verify_uploaded_file,
            print_summary_report,
        )
        from media_processor import (
            extract_detailed_exif, extract_date_from_filename,
            extract_auto_tags, generate_image_thumbnail,
            generate_video_thumbnail, cleanup_old_thumbnails,
            get_media_type, get_video_mime,
            SUPPORTED_EXTENSIONS, VIDEO_EXTS,
            MONTH_NAMES_ID,
        )
        from html_builder import build_all
        from account_manager import get_account_paths
    except ImportError as e:
        print_error(f"Gagal import module upload: {e}")
        print_info("Pastikan semua file batch 2 ada.")
        return

    paths = get_account_paths(slug)
    cfg = cm.load_config(slug)

    # ── v7.2.2: Multi-folder media ──
    media_dirs = cm.get_enabled_media_dirs(slug)

    if not media_dirs:
        print_error("Belum ada folder media yang di-set.")
        print_info("Buka menu 7 → Edit Konfigurasi → Kelola Folder Media")
        return

    output_dir = paths["output_dir"]
    cache_file = paths["cache"]
    deleted_file = paths["deleted"]

    print()
    print(f"{C_MOSS_1}━━━ 🚀\033[8GMULAI UPLOAD ━━━{C_RESET}\n")
    print(f"  {C_MOSS_3}Akun\033[12G{C_SILVER}:{C_RESET} {C_WHITE}{slug}{C_RESET}")
    print(f"  {C_MOSS_3}Folder\033[12G{C_SILVER}:{C_RESET} {C_WHITE}{len(media_dirs)} folder{C_RESET}")
    for md in media_dirs:
        rec = "recursive" if md.get("recursive", True) else "top-level"
        print(f"    {C_MOSS_2}•{C_RESET} {C_SILVER}{md['path']}{C_RESET} {C_SILVER}({rec}){C_RESET}")
    print(f"  {C_MOSS_3}Output\033[12G{C_SILVER}:{C_RESET} {C_WHITE}{output_dir}{C_RESET}")
    print()

    # ── Scan multi-folder ──
    scan_start = time.time()
    print(f"{C_MOSS_2}🔍\033[6GScan folder media...{C_RESET}")
    scanned = _scan_media_dirs(media_dirs, SUPPORTED_EXTENSIONS)
    scan_elapsed = time.time() - scan_start

    total_files = len(scanned)
    if total_files == 0:
        print_warning("Tidak ada media yang didukung.")
        print_info(f"Format didukung: {', '.join(sorted(SUPPORTED_EXTENSIONS))}")
        return

    print(f"{C_MOSS_1}✓\033[6G{C_WHITE}{total_files} file{C_RESET} {C_SILVER}ditemukan dalam {scan_elapsed:.1f}s{C_RESET}")
    print()

    # ── Reset stats ──
    stats_reset()

    import uploader as up
    with up._STATS_LOCK:
        up.SESSION_STATS["total_scanned"] = total_files
        up.SESSION_STATS["start_time"] = time.time()

    # ── Header info ──
    total_bytes = sum(os.path.getsize(p) for p, _, _ in scanned if os.path.exists(p))
    total_size_str = _format_bytes(total_bytes)

    print(f"  {C_MOSS_2}📊\033[6GTotal\033[16G{C_SILVER}:{C_RESET} {C_WHITE}{total_files} file{C_RESET} {C_SILVER}({total_size_str}){C_RESET}")
    print(f"  {C_MOSS_2}⚙️\033[6GWorkers\033[16G{C_SILVER}:{C_RESET} {C_WHITE}{cfg.get('workers', 1)}{C_RESET}")
    print()

    # ── Load cache & deleted ──
    cache = _load_json(cache_file, default={})
    deleted = _load_json(deleted_file, default={})

    # ── Process files ──
    gallery_data = []
    cache_dirty = False

    userhash = cfg.get("userhash", "")
    upload_cfg = cm.get_effective_config(slug)["global"].get("upload", {})
    batch_every = upload_cfg.get("batch_pause_every", 30)
    batch_seconds = upload_cfg.get("batch_pause_seconds", 60)
    delay_between = upload_cfg.get("delay_between_files", 2)
    max_retry = upload_cfg.get("retry_max", 3)

    for i, (file_path_str, source_label, rel_path_in_source) in enumerate(scanned, 1):
        file_p = Path(file_path_str)
        if not file_p.exists():
            continue

        # ── v7.2.2: cache key unik — {source_label}/{rel_path} ──
        cache_key = f"{source_label}/{rel_path_in_source}"
        rel_path = cache_key

        # Kategori dari subfolder
        folder_cat = os.path.dirname(rel_path_in_source).replace("\\", "/")
        if not folder_cat or folder_cat == ".":
            folder_cat = source_label or "General"

        stat = file_p.stat()
        file_mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat.st_mtime))
        ext = file_p.suffix.lower().replace(".", "").upper()

        # ── Cek cache ──
        cached_entry = cache.get(cache_key)
        catbox_url = None
        video_thumb_url = None
        thumb_url = None
        upload_time = None
        cached_meta = None

        if isinstance(cached_entry, dict):
            catbox_url = cached_entry.get("url")
            video_thumb_url = cached_entry.get("video_thumb_url")
            thumb_url = cached_entry.get("thumb_url")
            upload_time = cached_entry.get("uploaded_at")
            if (cached_entry.get("file_mtime_ns") == stat.st_mtime_ns
                    and cached_entry.get("file_size") == stat.st_size):
                cached_meta = cached_entry.get("meta")
        elif isinstance(cached_entry, str):
            catbox_url = cached_entry

        # ── Upload atau skip ──
        if not catbox_url:
            try:
                catbox_url = upload_to_catbox(
                    file_p,
                    userhash=userhash,
                    label=file_p.name,
                    is_thumb=False,
                    max_retry=max_retry,
                    batch_pause_every=batch_every,
                    batch_pause_seconds=batch_seconds,
                    delay_between_files=delay_between,
                )
                upload_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                with up._STATS_LOCK:
                    up.SESSION_STATS["success_uploads"] += 1

                ok, msg = verify_uploaded_file(catbox_url, stat.st_size)
                if not ok:
                    print_warning(f"  ⚠️\033[6G{msg}")
                    cache.pop(cache_key, None)
                    with up._STATS_LOCK:
                        up.SESSION_STATS["failed_uploads"] += 1
                    continue
            except Exception as e:
                with up._STATS_LOCK:
                    up.SESSION_STATS["failed_uploads"] += 1
                print(f"  {C_RED}⚠️\033[6GGagal: {file_p.name}{C_RESET}")
                print(f"      {C_SILVER}└─ {type(e).__name__}: {str(e)[:200]}{C_RESET}")
                continue
        else:
            with up._STATS_LOCK:
                up.SESSION_STATS["cached_count"] += 1

        media_type = get_media_type(file_p)

        # ── Thumbnail ──
        if media_type == "video" and not video_thumb_url:
            local_thumb = generate_video_thumbnail(file_p)
            if local_thumb and os.path.exists(local_thumb):
                try:
                    video_thumb_url = upload_to_catbox(
                        local_thumb,
                        userhash=userhash,
                        label=f"thumb_{file_p.stem[:12]}.jpg",
                        is_thumb=True,
                    )
                except Exception:
                    video_thumb_url = None

        if media_type == "image" and cfg.get("upload_thumbnails", True) and not thumb_url:
            local_thumb = generate_image_thumbnail(file_p)
            if local_thumb and os.path.exists(local_thumb):
                try:
                    thumb_url = upload_to_catbox(
                        local_thumb,
                        userhash=userhash,
                        label=f"thumb_{file_p.stem[:12]}.webp",
                        is_thumb=True,
                    )
                except Exception:
                    thumb_url = None

        # ── Meta ──
        if cached_meta is not None:
            exif_meta = cached_meta.get("exif", {})
            auto_tags = cached_meta.get("tags", [])
            media_date = cached_meta.get("date", file_mtime)
            year_str = cached_meta.get("year", "1970")
            year_month = cached_meta.get("month_key", "1970-01")
            month_display = cached_meta.get("month_display", "")
        else:
            exif_meta = extract_detailed_exif(file_p) if media_type == "image" else {}
            date_from_name = extract_date_from_filename(file_p.name)

            if exif_meta.get("original_date"):
                media_date = exif_meta["original_date"]
            elif date_from_name:
                if (date_from_name.get("hour", 0) or date_from_name.get("minute", 0)
                        or date_from_name.get("second", 0)):
                    media_date = date_from_name["datetime_str"]
                else:
                    media_date = date_from_name["date_str"]
            else:
                media_date = file_mtime

            date_parts = media_date.split(" ")[0].split("-")
            year_str = date_parts[0]
            month_idx = int(date_parts[1]) if len(date_parts) > 1 else 1
            year_month = f"{year_str}-{date_parts[1]:0>2}" if len(date_parts) > 1 else f"{year_str}-01"
            month_name = MONTH_NAMES_ID[month_idx] if 1 <= month_idx <= 12 else ""
            month_display = f"{month_name} {year_str}".strip()

            feat = cm.get_effective_config(slug)["global"].get("features", {})
            auto_tags = extract_auto_tags(
                file_p,
                folder_cat,
                exif_meta,
                media_type,
                enable_face_detect=feat.get("enable_face_detect", False),
                enable_color_tag=feat.get("enable_color_tag", True),
                enable_ocr=feat.get("enable_ocr", False),
                ocr_max_words=cm.get_effective_config(slug)["global"].get("ocr", {}).get("max_words", 3),
            )

        # ── Effective thumbnail URL ──
        if media_type == "image":
            effective_thumb = thumb_url or f"https://wsrv.nl/?url={catbox_url}&w=720&q=80&output=webp"
        else:
            effective_thumb = video_thumb_url or thumb_url or ""

        # ── Cache record ──
        cache_record = {
            "url": catbox_url,
            "source": source_label,
            "rel_path": rel_path_in_source,
            "uploaded_at": upload_time or file_mtime,
            "video_thumb_url": video_thumb_url,
            "thumb_url": thumb_url,
            "file_mtime_ns": stat.st_mtime_ns,
            "file_size": stat.st_size,
            "meta": {
                "exif": exif_meta or {},
                "tags": auto_tags or [],
                "date": media_date,
                "year": year_str,
                "month_key": year_month,
                "month_display": month_display,
            },
        }

        # ── Item data ──
        media_id = f"media_{hashlib.md5(rel_path.encode('utf-8')).hexdigest()[:12]}"
        item_data = {
            "id": media_id,
            "title": file_p.stem.replace("_", " ").title(),
            "filename": file_p.name,
            "category": folder_cat,
            "source": source_label,
            "date": media_date,
            "uploaded_at": upload_time,
            "year": year_str,
            "month_key": year_month,
            "month_display": month_display,
            "size": stat.st_size,
            "ext": ext,
            "type": media_type,
            "url": catbox_url,
            "thumb": effective_thumb,
            "video_thumb": video_thumb_url,
            "video_mime": get_video_mime(ext) if media_type == "video" else None,
            "geo": (exif_meta or {}).get("geo"),
            "camera": {
                "make": (exif_meta or {}).get("camera_make"),
                "model": (exif_meta or {}).get("camera_model"),
                "lens": (exif_meta or {}).get("lens_model"),
                "f_number": (exif_meta or {}).get("f_number"),
                "exposure": (exif_meta or {}).get("exposure_time"),
                "iso": (exif_meta or {}).get("iso"),
                "focal": (exif_meta or {}).get("focal_length"),
            },
            "tags": auto_tags,
        }

        cache[cache_key] = cache_record
        gallery_data.append(item_data)
        cache_dirty = True

    # ── Save cache ──
    if cache_dirty:
        _save_json(cache_file, cache)

    # ── End time ──
    with up._STATS_LOCK:
        up.SESSION_STATS["end_time"] = time.time()

    # ── Summary Report ──
    print_summary_report()

    # ── Load EMBED items ──
    embed_file = paths["embed_txt"]
    embed_items = _load_embed_items(embed_file, slug)
    if embed_items:
        print(f"  {C_MOSS_1}🌐\033[6GEmbed\033[14G{C_SILVER}:{C_RESET} {C_WHITE}{len(embed_items)} item dari embed.txt{C_RESET}")
        gallery_data.extend(embed_items)

    # ── Sort & filter blacklist ──
    gallery_data.sort(key=lambda x: x.get("date", ""), reverse=True)
    if deleted:
        before = len(gallery_data)
        gallery_data = [item for item in gallery_data if item["id"] not in deleted]
        removed = before - len(gallery_data)
        if removed > 0:
            print(f"  {C_SILVER}Blacklist\033[16G: {removed} item di-skip{C_RESET}")

    # ── Build HTML ──
    print()
    print(f"{C_MOSS_1}📄\033[6GGenerate HTML...{C_RESET}")

    eff = cm.get_effective_config(slug)
    autoplay_cfg = eff["global"].get("autoplay", {})
    items_per_page = eff["global"].get("gallery", {}).get("items_per_page", 24)
    theme = cm.get_theme_default()

    results = build_all(
        gallery_data,
        output_dir,
        project_title=cfg.get("judul_project", "lumoss"),
        items_per_page=items_per_page,
        autoplay_config=autoplay_cfg,
        theme=theme,
        deleted_data=deleted,
        account_info={"name": cfg.get("judul_project", slug), "slug": slug},
    )

    for fname, (ok, msg) in results.items():
        if ok:
            print_success(f"{fname}: {msg}")
        else:
            print_error(f"{fname}: {msg}")

    # ── Update stats akun ──
    try:
        am.update_account_stats(slug)
    except Exception:
        pass

    # ── Copy assets ──
    _copy_assets_to_output(paths["output_dir"])

    print()
    print_info(f"📂\033[6GBuka galeri: {output_dir}/index.html")
    print_info(f"⚙️\033[6GAtau manager: {output_dir}/manager.html")


# ═══════════════════════════════════════════════════════════
# CALLBACK: RUN REGENERATE
# ═══════════════════════════════════════════════════════════

def _callback_run_regenerate():
    """Callback: regenerate HTML dari cache (TANPA upload)."""
    slug = am.get_active_slug()
    if not slug:
        print_error("Belum ada akun aktif.")
        return

    try:
        from html_builder import build_all
        from account_manager import get_account_paths
    except ImportError as e:
        print_error(f"Gagal import module: {e}")
        return

    paths = get_account_paths(slug)
    cfg = cm.load_config(slug)

    output_dir = paths["output_dir"]
    cache_file = paths["cache"]
    deleted_file = paths["deleted"]

    print()
    print(f"{C_MOSS_1}━━━ 🔄\033[8MREGENERATE HTML ━━━{C_RESET}\n")
    print(f"  {C_MOSS_3}Akun\033[12G{C_SILVER}:{C_RESET} {C_WHITE}{slug}{C_RESET}")
    print(f"  {C_MOSS_3}Output\033[12G{C_SILVER}:{C_RESET} {C_WHITE}{output_dir}{C_RESET}")
    print()

    cache = _load_json(cache_file, default={})
    deleted = _load_json(deleted_file, default={})

    if not cache:
        print_warning("Cache kosong. Upload dulu via menu 1.")
        return

    print(f"  {C_MOSS_2}📊\033[6GCache\033[14G{C_SILVER}:{C_RESET} {C_WHITE}{len(cache)} entri{C_RESET}")
    print()

    try:
        from media_processor import (
            get_media_type, get_video_mime, VIDEO_EXTS,
        )
    except ImportError:
        get_media_type = None
        get_video_mime = None

    gallery_data = []
    skipped_missing = 0

    for cache_key, entry in cache.items():
        if not isinstance(entry, dict):
            continue
        url = entry.get("url")
        if not url:
            continue

        # v7.2.2: cache entry punya `source` & `rel_path`
        source_label = entry.get("source", "")
        rel_path_in_source = entry.get("rel_path", cache_key)

        # Coba rekonstruksi path
        file_exists = False
        file_p = None
        if source_label:
            # Cari di media_dirs
            for md in cm.get_enabled_media_dirs(slug):
                if md.get("label") == source_label:
                    candidate = os.path.join(md["path"], rel_path_in_source)
                    if os.path.exists(candidate):
                        file_p = Path(candidate)
                        file_exists = True
                        break

        if not file_exists:
            skipped_missing += 1

        meta = entry.get("meta", {}) or {}
        exif_meta = meta.get("exif", {}) or {}
        auto_tags = meta.get("tags", []) or []
        media_date = meta.get("date", "")
        year_str = meta.get("year", "1970")
        year_month = meta.get("month_key", "1970-01")
        month_display = meta.get("month_display", "")

        if not media_date:
            media_date = entry.get("uploaded_at", "")

        if file_exists and get_media_type:
            media_type = get_media_type(file_p)
        else:
            ext_low = os.path.splitext(rel_path_in_source)[1].lower().lstrip(".")
            media_type = "video" if ext_low in (
                "mp4", "mkv", "webm", "mov", "avi", "m4v", "ogv"
            ) else "image"

        # Kategori
        parts = rel_path_in_source.replace("\\", "/").split("/")
        if len(parts) > 1:
            folder_cat = "/".join(parts[:-1])
        else:
            folder_cat = source_label or "General"

        filename = parts[-1]
        title = os.path.splitext(filename)[0].replace("_", " ").title()
        ext = os.path.splitext(filename)[1].lstrip(".").upper()

        media_id = f"media_{hashlib.md5(cache_key.encode('utf-8')).hexdigest()[:12]}"

        thumb_url = entry.get("thumb_url")
        video_thumb_url = entry.get("video_thumb_url")
        if media_type == "image":
            effective_thumb = thumb_url or f"https://wsrv.nl/?url={url}&w=720&q=80&output=webp"
        else:
            effective_thumb = video_thumb_url or thumb_url or ""

        item_data = {
            "id": media_id,
            "title": title,
            "filename": filename,
            "category": folder_cat,
            "source": source_label,
            "date": media_date,
            "uploaded_at": entry.get("uploaded_at"),
            "year": year_str,
            "month_key": year_month,
            "month_display": month_display,
            "size": entry.get("file_size", 0),
            "ext": ext,
            "type": media_type,
            "url": url,
            "thumb": effective_thumb,
            "video_thumb": video_thumb_url,
            "video_mime": get_video_mime(ext) if (get_video_mime and media_type == "video") else None,
            "geo": exif_meta.get("geo"),
            "camera": {
                "make": exif_meta.get("camera_make"),
                "model": exif_meta.get("camera_model"),
                "lens": exif_meta.get("lens_model"),
                "f_number": exif_meta.get("f_number"),
                "exposure": exif_meta.get("exposure_time"),
                "iso": exif_meta.get("iso"),
                "focal": exif_meta.get("focal_length"),
            },
            "tags": auto_tags,
        }
        gallery_data.append(item_data)

    if skipped_missing > 0:
        print(f"  {C_YELLOW}⚠️\033[6G{skipped_missing} file di cache udah gak ada di folder{C_RESET}")
        print(f"  {C_SILVER}   Metadata tetep dipake dari cache{C_RESET}")
        print()

    print(f"  {C_MOSS_2}📄\033[6GItem\033[15G{C_SILVER}:{C_RESET} {C_WHITE}{len(gallery_data)} file dari cache{C_RESET}")

    # ── Load embed items ──
    embed_file = paths["embed_txt"]
    embed_items = _load_embed_items(embed_file, slug)
    if embed_items:
        print(f"  {C_MOSS_1}🌐\033[6GEmbed\033[14G{C_SILVER}:{C_RESET} {C_WHITE}{len(embed_items)} item{C_RESET}")
        gallery_data.extend(embed_items)

    # ── Sort & filter blacklist ──
    gallery_data.sort(key=lambda x: x.get("date", ""), reverse=True)
    if deleted:
        before = len(gallery_data)
        gallery_data = [item for item in gallery_data if item["id"] not in deleted]
        removed = before - len(gallery_data)
        if removed > 0:
            print(f"  {C_SILVER}Blacklist\033[16G: {removed} item di-skip{C_RESET}")

    # ── Build HTML ──
    print()
    print(f"{C_MOSS_1}📄\033[6GBuild HTML...{C_RESET}")

    eff = cm.get_effective_config(slug)
    autoplay_cfg = eff["global"].get("autoplay", {})
    items_per_page = eff["global"].get("gallery", {}).get("items_per_page", 24)
    theme = cm.get_theme_default()

    gh_user = (cfg.get("github_username") or "").strip()
    gh_repo_name = (cfg.get("github_repo") or "").strip()
    github_repo_str = f"{gh_user}/{gh_repo_name}" if gh_user and gh_repo_name else ""

    results = build_all(
        gallery_data,
        output_dir,
        project_title=cfg.get("judul_project", "lumoss"),
        items_per_page=items_per_page,
        autoplay_config=autoplay_cfg,
        theme=theme,
        deleted_data=deleted,
        account_info={"name": cfg.get("judul_project", slug), "slug": slug},
        github_repo=github_repo_str,
    )

    for fname, (ok, msg) in results.items():
        if ok:
            print_success(f"{fname}: {msg}")
        else:
            print_error(f"{fname}: {msg}")

    try:
        am.update_account_stats(slug)
    except Exception:
        pass

    _copy_assets_to_output(paths["output_dir"])

    print()
    print_info(f"📂\033[6GBuka galeri: {output_dir}/index.html")


# ═══════════════════════════════════════════════════════════
# CALLBACK: RUN ACCOUNT
# ═══════════════════════════════════════════════════════════

def _callback_run_account():
    """Callback: buka submenu account manager."""
    try:
        from menu_account import run_account_menu
        run_account_menu()
    except ImportError as e:
        print_error(f"menu_account.py tidak ada: {e}")


# ═══════════════════════════════════════════════════════════
# CALLBACK: RUN TOOLS
# ═══════════════════════════════════════════════════════════

def _callback_run_tools():
    """Callback: buka submenu tools."""
    try:
        from menu_tools import run_tools_menu
        run_tools_menu()
    except ImportError as e:
        print_error(f"menu_tools.py tidak ada: {e}")


# ═══════════════════════════════════════════════════════════
# CALLBACK: RUN EMBED
# ═══════════════════════════════════════════════════════════

def _callback_run_embed():
    """Callback: buka submenu import embed."""
    try:
        from menu_embed import run_embed_menu
        run_embed_menu()
    except ImportError as e:
        print_error(f"menu_embed.py tidak ada: {e}")


# ═══════════════════════════════════════════════════════════
# HELPER: EMBED ITEMS
# ═══════════════════════════════════════════════════════════

def _load_embed_items(embed_file, slug):
    """Load embed items dari embed.txt (1 URL per baris)."""
    if not os.path.exists(embed_file):
        return []

    try:
        from embed_parser import parse_embed_line
    except ImportError:
        return []

    items = []
    try:
        with open(embed_file, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    parsed = parse_embed_line(line, index=i, slug=slug)
                    if parsed:
                        items.append(parsed)
                except Exception:
                    continue
    except Exception:
        return []

    return items


# ═══════════════════════════════════════════════════════════
# HELPER: COPY ASSETS
# ═══════════════════════════════════════════════════════════

def _copy_assets_to_output(output_dir):
    """Copy template assets ke folder output akun."""
    assets_src = os.path.join("templates", "assets")
    if not os.path.isdir(assets_src):
        return
    assets_dst = os.path.join(output_dir, "assets")
    try:
        import shutil as _sh
        if os.path.exists(assets_dst):
            _sh.rmtree(assets_dst, ignore_errors=True)
        _sh.copytree(assets_src, assets_dst)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════

def _format_bytes(b):
    if not b or b == 0:
        return "0 B"
    val = float(b)
    units = ["B", "kB", "MB", "GB"]
    i = 0
    while val >= 1024 and i < len(units) - 1:
        val /= 1024
        i += 1
    return f"{val:.1f} {units[i]}"


def _load_json(path, default=None):
    if not os.path.exists(path):
        return default if default is not None else {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default if default is not None else {}


def _save_json(path, data):
    tmp = path + ".tmp"
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════

def main():
    """Entry point utama lumoss."""
    args = sys.argv[1:]

    callbacks = {
        "run_upload": _callback_run_upload,
        "run_regenerate": _callback_run_regenerate,
        "run_account": _callback_run_account,
        "run_tools": _callback_run_tools,
        "run_embed": _callback_run_embed,
    }

    if args and args[0] == "upload":
        slug = am.get_active_slug()
        if not slug:
            print_error("Belum ada akun aktif.")
            print_info("Jalankan: python lumoss.py")
            sys.exit(1)
        _callback_run_upload()
        return

    if args and args[0] in ("regen", "regenerate"):
        slug = am.get_active_slug()
        if not slug:
            print_error("Belum ada akun aktif.")
            print_info("Jalankan: python lumoss.py")
            sys.exit(1)
        _callback_run_regenerate()
        return

    try:
        menu.run_menu(callbacks=callbacks)
    except KeyboardInterrupt:
        print()
        print(f"\n{C_YELLOW}  ⚠️\033[7GDibatalkan oleh user.{C_RESET}")
        print(f"{C_SILVER}  Sampai nanti boss! 👋{C_RESET}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()