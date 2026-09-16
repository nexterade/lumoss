"""
lumoss — Embed Parser (v7.2.11 MEDIA GARDEN)
Parse URL dari embed.txt jadi item gallery_data.

Changelog v7.2.11:
- Deteksi aspect_ratio per platform (landscape/portrait)

Support:
- Direct link: .jpg, .jpeg, .png, .gif, .webp, .bmp, .mp4, .mkv, .webm, .mov, .avi
- YouTube: watch?v=, youtu.be/, shorts/, embed/
- Instagram: /p/, /reel/, /tv/
- Facebook: /watch?v=, /videos/, fb.watch/
- TikTok: /@user/video/
- Twitter/X: /status/
- Vimeo: /123456789
"""

import os
import re
import hashlib
from datetime import datetime

try:
    from urllib.parse import urlparse, parse_qs, quote
except ImportError:
    from urlparse import urlparse, parse_qs


MONTH_NAMES_ID = [
    "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]

IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg")
VIDEO_EXTS = (".mp4", ".mkv", ".webm", ".mov", ".avi", ".m4v", ".ogv")


def parse_embed_line(url, index=1, slug="default"):
    """Parse 1 baris URL jadi item dict."""
    url = (url or "").strip()
    if not url or url.startswith("#"):
        return None

    if not (url.startswith("http://") or url.startswith("https://")):
        return None

    platform = detect_platform(url)
    base = _build_base_item(url, index, slug, platform)

    if platform == "youtube":
        result = _parse_youtube(url, base)
    elif platform == "instagram":
        result = _parse_instagram(url, base)
    elif platform == "facebook":
        result = _parse_facebook(url, base)
    elif platform == "tiktok":
        result = _parse_tiktok(url, base)
    elif platform == "twitter":
        result = _parse_twitter(url, base)
    elif platform == "vimeo":
        result = _parse_vimeo(url, base)
    elif platform == "direct_image":
        result = _parse_direct_image(url, base)
    elif platform == "direct_video":
        result = _parse_direct_video(url, base)
    else:
        result = _parse_generic(url, base)

    return result


def detect_platform(url):
    """Deteksi platform dari URL."""
    u = url.lower()

    path = urlparse(url).path.lower()
    if any(path.endswith(ext) for ext in IMAGE_EXTS):
        return "direct_image"
    if any(path.endswith(ext) for ext in VIDEO_EXTS):
        return "direct_video"

    if "youtube.com" in u or "youtu.be" in u or "youtube-nocookie.com" in u:
        return "youtube"
    if "instagram.com" in u or "instagr.am" in u:
        return "instagram"
    if "facebook.com" in u or "fb.watch" in u or "fb.com" in u:
        return "facebook"
    if "tiktok.com" in u:
        return "tiktok"
    if "twitter.com" in u or "x.com" in u:
        return "twitter"
    if "vimeo.com" in u:
        return "vimeo"

    return "generic"


def _build_base_item(url, index, slug, platform):
    """Build base item dict (sebelum parsing spesifik)."""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")
    year_str = now.strftime("%Y")
    month_key = now.strftime("%Y-%m")
    month_idx = now.month
    month_display = f"{MONTH_NAMES_ID[month_idx]} {year_str}"

    raw_id = f"{slug}:{url}:{index}"
    media_id = f"embed_{hashlib.md5(raw_id.encode('utf-8')).hexdigest()[:12]}"

    try:
        parsed = urlparse(url)
        path = parsed.path or ""
        filename = os.path.basename(path) or f"embed_{index}"
    except Exception:
        filename = f"embed_{index}"

    return {
        "id": media_id,
        "title": filename,
        "filename": filename,
        "category": "Embed",
        "date": date_str,
        "uploaded_at": None,
        "year": year_str,
        "month_key": month_key,
        "month_display": month_display,
        "size": 0,
        "ext": "URL",
        "type": "embed",
        "url": url,
        "thumb": "",
        "video_thumb": None,
        "video_mime": None,
        "geo": None,
        "camera": {},
        "tags": ["embed", platform],
        "source": platform.title(),
        "original_url": url,
        "aspect_ratio": "16/9",
    }


def _parse_youtube(url, base):
    """Parse YouTube URL → embed URL + thumbnail.

    v7.2.9 (PR-7): Fix error 153 dengan parameter origin + enablejsapi.
    v7.2.11: Deteksi aspect ratio (shorts = 9:16, watch = 16:9).
    """
    video_id = _extract_youtube_id(url)
    if not video_id:
        return None

    params = (
        "?origin={ORIGIN}"
        "&enablejsapi=1"
        "&rel=0"
        "&modestbranding=1"
        "&playsinline=1"
    )

    is_shorts = "/shorts/" in url.lower()
    aspect = "9/16" if is_shorts else "16/9"

    base["url"] = f"https://www.youtube.com/embed/{video_id}{params}"
    base["thumb"] = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    base["title"] = f"YouTube — {video_id}"
    base["filename"] = f"youtube_{video_id}.mp4"
    base["ext"] = "MP4"
    base["type"] = "embed"
    base["source"] = "YouTube"
    base["original_url"] = url
    base["aspect_ratio"] = aspect
    base["tags"] = ["embed", "youtube", "video"]
    if is_shorts:
        base["tags"].append("shorts")
    return base


def _extract_youtube_id(url):
    """Extract video ID dari berbagai format YouTube URL."""
    try:
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        path = parsed.path
        qs = parse_qs(parsed.query)

        if "youtu.be" in host:
            vid = path.lstrip("/").split("/")[0]
            return vid if vid else None

        if "watch" in path:
            v = qs.get("v", [None])[0]
            if v:
                return v

        if "/embed/" in path:
            return path.split("/embed/")[1].split("/")[0].split("?")[0]

        if "/shorts/" in path:
            return path.split("/shorts/")[1].split("/")[0].split("?")[0]

        if "/v/" in path:
            return path.split("/v/")[1].split("/")[0].split("?")[0]
    except Exception:
        return None
    return None


def _parse_instagram(url, base):
    """Parse Instagram URL → embed URL.

    v7.2.9 (PR-8): /captioned/ biar caption + media muncul.
    v7.2.11: Deteksi aspect ratio (reel/tv = 9:16, post = 4:5).
    """
    try:
        parsed = urlparse(url)
        path = parsed.path.rstrip("/")
        parts = [p for p in path.split("/") if p]
        if len(parts) < 2:
            return None

        post_type = parts[0]
        shortcode = parts[1]

        embed_url = f"https://www.instagram.com/{post_type}/{shortcode}/embed/captioned/"
        base["url"] = embed_url
        base["thumb"] = ""
        base["title"] = f"Instagram — {shortcode}"
        base["filename"] = f"instagram_{shortcode}.mp4"
        base["ext"] = "MP4"
        base["type"] = "embed"
        base["source"] = "Instagram"
        base["original_url"] = url

        if post_type in ("reel", "tv"):
            base["aspect_ratio"] = "9/16"
        else:
            base["aspect_ratio"] = "4/5"

        base["tags"] = ["embed", "instagram"]
        if post_type == "reel":
            base["tags"].append("reel")
        return base
    except Exception:
        return None


def _parse_facebook(url, base):
    """Parse Facebook URL → plugin embed URL."""
    try:
        encoded = quote(url, safe="")
        embed_url = (
            f"https://www.facebook.com/plugins/video.php?"
            f"href={encoded}&show_text=false&width=560"
        )
        base["url"] = embed_url
        base["title"] = "Facebook Video"
        base["filename"] = "facebook_video.mp4"
        base["ext"] = "MP4"
        base["type"] = "embed"
        base["source"] = "Facebook"
        base["original_url"] = url
        base["aspect_ratio"] = "16/9"
        base["tags"] = ["embed", "facebook"]
        return base
    except Exception:
        return None


def _parse_tiktok(url, base):
    """Parse TikTok URL → embed URL."""
    try:
        parsed = urlparse(url)
        path = parsed.path.rstrip("/")
        parts = [p for p in path.split("/") if p]
        video_id = None
        if "video" in parts:
            idx = parts.index("video")
            if idx + 1 < len(parts):
                video_id = parts[idx + 1]

        if not video_id:
            return None

        embed_url = f"https://www.tiktok.com/embed/v2/{video_id}"
        base["url"] = embed_url
        base["title"] = f"TikTok — {video_id}"
        base["filename"] = f"tiktok_{video_id}.mp4"
        base["ext"] = "MP4"
        base["type"] = "embed"
        base["source"] = "TikTok"
        base["original_url"] = url
        base["aspect_ratio"] = "9/16"
        base["tags"] = ["embed", "tiktok"]
        return base
    except Exception:
        return None


def _parse_twitter(url, base):
    """Parse Twitter/X URL → embed via platform.twitter.com."""
    try:
        clean_url = url.replace("x.com", "twitter.com")
        encoded = quote(clean_url, safe="")
        embed_url = f"https://platform.twitter.com/embed/Tweet.html?url={encoded}"
        base["url"] = embed_url
        base["title"] = "Twitter/X Post"
        base["filename"] = "twitter_post.html"
        base["ext"] = "HTML"
        base["type"] = "embed"
        base["source"] = "Twitter/X"
        base["original_url"] = url
        base["aspect_ratio"] = "16/9"
        base["tags"] = ["embed", "twitter"]
        return base
    except Exception:
        return None


def _parse_vimeo(url, base):
    """Parse Vimeo URL → embed URL."""
    try:
        parsed = urlparse(url)
        path = parsed.path.rstrip("/")
        video_id = path.lstrip("/").split("/")[0]
        if not video_id or not video_id.isdigit():
            return None

        embed_url = f"https://player.vimeo.com/video/{video_id}"
        base["url"] = embed_url
        base["title"] = f"Vimeo — {video_id}"
        base["filename"] = f"vimeo_{video_id}.mp4"
        base["ext"] = "MP4"
        base["type"] = "embed"
        base["source"] = "Vimeo"
        base["original_url"] = url
        base["aspect_ratio"] = "16/9"
        base["tags"] = ["embed", "vimeo", "video"]
        return base
    except Exception:
        return None


def _parse_direct_image(url, base):
    """Parse direct image URL."""
    try:
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path) or "image.jpg"
        ext = os.path.splitext(filename)[1].lstrip(".").upper() or "JPG"

        base["url"] = url
        base["thumb"] = url
        base["title"] = filename
        base["filename"] = filename
        base["ext"] = ext
        base["type"] = "image"
        base["source"] = "Direct Link"
        base["tags"] = ["embed", "direct", "image"]
        return base
    except Exception:
        return None


