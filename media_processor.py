"""
Lumoss — Media Processor
Pengolah media: EXIF, thumbnail, auto-tag, auto-date.

Fitur:
- Extract EXIF (kamera, GPS, ISO, exposure, focal length)
- Generate thumbnail (WebP untuk gambar, JPG untuk video via FFmpeg)
- Auto-tag dari nama file + folder + EXIF + warna dominan
- Auto-detect tanggal dari nama file (support berbagai format)
- OCR & face detection (opsional, opt-in via config)
"""

import os
import re
import time
import hashlib
import tempfile
import subprocess
import threading
import shutil
from pathlib import Path
from datetime import datetime

# ── Optional: Pillow ──
try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS, IFD
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    IFD = None

# ── Optional: Tesseract OCR ──
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

# ── Optional: OpenCV (face detect) ──
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False


# ═══════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════

SUPPORTED_IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".ico"}
SUPPORTED_VIDEO_EXT = {".mp4", ".mkv", ".webm", ".mov"}
SUPPORTED_EXTENSIONS = SUPPORTED_IMAGE_EXT | SUPPORTED_VIDEO_EXT

VIDEO_EXTS = {"MP4", "MKV", "WEBM", "MOV"}
VIDEO_MIME = {
    "MP4": "video/mp4",
    "WEBM": "video/webm",
    "MOV": "video/quicktime",
    "MKV": "video/x-matroska",
}

FFMPEG_PATH = shutil.which("ffmpeg")

# Thumbnail settings
THUMBNAIL_DIR = os.path.join(tempfile.gettempdir(), "lumoss_thumbs")
THUMB_MAX_SIZE = 720
THUMB_QUALITY = 80
THUMB_CLEANUP_MAX_AGE_DAYS = 30

# Nama bulan Indonesia
MONTH_NAMES_ID = [
    "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
]

# Lock untuk face cascade
_FACE_CASCADE = None
_FACE_DETECTION_LOCK = threading.Lock()


# ═══════════════════════════════════════════════════════════
# DATE EXTRACTION DARI FILENAME
# ═══════════════════════════════════════════════════════════

_DATE_PATTERNS = [
    # YYYYMMDD_HHMMSS
    (r"(20\d{2})[-_.]?(\d{2})[-_.]?(\d{2})[_\-\s](\d{2})[-_.]?(\d{2})[-_.]?(\d{2})", "ymd_hms"),
    # YYYY-MM-DD atau YYYY_MM_DD
    (r"(20\d{2})[-_.](\d{1,2})[-_.](\d{1,2})", "ymd"),
    # DD-MM-YYYY atau DD_MM_YYYY
    (r"(\d{1,2})[-_.](\d{1,2})[-_.](20\d{2})", "dmy"),
    # YYYYMMDD (8 digit)
    (r"(?<!\d)(20\d{2})(\d{2})(\d{2})(?!\d)", "ymd"),
    # DDMMYYYY (8 digit)
    (r"(?<!\d)(\d{2})(\d{2})(20\d{2})(?!\d)", "dmy"),
    # YYYY-MM (year-month)
    (r"(20\d{2})[-_.](\d{1,2})(?![-_.]\d)", "ym"),
]


