"""
lumoss — Embed Parser (v7.2.13 MEDIA GARDEN)
Parse URL dari embed.txt jadi item gallery_data.

Changelog v7.2.13:
- FIX (PR-9): Deteksi embed vs video lebih akurat
  · A1: Cek extension di query string (bukan cuma path)
  · A2: Tambah HLS/DASH extension (.m3u8, .mpd)
  · A3: is_embed_url() lebih strict (whitelist platform)
  · A4: _parse_generic() cek whitelist domain embed-able
  · A5: _parse_twitter() catat endpoint deprecated
- NEW (Auto-Tag):
  · B1: _extract_embed_tags() — extract tag dari URL path
  · B2: _fetch_page_title() — fetch HTML title (opt-in)
  · B3: Config toggle enable_embed_autotag
  · B4: Config toggle embed_autotag_fetch_title
  · B5: Integrasi ke _build_base_item()
- NEW (Platform Icon support):
  · G4: Tambah field `platform` (slug lowercase) di item dict

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
import json
from datetime import datetime

try:
    from urllib.parse import urlparse, parse_qs, quote
except ImportError:
    from urlparse import urlparse, parse_qs


MONTH_NAMES_ID = [
    "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]

IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".ico", ".tiff", ".heic")
VIDEO_EXTS = (
    ".mp4", ".mkv", ".webm", ".mov", ".avi", ".m4v", ".ogv",
    ".m3u8",  # HLS playlist
    ".mpd",   # DASH manifest
    ".flv",   # Flash video (legacy)
    ".wmv",   # Windows Media
)

# v7.2.13: Whitelist domain yang emang support iframe embed
EMBED_WHITELIST = {
    # Video platform
    "youtube.com", "youtu.be", "youtube-nocookie.com",
    "vimeo.com", "player.vimeo.com",
    "dailymotion.com", "dai.ly",
    "twitch.tv",
    "bitchute.com",
    "odysee.com",
    "rumble.com",
    # Audio platform
    "soundcloud.com",
    "spotify.com", "open.spotify.com",
    "bandcamp.com",
    # Code / dev
    "codepen.io", "jsfiddle.net", "jsbin.com", "replit.com",
    "github.dev", "gist.github.com",
    # Social
    "twitter.com", "x.com", "platform.twitter.com",
    "instagram.com", "facebook.com", "tiktok.com",
    # Maps
    "google.com", "maps.google.com", "openstreetmap.org",
    # Docs
    "docs.google.com", "drive.google.com",
}

# v7.2.13: Mapping platform slug → display name
PLATFORM_DISPLAY = {
    "youtube": "YouTube",
    "instagram": "Instagram",
    "facebook": "Facebook",
    "tiktok": "TikTok",
    "twitter": "Twitter/X",
    "vimeo": "Vimeo",
    "direct_image": "Direct Image",
    "direct_video": "Direct Video",
    "generic": "Generic Embed",
}


# ═══════════════════════════════════════════════════════════
# HELPER — URL ANALYSIS
# ═══════════════════════════════════════════════════════════

def _url_has_ext(url, exts):
    """
    v7.2.13 (A1): Cek extension di path ATAU query string.
    
    Contoh yang ke-handle:
    - https://example.com/foto.jpg           → path match
    - https://example.com/foto.jpg?x=1       → path match
    - https://example.com/download?file=a.jpg → query match
    """
    try:
        parsed = urlparse(url)
        path_low = parsed.path.lower()
        if any(path_low.endswith(ext) for ext in exts):
            return True
        query_low = parsed.query.lower()
        # Cek token di query: file=xxx.jpg
        for param_val in parse_qs(parsed.query).values():
            for v in param_val:
                if any(v.lower().endswith(ext) for ext in exts):
                    return True
        return False
    except Exception:
        return False


def _is_domain_in_whitelist(url):
    """
    v7.2.13 (A4): Cek apakah domain URL ada di whitelist embed.
    """
    try:
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        # Hapus port kalo ada
        if ":" in host:
            host = host.split(":")[0]
        # Hapus www prefix
        if host.startswith("www."):
            host = host[4:]
        return host in EMBED_WHITELIST
    except Exception:
        return False


# ═══════════════════════════════════════════════════════════
# HELPER — AUTO-TAG (v7.2.13)
# ═══════════════════════════════════════════════════════════

# Stop words yang gak jadi tag
_EMBED_STOP_WORDS = {
    "the", "and", "for", "with", "from", "into", "onto", "over", "under",
    "this", "that", "these", "those", "here", "there", "when", "where",
    "what", "which", "who", "why", "how", "also", "just", "only", "very",
    "more", "most", "less", "least", "many", "much", "some", "any",
    "all", "each", "every", "both", "either", "neither", "none",
    "http", "https", "www", "com", "net", "org", "html", "htm",
    "watch", "video", "videos", "photo", "photos", "pic", "pics",
    "embed", "embedded", "share", "shared", "post", "posts",
    "official", "channel", "user", "profile", "page", "content",
    "yang", "dan", "atau", "untuk", "dengan", "dari", "ke", "di", "pada",
    "adalah", "akan", "sudah", "telah", "sedang", "masih", "belum",
    "ini", "itu", "sini", "sana", "mana", "kapan", "siapa", "apa",
    "juga", "saja", "hanya", "sangat", "lebih", "paling", "kurang",
}


def _extract_embed_tags(url, platform, slug="default"):
    """
    v7.2.13 (B1): Extract tag dari URL embed.
    
    Coba berbagai strategi:
    1. Extract dari path URL (kayak /foto_liburan_bali.jpg)
    2. Extract dari slug Instagram (kayak /p/Cxyz123 → gak dapet)
    3. Extract dari YouTube video ID (kayak dQw4w9WgXcQ → gak dapet)
    
    Return: list tag (max 8, exclude platform dasar)
    """
    tags = []
    seen = set()
    
    def _add(tag):
        if not tag:
            return
        t = str(tag).strip().lower()
        if len(t) < 3 or t.isdigit():
            return
        if t in _EMBED_STOP_WORDS:
            return
        if t in seen:
            return
        seen.add(t)
        tags.append(t)
    
    try:
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        
        # Skip kalo path cuma ID (YouTube, IG, TikTok)
        # Contoh: /watch, /p/Cxyz, /@user/video/123
        if platform in ("youtube", "instagram", "tiktok"):
            # Coba extract dari query (YouTube watch?v=)
            pass  # ID doang, gak ada tag
        
        # Tokenize path
        # Split by /, -, _, ., +
        tokens = re.split(r"[/\-_.+]", path)
        for tok in tokens:
            # Filter token yang isinya cuma angka atau hex
            if re.match(r"^[a-f0-9]{6,}$", tok, re.IGNORECASE):
                continue
            if tok.isdigit():
                continue
            # Filter yang kayak video ID YouTube (11 char, campur)
            if len(tok) == 11 and re.match(r"^[A-Za-z0-9_-]+$", tok):
                continue
            # Filter yang kayak IG shortcode (11 char base64)
            if len(tok) == 11 and re.match(r"^[A-Za-z0-9_-]+$", tok):
                continue
            _add(tok)
        
        # Coba extract dari query (?title=xxx, ?name=xxx)
        qs = parse_qs(parsed.query)
        for key in ("title", "name", "q", "query", "text", "caption"):
            for v in qs.get(key, []):
                for tok in re.split(r"[\s\-_.+]+", v):
                    _add(tok)
    
    except Exception:
        pass
    
    # Batasi max 8 tag
    return tags[:8]


def _fetch_page_title(url, timeout=5):
    """
    v7.2.13 (B2): Fetch HTML page + extract <title> tag.
    
    Opt-in via config: enable_embed_autotag + embed_autotag_fetch_title
    
    Return: string title, atau "" kalo gagal.
    """
    try:
        import requests
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 lumoss/7.2.13"
            ),
        }
        r = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        if r.status_code != 200:
            return ""
        
        # Extract <title>...</title> — case insensitive
        match = re.search(
            r"<title[^>]*>(.*?)</title>",
            r.text,
            re.IGNORECASE | re.DOTALL,
        )
        if not match:
            return ""
        
        title = match.group(1).strip()
        # Bersihin HTML entities
        title = title.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        title = title.replace("&quot;", '"').replace("&#39;", "'")
        # Batasi panjang
        if len(title) > 200:
            title = title[:200]
        return title
    except Exception:
        return ""


def _should_enable_autotag():
    """Cek config: enable_embed_autotag."""
    try:
        from config_manager import get_global_value
        return bool(get_global_value("features.enable_embed_autotag", True))
    except Exception:
        return True  # default ON


def _should_fetch_title():
    """Cek config: embed_autotag_fetch_title."""
    try:
        from config_manager import get_global_value
        return bool(get_global_value("features.embed_autotag_fetch_title", False))
    except Exception:
        return False  # default OFF


# ═══════════════════════════════════════════════════════════
# PARSE — ENTRY POINT
# ═══════════════════════════════════════════════════════════

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
    """
    Deteksi platform dari URL.
    
    v7.2.13 (A1): Cek extension di path + query string.
    v7.2.13 (A2): Tambah HLS/DASH extension.
    """
    u = url.lower()

    # Cek direct image/video (path ATAU query)
    if _url_has_ext(url, IMAGE_EXTS):
        return "direct_image"
    if _url_has_ext(url, VIDEO_EXTS):
        return "direct_video"

    # Cek platform spesifik (host based)
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
    """
    Build base item dict (sebelum parsing spesifik).
    
    v7.2.13: Tambah field `platform` + auto-tag.
    """
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

    # v7.2.13 (B1): Auto-tag dari URL
    embed_tags = []
    if _should_enable_autotag():
        embed_tags = _extract_embed_tags(url, platform, slug)

    # v7.2.13 (B2): Fetch HTML title (opt-in)
    if _should_enable_autotag() and _should_fetch_title():
        try:
            title = _fetch_page_title(url)
            if title:
                # Extract kata dari title, gabung ke tags
                title_tokens = re.findall(r"[A-Za-z]{3,}", title)
                for tok in title_tokens[:5]:
                    tok_low = tok.lower()
                    if tok_low not in _EMBED_STOP_WORDS and tok_low not in embed_tags:
                        embed_tags.append(tok_low)
                # Batasi max 10
                embed_tags = embed_tags[:10]
        except Exception:
            pass

    # Platform display name
    platform_display = PLATFORM_DISPLAY.get(platform, platform.title())

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
        "tags": ["embed", platform] + embed_tags,
        "source": platform_display,
        "platform": platform,  # v7.2.13 (G4): slug lowercase
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
    base["platform"] = "youtube"
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
        base["platform"] = "instagram"
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
        base["platform"] = "facebook"
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
        base["platform"] = "tiktok"
        base["original_url"] = url
        base["aspect_ratio"] = "9/16"
        base["tags"] = ["embed", "tiktok"]
        return base
    except Exception:
        return None


def _parse_twitter(url, base):
    """
    Parse Twitter/X URL.
    
    v7.2.13 (A5): Endpoint platform.twitter.com udah deprecated (2023).
    Twitter/X sekarang cuma support blockquote embed (butuh JS).
    
    Solusi sementara: tampilin sebagai link preview.
    """
    try:
        # Set type jadi "embed" tapi tandai "twitter" (buat icon)
        # Lightbox bakal nampilin fallback UI (link ke original_url)
        base["url"] = url  # Langsung URL original, bukan iframe
        base["title"] = "Twitter/X Post"
        base["filename"] = "twitter_post.html"
        base["ext"] = "URL"
        base["type"] = "embed"
        base["source"] = "Twitter/X"
        base["platform"] = "twitter"
        base["original_url"] = url
        base["aspect_ratio"] = "16/9"
        base["tags"] = ["embed", "twitter"]
        # Flag buat frontend — tampilin fallback UI, jangan iframe
        base["no_iframe"] = True
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
        base["platform"] = "vimeo"
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
        base["platform"] = "direct_image"
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
        base["platform"] = "direct_video"
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
        "m3u8": "application/x-mpegURL",
        "mpd": "application/dash+xml",
        "flv": "video/x-flv",
        "wmv": "video/x-ms-wmv",
    }.get(ext, "video/mp4")


def _parse_generic(url, base):
    """
    Fallback: coba iframe embed langsung.
    
    v7.2.13 (A4): Cek whitelist domain.
    - Kalo di whitelist → iframe (embed URL)
    - Kalo gak → direct link (buka di tab baru)
    """
    is_whitelisted = _is_domain_in_whitelist(url)
    
    base["url"] = url
    base["title"] = "Embed — Unknown"
    base["filename"] = "embed.html"
    base["ext"] = "URL"
    base["type"] = "embed"
    base["source"] = "Generic"
    base["platform"] = "generic"
    base["original_url"] = url
    
    if not is_whitelisted:
        # Gak di whitelist — flag buat frontend
        base["no_iframe"] = True
    
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
    """
    Quick check: URL ini embed-able atau direct link.
    
    v7.2.13 (A3): Lebih strict — cek whitelist platform.
    """
    platform = detect_platform(url)
    # Direct image/video BUKAN embed
    if platform in ("direct_image", "direct_video"):
        return False
    # Platform spesifik yang emang support embed
    if platform in ("youtube", "instagram", "tiktok", "vimeo", "facebook", "twitter"):
        return True
    # Generic — cek whitelist domain
    if platform == "generic":
        return _is_domain_in_whitelist(url)
    return False


__all__ = [
    "parse_embed_line",
    "parse_file",
    "detect_platform",
    "is_embed_url",
    "IMAGE_EXTS",
    "VIDEO_EXTS",
    "MONTH_NAMES_ID",
    "EMBED_WHITELIST",
    "PLATFORM_DISPLAY",
]