def _parse_direct_video(url, base):
    """Parse direct video URL."""
    try:
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path) or "video.mp4"
        ext = os.path.splitext(filename)[1].lstrip(".").upper() or "MP4"

        base["url"] = url
        base["thumb"] = ""
        base["title"] = filename
        base["filename"] = filename
        base["ext"] = ext
        base["type"] = "video"
        base["video_mime"] = _mime_for_ext(ext)
        base["source"] = "Direct Link"
        base["aspect_ratio"] = "16/9"
        base["tags"] = ["embed", "direct", "video"]
        return base
    except Exception:
        return None


def _mime_for_ext(ext):
    """MIME type untuk video ekstensi."""
    ext = ext.lower()
    return {
        "mp4": "video/mp4",
        "webm": "video/webm",
        "mov": "video/quicktime",
        "mkv": "video/x-matroska",
        "avi": "video/x-msvideo",
        "m4v": "video/x-m4v",
        "ogv": "video/ogg",
    }.get(ext, "video/mp4")


def _parse_generic(url, base):
    """Fallback: coba iframe embed langsung."""
    base["url"] = url
    base["title"] = "Embed — Unknown"
    base["filename"] = "embed.html"
    base["ext"] = "URL"
    base["type"] = "embed"
    base["source"] = "Generic"
    base["tags"] = ["embed", "generic"]
    return base


def parse_file(embed_file, slug="default"):
    """Parse semua URL dari embed.txt → list item."""
    if not os.path.exists(embed_file):
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


def is_embed_url(url):
    """Quick check: URL ini embed-able atau direct link."""
    platform = detect_platform(url)
    return platform not in ("direct_image", "direct_video")


__all__ = [
    "parse_embed_line",
    "parse_file",
    "detect_platform",
    "is_embed_url",
    "IMAGE_EXTS",
    "VIDEO_EXTS",
    "MONTH_NAMES_ID",
]