def extract_date_from_filename(filename):
    """
    Extract tanggal dari nama file.
    
    Returns:
        dict {
            year, month, day, hour, minute, second,
            date_str, datetime_str, month_display, month_key
        }
        atau None kalau tidak ada pola tanggal
    """
    stem = Path(filename).stem
    
    for pattern, order in _DATE_PATTERNS:
        m = re.search(pattern, stem)
        if not m:
            continue
        
        try:
            if order == "ymd_hms":
                y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
                hh, mm, ss = int(m.group(4)), int(m.group(5)), int(m.group(6))
            elif order == "ymd":
                y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
                hh, mm, ss = 0, 0, 0
            elif order == "dmy":
                d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
                hh, mm, ss = 0, 0, 0
            elif order == "ym":
                y, mo = int(m.group(1)), int(m.group(2))
                d, hh, mm, ss = 1, 0, 0, 0
            else:
                continue
            
            if not (2000 <= y <= 2099):
                continue
            if not (1 <= mo <= 12):
                continue
            if not (1 <= d <= 31):
                continue
            if not (0 <= hh <= 23):
                continue
            if not (0 <= mm <= 59):
                continue
            if not (0 <= ss <= 59):
                continue
            
            return {
                "year": y,
                "month": mo,
                "day": d,
                "hour": hh,
                "minute": mm,
                "second": ss,
                "date_str": f"{y:04d}-{mo:02d}-{d:02d}",
                "datetime_str": f"{y:04d}-{mo:02d}-{d:02d} {hh:02d}:{mm:02d}:{ss:02d}",
                "month_display": f"{MONTH_NAMES_ID[mo]} {y}",
                "month_key": f"{y:04d}-{mo:02d}",
            }
        except (ValueError, IndexError):
            continue
    
    return None


# ═══════════════════════════════════════════════════════════
# EXIF EXTRACTION
# ═══════════════════════════════════════════════════════════

def _convert_to_degrees(value):
    """Konversi GPS coordinates (DMS) ke degrees."""
    try:
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)
    except Exception:
        return None


def _ref_str(v):
    """Normalisasi GPS ref string."""
    if v is None:
        return ""
    if isinstance(v, bytes):
        v = v.decode("utf-8", errors="ignore")
    return str(v).strip().upper()


def _merge_exif_ifds(exif_obj, exif_dict):
    """Merge EXIF dari berbagai IFD (ExifIFD, GPSInfo)."""
    merged = dict(exif_dict) if exif_dict else {}
    
    try:
        if IFD is not None and exif_dict:
            for name in ("ExifIFD", "GPSInfo"):
                ifd_id = getattr(IFD, name, None)
                if ifd_id is None:
                    continue
                sub = exif_dict.get(ifd_id)
                if isinstance(sub, dict):
                    merged.update(sub)
    except Exception:
        pass
    
    try:
        if exif_obj is not None and hasattr(exif_obj, "get_ifd"):
            for ifd_id in (0x8769, 0x8825):  # ExifIFD, GPSInfo
                try:
                    sub = exif_obj.get_ifd(ifd_id)
                    if sub:
                        merged.update(sub)
                except Exception:
                    pass
    except Exception:
        pass
    
    return merged


def extract_detailed_exif(file_path):
    """
    Extract EXIF lengkap dari gambar.
    
    Returns:
        dict {
            geo, original_date, camera_make, camera_model,
            lens_model, f_number, exposure_time, iso,
            focal_length, dimensions
        }
    """
    result = {
        "geo": None,
        "original_date": None,
        "camera_make": None,
        "camera_model": None,
        "lens_model": None,
        "f_number": None,
        "exposure_time": None,
        "iso": None,
        "focal_length": None,
        "dimensions": None,
    }
    
    if not PILLOW_AVAILABLE:
        return result
    
    file_path = Path(file_path)
    if file_path.suffix.lower() not in {".jpg", ".jpeg", ".tiff", ".webp", ".png"}:
        return result
    
    try:
        with Image.open(file_path) as img:
            result["dimensions"] = img.size
            
            exif_obj = None
            exif = None
            
            try:
                exif_obj = img.getexif()
            except Exception:
                exif_obj = None
            
            try:
                exif = img._getexif() if hasattr(img, "_getexif") else None
            except Exception:
                exif = None
            
            merged = _merge_exif_ifds(exif_obj, exif)
            if not merged:
                return result
            
            gps_info = {}
            
            for tag_id, val in merged.items():
                tag_name = TAGS.get(tag_id, tag_id)
                
                if tag_name == "DateTimeOriginal":
                    try:
                        result["original_date"] = datetime.strptime(
                            str(val), "%Y:%m:%d %H:%M:%S"
                        ).strftime("%Y-%m-%d %H:%M:%S")
                    except Exception:
                        pass
                
                elif tag_name == "DateTime" and not result["original_date"]:
                    try:
                        result["original_date"] = datetime.strptime(
                            str(val), "%Y:%m:%d %H:%M:%S"
                        ).strftime("%Y-%m-%d %H:%M:%S")
                    except Exception:
                        pass
                
                elif tag_name == "Make":
                    result["camera_make"] = str(val).strip()
                
                elif tag_name == "Model":
                    result["camera_model"] = str(val).strip()
                
                elif tag_name == "LensModel":
                    result["lens_model"] = str(val).strip()
                
                elif tag_name == "FNumber":
                    try:
                        result["f_number"] = f"f/{float(val):.1f}"
                    except Exception:
                        pass
                
                elif tag_name == "ExposureTime":
                    try:
                        fval = float(val)
                        if fval < 1:
                            result["exposure_time"] = f"1/{int(round(1 / fval))}s"
                        else:
                            result["exposure_time"] = f"{fval}s"
                    except Exception:
                        result["exposure_time"] = str(val)
                
                elif tag_name == "ISOSpeedRatings":
                    result["iso"] = f"ISO {val}"
                
                elif tag_name == "FocalLength":
                    try:
                        result["focal_length"] = f"{float(val):.1f}mm"
                    except Exception:
                        pass
                
                elif tag_name == "GPSInfo":
                    for key, sub in (val.items() if isinstance(val, dict) else []):
                        gps_info[GPSTAGS.get(key, key)] = sub
            
            if gps_info:
                lat = _convert_to_degrees(gps_info.get("GPSLatitude"))
                lon = _convert_to_degrees(gps_info.get("GPSLongitude"))
                if lat is not None and lon is not None:
                    if _ref_str(gps_info.get("GPSLatitudeRef")) == "S":
                        lat = -lat
                    if _ref_str(gps_info.get("GPSLongitudeRef")) == "W":
                        lon = -lon
                    result["geo"] = {"lat": round(lat, 6), "lon": round(lon, 6)}
    except Exception:
        pass
    
    return result


# ═══════════════════════════════════════════════════════════
# THUMBNAIL GENERATION
# ═══════════════════════════════════════════════════════════

def generate_image_thumbnail(image_path, max_size=THUMB_MAX_SIZE, quality=THUMB_QUALITY):
    """
    Generate thumbnail WebP untuk gambar.
    Return path thumbnail, atau None kalau gagal.
    """
    if not PILLOW_AVAILABLE:
        return None
    
    ext = Path(image_path).suffix.lower()
    if ext in {".svg", ".ico"}:
        return None
    
    try:
        os.makedirs(THUMBNAIL_DIR, exist_ok=True)
        
        stat = os.stat(image_path)
        key = hashlib.md5(
            f"{image_path}|{stat.st_mtime_ns}|{stat.st_size}".encode("utf-8")
        ).hexdigest()[:20]
        out_path = os.path.join(THUMBNAIL_DIR, f"{key}.webp")
        
        # Cache hit
        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            return out_path
        
        with Image.open(image_path) as img:
            if getattr(img, "is_animated", False):
                img.seek(0)
            
            if img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGBA")
                bg = Image.new("RGB", img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[-1])
                img = bg
            else:
                img = img.convert("RGB")
            
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            img.save(out_path, "WEBP", quality=quality, method=4)
        
        return out_path
    except Exception:
        return None


def generate_video_thumbnail(video_path, max_size=THUMB_MAX_SIZE):
    """
    Generate thumbnail JPG dari video via FFmpeg.
    Return path thumbnail, atau None kalau gagal.
    """
    if not FFMPEG_PATH:
        return None
    
    try:
        temp_dir = tempfile.gettempdir()
        thumb_name = f"thumb_{hashlib.md5(str(video_path).encode()).hexdigest()[:12]}.jpg"
        thumb_path = os.path.join(temp_dir, thumb_name)
        
        if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 0:
            return thumb_path
        
        cmd = [
            FFMPEG_PATH, "-y",
            "-ss", "0.5",
            "-i", str(video_path),
            "-vframes", "1",
            "-vf", f"scale='min({max_size},iw)':-2",
            "-q:v", "3",
            thumb_path,
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
        
        if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 0:
            return thumb_path
        return None
    except Exception:
        return None


def cleanup_old_thumbnails(max_age_days=THUMB_CLEANUP_MAX_AGE_DAYS):
    """Hapus thumbnail lama (>N hari)."""
    if not os.path.isdir(THUMBNAIL_DIR):
        return 0
    
    cutoff = time.time() - max_age_days * 86400
    removed = 0
    
    # Cleanup THUMBNAIL_DIR
    for f in os.listdir(THUMBNAIL_DIR):
        p = os.path.join(THUMBNAIL_DIR, f)
        try:
            if os.path.isfile(p) and os.path.getmtime(p) < cutoff:
                os.remove(p)
                removed += 1
        except Exception:
            pass
    
    # Cleanup temp thumb_
    temp_dir = tempfile.gettempdir()
    for f in os.listdir(temp_dir):
        if f.startswith("thumb_") and f.endswith(".jpg"):
            p = os.path.join(temp_dir, f)
            try:
                if os.path.isfile(p) and os.path.getmtime(p) < cutoff:
                    os.remove(p)
                    removed += 1
            except Exception:
                pass
    
    return removed


# ═══════════════════════════════════════════════════════════
# COLOR DETECTION
# ═══════════════════════════════════════════════════════════

def detect_dominant_colors(image_path):
    """
    Deteksi warna dominan dari gambar (HSV-based).
    Return list tag warna.
    """
    if not PILLOW_AVAILABLE:
        return []
    
    try:
        with Image.open(image_path) as img:
            if getattr(img, "is_animated", False):
                img.seek(0)
            
            img = img.convert("RGB")
            if max(img.size) > 400:
                img.thumbnail((400, 400), Image.Resampling.LANCZOS)
            
            try:
                pixels = list(img.get_flattened_data())
            except AttributeError:
                pixels = list(img.getdata())
            
            total = len(pixels)
            if total == 0:
                return []
            
            # Sampling
            MAX_SAMPLES = 10000
            if total > MAX_SAMPLES:
                step = total // MAX_SAMPLES
                pixels = pixels[::step]
                total = len(pixels)
            
            r_sum = sum(p[0] for p in pixels) / total
            g_sum = sum(p[1] for p in pixels) / total
            b_sum = sum(p[2] for p in pixels) / total
            brightness = (r_sum + g_sum + b_sum) / 3
            
            tags = []
            
            # Dominan warna
            if r_sum > g_sum + 40 and r_sum > b_sum + 40:
                tags.append("Merah")
            elif g_sum > r_sum + 30 and g_sum > b_sum + 30:
                tags.append("Hijau")
            elif b_sum > r_sum + 40 and b_sum > g_sum + 30:
                tags.append("Biru")
            
            # Brightness
            if brightness < 50:
                tags.append("Gelap")
            elif brightness > 200:
                tags.append("Terang")
            
            # Grayscale
            max_c = max(r_sum, g_sum, b_sum)
            min_c = min(r_sum, g_sum, b_sum)
            if max_c - min_c < 20:
                if brightness > 180:
                    tags.append("Putih")
                elif brightness < 80:
                    tags.append("Hitam")
                else:
                    tags.append("Abu-abu")
            
            return tags
    except Exception:
        return []


# ═══════════════════════════════════════════════════════════
# FACE DETECTION (OPTIONAL)
# ═══════════════════════════════════════════════════════════

def detect_faces(image_path):
    """
    Deteksi jumlah wajah dalam gambar (via OpenCV).
    Return jumlah wajah, atau 0 kalau gagal/tidak aktif.
    """
    global _FACE_CASCADE
    
    if not CV2_AVAILABLE:
        return 0
    
    try:
        with _FACE_DETECTION_LOCK:
            if _FACE_CASCADE is None:
                cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
                _FACE_CASCADE = cv2.CascadeClassifier(cascade_path)
        
        img = cv2.imread(str(image_path))
        if img is None:
            return 0
        
        # Resize kalau terlalu besar
        if max(img.shape[:2]) > 1200:
            scale = 1200 / max(img.shape[:2])
            img = cv2.resize(img, None, fx=scale, fy=scale)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        
        faces = _FACE_CASCADE.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )
        return len(faces) if faces is not None else 0
    except Exception:
        return 0


# ═══════════════════════════════════════════════════════════
# OCR (OPTIONAL)
# ═══════════════════════════════════════════════════════════

_OCR_STOP_WORDS = {
    "the", "and", "for", "with", "from", "this", "that", "have", "has",
    "are", "was", "were", "will", "would", "could", "should", "can",
    "you", "your", "our", "their", "his", "her", "its",
    "but", "not", "all", "any", "some", "each", "every",
    "dan", "atau", "untuk", "dengan", "dari", "yang", "ini", "itu",
    "ada", "akan", "sudah", "telah", "juga", "saja", "hanya",
    "http", "https", "www", "com", "net", "org",
}


def extract_text_from_image(image_path, max_words=3, lang="ind+eng"):
    """
    Extract teks dari gambar via Tesseract OCR.
    Return list kata unik.
    """
    if not TESSERACT_AVAILABLE or not PILLOW_AVAILABLE:
        return []
    
    try:
        with Image.open(image_path) as img:
            if getattr(img, "is_animated", False):
                img.seek(0)
            img = img.convert("RGB")
            
            # Resize kalau kecil
            if max(img.size) < 800:
                scale = max(2, 1200 // max(img.size))
                img = img.resize(
                    (img.width * scale, img.height * scale),
                    Image.LANCZOS,
                )
            
            text = pytesseract.image_to_string(
                img, lang=lang, config="--psm 3"
            )
        
        words = re.findall(r"[A-Za-z]{3,}", text)
        seen = set()
        result = []
        
        for w in words:
            wl = w.lower()
            if wl in _OCR_STOP_WORDS or wl in seen:
                continue
            if wl.isdigit():
                continue
            seen.add(wl)
            result.append(w.capitalize())
            if len(result) >= max_words:
                break
        
        return result
    except Exception:
        return []


# ═══════════════════════════════════════════════════════════
# AUTO TAG
# ═══════════════════════════════════════════════════════════

_STOP_WORDS = {
    "img", "vid", "video", "photo", "pic", "picture", "image", "images",
    "dsc", "dscf", "dscn", "screenshot", "screen", "shot", "capture",
    "transformed", "upscale", "upscaled", "wallpaper", "background",
    "hd", "fhd", "uhd", "4k", "1080", "general", "copy", "final",
    "edit", "edited", "output", "result", "download", "downloaded",
    "saved", "new", "old", "temp", "tmp", "untitled", "unnamed",
    "file", "files", "doc", "document", "wa", "whatsapp", "fb",
    "facebook", "ig", "instagram", "tw", "twitter", "tiktok", "yt",
    "youtube", "telegram", "line", "snapchat", "official", "verified",
    "story", "reels", "shorts", "post", "app", "camera", "pix",
    "pixel", "snapseed", "lightroom", "photoshop", "canva", "picsart",
    "remastered", "remaster", "heic", "jpeg", "jpg", "png", "webp",
    "and", "the", "for", "with", "from", "into", "onto", "over", "under",
    "this", "that", "these", "those", "here", "there", "when", "where",
    "what", "which", "who", "why", "how", "also", "just", "only", "very",
    "more", "most", "less", "least", "many", "much", "some", "any",
    "all", "each", "every", "both", "either", "neither", "none",
    "yang", "dan", "atau", "untuk", "dengan", "dari", "ke", "di", "pada",
    "adalah", "akan", "sudah", "telah", "sedang", "masih", "belum",
    "ini", "itu", "sini", "sana", "mana", "kapan", "siapa", "apa",
    "juga", "saja", "hanya", "sangat", "lebih", "paling", "kurang",
    "banyak", "sedikit", "semua", "setiap", "beberapa", "para",
    "format", "size", "version", "beta", "alpha", "stable", "preview",
    "thumbnail", "thumb", "sample", "test", "demo", "audio", "media",
    "content", "red", "green", "blue", "yellow", "black", "white",
    "pink", "purple", "orange", "brown", "gray", "grey", "px", "mp",
    "kb", "mb", "gb", "tb", "usb", "hdr", "gps", "iso", "raw", "exif",
    "mp4", "mov", "mkv",
}

_BRAND_CASE = {
    "iphone": "iPhone", "ipad": "iPad", "ipod": "iPod",
    "gopro": "GoPro", "dji": "DJI", "sony": "Sony",
    "canon": "Canon", "nikon": "Nikon", "fujifilm": "Fujifilm",
    "panasonic": "Panasonic", "olympus": "Olympus", "leica": "Leica",
    "samsung": "Samsung", "xiaomi": "Xiaomi", "oppo": "OPPO",
    "vivo": "vivo", "realme": "realme", "huawei": "Huawei",
    "oneplus": "OnePlus", "google": "Google", "pixel": "Pixel",
    "adobe": "Adobe", "lightroom": "Lightroom",
    "android": "Android", "ios": "iOS",
}


def _clean_token(tok):
    """Bersihkan token (buang yang tidak berguna)."""
    if not tok:
        return None
    
    t = tok.strip()
    
    if len(t) < 3:
        return None
    if t.isdigit():
        return None
    if re.match(r"^[a-f0-9]{8,}$", t, re.IGNORECASE):
        return None
    if re.match(r"^[a-z]{1,3}\d{4,}$", t, re.IGNORECASE):
        return None
    if re.match(r"^(19|20)\d{6,}$", t):
        return None
    if re.match(r"^[a-f0-9]{4}-[a-f0-9]{4}", t, re.IGNORECASE):
        return None
    if t.lower() in _STOP_WORDS:
        return None
    return t


def _normalize_case(tok):
    """Normalisasi case untuk tag."""
    low = tok.lower()
    if low in _BRAND_CASE:
        return _BRAND_CASE[low]
    if tok.isupper() and len(tok) <= 5:
        return tok
    if len(tok) > 1:
        return tok[0].upper() + tok[1:].lower()
    return tok.upper()


def extract_auto_tags(
    file_path,
    category="",
    exif_meta=None,
    media_type="image",
    enable_face_detect=False,
    enable_color_tag=True,
    enable_ocr=False,
    ocr_max_words=3,
):
    """
    Extract tag otomatis dari berbagai sumber.
    
    Args:
        file_path: Path file
        category: Nama folder kategori
        exif_meta: dict hasil extract_detailed_exif
        media_type: "image" atau "video"
        enable_face_detect: aktifkan face detection
        enable_color_tag: aktifkan color tag
        enable_ocr: aktifkan OCR
        ocr_max_words: max kata dari OCR
    
    Returns:
        list tag (max 10)
    """
    file_path = Path(file_path)
    collected = []
    seen_lower = set()
    
    def add(tag, priority=5):
        if not tag:
            return
        t = str(tag).strip()
        if not t or len(t) < 2:
            return
        low = t.lower()
        if low in seen_lower or low in _STOP_WORDS:
            return
        seen_lower.add(low)
        collected.append((priority, t))
    
    # 1. Kategori dari folder
    cat_clean = (category or "").strip()
    if cat_clean and cat_clean.lower() not in ("general", ".", ""):
        for part in re.split(r"[\s_\-]+", cat_clean):
            c = _clean_token(part)
            if c:
                add(_normalize_case(c), priority=2)
    
    # 2. Tanggal dari nama file
    date_info = extract_date_from_filename(file_path.name)
    if date_info:
        add(date_info["month_display"], priority=2)
        add(str(date_info["year"]), priority=3)
    
    # 3. EXIF
    if exif_meta:
        make = exif_meta.get("camera_make")
        model = exif_meta.get("camera_model")
        
        if make:
            m = _clean_token(make.split()[0] if make.split() else make)
            if m:
                add(_normalize_case(m), priority=1)
        
        if model:
            for part in re.split(r"[\s_\-]+", model):
                p = _clean_token(part)
                if p and (not make or p.lower() not in make.lower()):
                    add(_normalize_case(p), priority=1)
                    break
        
        dims = exif_meta.get("dimensions")
        if dims and isinstance(dims, (tuple, list)):
            w, h = dims
            if w > h:
                add("Landscape", priority=4)
            elif h > w:
                add("Portrait", priority=4)
            elif w == h and w > 0:
                add("Square", priority=4)
        
        if exif_meta.get("geo"):
            add("Geotagged", priority=3)
    
    # 4. Face detect (opsional)
    if media_type == "image" and enable_face_detect and CV2_AVAILABLE:
        try:
            fc = detect_faces(file_path)
            if fc >= 1:
                add("Wajah", priority=3)
                add("Orang", priority=3)
            if fc >= 2:
                add("Grup", priority=3)
        except Exception:
            pass
    
    # 5. Color detect
    if media_type == "image" and enable_color_tag:
        try:
            for ot in detect_dominant_colors(file_path):
                add(ot, priority=6)
        except Exception:
            pass
    
    # 6. OCR (opsional)
    if media_type == "image" and enable_ocr and TESSERACT_AVAILABLE:
        try:
            for w in extract_text_from_image(file_path, max_words=ocr_max_words):
                add(w, priority=7)
        except Exception:
            pass
    
    # 7. Dari nama file (fallback)
    raw_name = file_path.stem
    cleaned = re.sub(
        r"(IMG|VID|WA|FB_IMG|Screenshot|Screen_Shot|PXL|DSC|DSCF|DSCN|GOPR|lv_\d+)[_\-\s]*",
        " ",
        raw_name,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"\b(19|20)\d{6,}\b", " ", cleaned)
    cleaned = re.sub(r"\b\d{4}[-_]\d{2}[-_]\d{2}\b", " ", cleaned)
    cleaned = re.sub(r"\b\d{2}[-_]\d{2}[-_]\d{4}\b", " ", cleaned)
    cleaned = re.sub(r"[_\-–—\.\(\)\[\]\{\}\+\#\@\&\|/,;:]+", " ", cleaned)
    
    for t in re.findall(r"[A-Za-z][A-Za-z0-9]+", cleaned):
        c = _clean_token(t)
        if c:
            add(_normalize_case(c), priority=5)
    
    # Sort by priority, limit 10
    collected.sort(key=lambda x: (x[0], x[1].lower()))
    return [tag for _, tag in collected[:10]]


# ═══════════════════════════════════════════════════════════
# MEDIA TYPE DETECTION
# ═══════════════════════════════════════════════════════════

def get_media_type(file_path):
    """Return 'image' atau 'video'."""
    ext = Path(file_path).suffix.lower()
    if ext in SUPPORTED_VIDEO_EXT:
        return "video"
    return "image"


def is_supported_file(file_path):
    """Cek apakah file didukung."""
    ext = Path(file_path).suffix.lower()
    return ext in SUPPORTED_EXTENSIONS


def get_video_mime(ext):
    """Return MIME type untuk video."""
    ext_upper = ext.upper().lstrip(".")
    return VIDEO_MIME.get(ext_upper, "video/mp4")


# ═══════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════

__all__ = [
    # Constants
    "SUPPORTED_EXTENSIONS", "SUPPORTED_IMAGE_EXT", "SUPPORTED_VIDEO_EXT",
    "VIDEO_EXTS", "VIDEO_MIME",
    "PILLOW_AVAILABLE", "TESSERACT_AVAILABLE", "CV2_AVAILABLE",
    "FFMPEG_PATH",
    "THUMBNAIL_DIR", "THUMB_MAX_SIZE", "THUMB_QUALITY",
    "MONTH_NAMES_ID",
    # Date
    "extract_date_from_filename",
    # EXIF
    "extract_detailed_exif",
    # Thumbnail
    "generate_image_thumbnail", "generate_video_thumbnail",
    "cleanup_old_thumbnails",
    # Color
    "detect_dominant_colors",
    # Face / OCR
    "detect_faces", "extract_text_from_image",
    # Auto tag
    "extract_auto_tags",
    # Helpers
    "get_media_type", "is_supported_file", "get_video_mime",
]