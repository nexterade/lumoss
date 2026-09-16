"""
amuv7 — Uploader (v7.1.0 LUMINOUS MOSS)
Mesin upload ke Catbox.moe dengan cursor-positioning & Luminous Moss aesthetic.
"""

import os
import sys
import time
import threading
import shutil
from pathlib import Path

import requests

from ui_helpers import (
    C_RESET, C_BOLD, C_GREEN, C_YELLOW, C_RED, C_WHITE,
    C_MOSS_1, C_MOSS_2, C_MOSS_3, C_SILVER, C_SILVER_LIGHT,
    format_bytes, short_label,
)

# ── Optional: requests-toolbelt untuk streaming progress ──
try:
    from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
    TOOLBELT_AVAILABLE = True
except ImportError:
    TOOLBELT_AVAILABLE = False


# ═══════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════

CATBOX_API = "https://catbox.moe/user/api.php"
CATBOX_MAX_FILE_SIZE = 200 * 1024 * 1024  # 200 MB

# Session stats (di-update thread-safe)
_STATS_LOCK = threading.Lock()
_STDOUT_LOCK = threading.Lock()

SESSION_STATS = {
    "total_scanned": 0,
    "success_uploads": 0,
    "failed_uploads": 0,
    "cached_count": 0,
    "total_bytes_sent": 0,
    "item_counter": 0,
    "start_time": 0,
    "end_time": 0,
}


# ═══════════════════════════════════════════════════════════
# STATS HELPERS
# ═══════════════════════════════════════════════════════════

def stats_reset():
    """Reset semua statistik session."""
    with _STATS_LOCK:
        SESSION_STATS["total_scanned"] = 0
        SESSION_STATS["success_uploads"] = 0
        SESSION_STATS["failed_uploads"] = 0
        SESSION_STATS["cached_count"] = 0
        SESSION_STATS["total_bytes_sent"] = 0
        SESSION_STATS["item_counter"] = 0
        SESSION_STATS["start_time"] = 0
        SESSION_STATS["end_time"] = 0


def stats_inc(key, amount=1):
    """Tambah counter."""
    with _STATS_LOCK:
        SESSION_STATS[key] = SESSION_STATS.get(key, 0) + amount


def stats_next_counter():
    """Ambil counter item berikutnya (auto increment)."""
    with _STATS_LOCK:
        SESSION_STATS["item_counter"] += 1
        return SESSION_STATS["item_counter"]


def stats_snapshot():
    """Ambil snapshot stats (thread-safe)."""
    with _STATS_LOCK:
        return dict(SESSION_STATS)


# ═══════════════════════════════════════════════════════════
# PROGRESS PRINTER
# ═══════════════════════════════════════════════════════════

class ProgressPrinter:
    """Progress bar sederhana yang update tiap 0.25 detik."""
    
    RENDER_INTERVAL = 0.25
    BAR_WIDTH = 10
    
    def __init__(self, total_size, label, current_idx, total_idx):
        self.total_size = max(1, total_size)
        self.label = label
        self.current_idx = current_idx
        self.total_idx = total_idx
        self._uploaded = 0
        self.start_time = time.time()
        self._last_len = 0
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
    
    def _loop(self):
        while not self._stop.is_set():
            with self._lock:
                self._render()
            time.sleep(self.RENDER_INTERVAL)
    
    def update(self, n):
        with self._lock:
            self._uploaded = n
    
    def _build_line(self):
        elapsed = max(0.001, time.time() - self.start_time)
        speed = self._uploaded / elapsed
        pct = int((self._uploaded / self.total_size) * 100)
        pct = max(0, min(100, pct))
        
        bar_w = self.BAR_WIDTH
        filled = int(bar_w * pct / 100)
        
        if pct >= 100:
            bar_colored = f"{C_MOSS_1}{'▰' * bar_w}{C_RESET}"
        else:
            bar_colored = (
                f"{C_MOSS_1}{'▰' * filled}"
                f"{C_SILVER}{'▱' * (bar_w - filled)}{C_RESET}"
            )
        
        speed_str = f"{format_bytes(speed)}/s"
        pct_str = f"{pct:3d}%"
        idx_str = f"[{self.current_idx}/{self.total_idx}]"
        
        # Batasi label berdasarkan lebar terminal
        term_w = shutil.get_terminal_size(fallback=(60, 20)).columns
        fixed_visible = len(idx_str) + 1 + bar_w + 1 + len(pct_str) + 1 + len(speed_str) + 1
        label_budget = term_w - fixed_visible - 2
        
        label = self.label
        if label_budget < 6:
            label = ""
        elif len(label) > label_budget:
            label = label[:max(1, label_budget - 1)] + "…"
        
        parts = [
            f"{C_MOSS_2}{idx_str}{C_RESET}",
            bar_colored,
            f"{C_BOLD}{C_WHITE}{pct_str}{C_RESET}",
            f"{C_MOSS_3}{speed_str}{C_RESET}",
        ]
        if label:
            parts.append(f"{C_SILVER}{label}{C_RESET}")
        
        msg = " ".join(parts)
        visible = fixed_visible + (len(label) if label else 0) - 1
        return msg, visible
    
    def _render(self):
        with _STDOUT_LOCK:
            msg, visible = self._build_line()
            pad = ""
            if visible < self._last_len:
                pad = " " * (self._last_len - visible)
            self._last_len = max(visible, self._last_len)
            sys.stdout.write("\r\033[2K" + msg + pad)
            sys.stdout.flush()
    
    def finish(self):
        with self._lock:
            self._uploaded = self.total_size
            self._render()
    
    def stop(self):
        self._stop.set()
        try:
            self._thread.join(timeout=0.5)
        except Exception:
            pass
        with _STDOUT_LOCK:
            sys.stdout.write("\r\033[2K")
            sys.stdout.flush()
        self._last_len = 0


# ═══════════════════════════════════════════════════════════
# UPLOAD CORE
# ═══════════════════════════════════════════════════════════

def _upload_streaming(file_path, data_fields, printer):
    """Upload dengan streaming (progress bar real-time)."""
    filename = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    file_obj = open(file_path, "rb")
    file_obj.seek(0, os.SEEK_SET)
    
    fields = dict(data_fields)
    fields["fileToUpload"] = (filename, file_obj, "application/octet-stream")
    
    try:
        encoder = MultipartEncoder(fields=fields)
        
        def _on_progress(monitor):
            printer.update(monitor.bytes_read)
        
        monitor = MultipartEncoderMonitor(encoder, _on_progress)
        res = requests.post(
            CATBOX_API,
            data=monitor,
            headers={
                "Content-Type": monitor.content_type,
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            },
            timeout=600,
        )
        res.raise_for_status()
        
        result = res.text.strip()
        
        if not result or not result.startswith("http"):
            raise RuntimeError(f"Catbox response tidak valid: {result[:100]}")
        
        if hasattr(monitor, "bytes_read") and monitor.bytes_read < file_size:
            raise RuntimeError(
                f"Upload tidak lengkap: {monitor.bytes_read}/{file_size} bytes"
            )
        
        return result
    finally:
        try:
            file_obj.close()
        except Exception:
            pass


def _upload_simple(file_path, data_fields):
    """Upload tanpa progress bar (fallback)."""
    filename = os.path.basename(file_path)
    
    with open(file_path, "rb") as f:
        f.seek(0, os.SEEK_SET)
        files = {"fileToUpload": (filename, f, "application/octet-stream")}
        res = requests.post(
            CATBOX_API,
            data=data_fields,
            files=files,
            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"},
            timeout=600,
        )
        res.raise_for_status()
        result = res.text.strip()
        
        if not result or not result.startswith("http"):
            raise RuntimeError(f"Catbox response tidak valid: {result[:100]}")
        return result


def _do_catbox_request(file_path, data_fields, printer):
    """Pilih upload method berdasarkan ketersediaan toolbelt."""
    if TOOLBELT_AVAILABLE:
        return _upload_streaming(file_path, data_fields, printer)
    else:
        result = _upload_simple(file_path, data_fields)
        printer.update(os.path.getsize(file_path))
        return result


# ═══════════════════════════════════════════════════════════
# PUBLIC API — UPLOAD
# ═══════════════════════════════════════════════════════════

def upload_to_catbox(
    file_path,
    userhash="",
    label=None,
    is_thumb=False,
    max_retry=3,
    batch_pause_every=30,
    batch_pause_seconds=60,
    delay_between_files=2,
):
    """Upload file ke Catbox dengan retry & rate limit handling."""
    file_path = Path(file_path)
    file_size = os.path.getsize(file_path)
    
    if not is_thumb and file_size > CATBOX_MAX_FILE_SIZE:
        raise RuntimeError(
            f"File melebihi batas Catbox "
            f"({format_bytes(file_size)} > {format_bytes(CATBOX_MAX_FILE_SIZE)})"
        )
    
    raw_label = label or file_path.name
    label_display = short_label(raw_label, 40)
    
    if not is_thumb:
        idx = stats_next_counter()
    else:
        idx = stats_snapshot().get("item_counter", 0)
    
    total = stats_snapshot()["total_scanned"]
    ext = file_path.suffix.lower().lstrip(".")
    
    # Icon & tipe
    if is_thumb:
        icon = "🖼️"
        kind_txt = f"{C_YELLOW}THUMB{C_RESET}"
    elif ext in {"mp4", "mkv", "webm", "mov"}:
        icon = "🎬"
        kind_txt = f"{C_MOSS_1}VIDEO{C_RESET}"
    else:
        icon = "📷"
        kind_txt = f"{C_MOSS_3}IMAGE{C_RESET}"
    
    with _STDOUT_LOCK:
        sys.stdout.write(
            f"  {icon}\033[7G{C_MOSS_2}{C_BOLD}[{idx}/{total}]{C_RESET}"
            f"\033[16G{kind_txt}"
            f"\033[24G{C_WHITE}{label_display}{C_RESET}  "
            f"{C_SILVER}⤷  {format_bytes(file_size)}{C_RESET}\n"
        )
        sys.stdout.flush()
    
    data_fields = {"reqtype": "fileupload"}
    if userhash:
        data_fields["userhash"] = userhash
    
    upload_start = time.time()
    result_url = None
    last_error = None
    printer = None
    
    # Retry loop
    for attempt in range(max_retry):
        printer = ProgressPrinter(
            total_size=file_size,
            label=label_display,
            current_idx=idx,
            total_idx=total,
        )
        
        try:
            try:
                result_url = _do_catbox_request(file_path, data_fields, printer)
                break  # Sukses
            except requests.HTTPError as he:
                status = getattr(he.response, "status_code", None)
                
                # Rate limit → tunggu & retry
                if status == 429:
                    printer.stop()
                    wait_time = (attempt + 1) * 15
                    with _STDOUT_LOCK:
                        sys.stdout.write(
                            f"  {C_SILVER}╰─{C_RESET} {C_YELLOW}⏳\033[10GRate limit, "
                            f"tunggu {wait_time}s... "
                            f"(attempt {attempt + 1}/{max_retry}){C_RESET}\n"
                        )
                        sys.stdout.flush()
                    time.sleep(wait_time)
                    last_error = he
                    continue
                
                # Userhash invalid → fallback anonymous
                elif status in (401, 403, 412) and "userhash" in data_fields:
                    printer.stop()
                    with _STDOUT_LOCK:
                        sys.stdout.write(
                            f"  {C_SILVER}╰─{C_RESET} {C_YELLOW}⚠️\033[10GUserhash invalid, "
                            f"coba anonymous...{C_RESET}\n"
                        )
                        sys.stdout.flush()
                    
                    printer2 = ProgressPrinter(
                        total_size=file_size,
                        label=label_display,
                        current_idx=idx,
                        total_idx=total,
                    )
                    try:
                        result_url = _do_catbox_request(
                            file_path, {"reqtype": "fileupload"}, printer2
                        )
                        printer2.finish()
                        time.sleep(0.15)
                        printer2.stop()
                        printer = printer2
                        break
                    except Exception as e2:
                        printer2.stop()
                        last_error = e2
                        continue
                else:
                    printer.stop()
                    last_error = he
                    raise
            
            except requests.RequestException as re:
                # Timeout / connection error → retry
                printer.stop()
                last_error = re
                
                if attempt < max_retry - 1:
                    wait_time = (attempt + 1) * 5
                    with _STDOUT_LOCK:
                        sys.stdout.write(
                            f"  {C_SILVER}╰─{C_RESET} {C_YELLOW}⚠️\033[10G"
                            f"{type(re).__name__}, retry dalam {wait_time}s... "
                            f"({attempt + 1}/{max_retry}){C_RESET}\n"
                        )
                        sys.stdout.flush()
                    time.sleep(wait_time)
                    continue
                else:
                    raise
        
        except Exception as e:
            printer.stop()
            last_error = e
            if attempt < max_retry - 1:
                continue
            else:
                raise
    
    if result_url is None:
        raise last_error or RuntimeError("Upload gagal setelah retry")
    
    elapsed = max(0.001, time.time() - upload_start)
    avg_speed = file_size / elapsed
    
    # Stop progress bar
    try:
        printer.finish()
        time.sleep(0.1)
        printer.stop()
    except Exception:
        pass
    
    finish_time_str = time.strftime("%H:%M:%S", time.localtime())
    
    with _STDOUT_LOCK:
        sys.stdout.write(
            f"  {C_SILVER}╰─{C_RESET} {C_GREEN}✅{C_RESET}\033[10G"
            f"{C_WHITE}{format_bytes(file_size)}{C_RESET}  "
            f"{C_SILVER}dalam{C_RESET} {C_MOSS_2}{elapsed:.1f}s{C_RESET}  "
            f"{C_SILVER}({C_MOSS_1}{format_bytes(avg_speed)}/s{C_SILVER}){C_RESET}  "
            f"{C_MOSS_3}✓ {finish_time_str}{C_RESET}\n"
        )
        sys.stdout.flush()
    
    stats_inc("total_bytes_sent", file_size)
    
    # Batch rate limiting (kecuali thumbnail)
    if not is_thumb:
        time.sleep(delay_between_files)
        
        current_count = stats_snapshot().get("item_counter", 0)
        if current_count > 0 and current_count % batch_pause_every == 0:
            _batch_pause(batch_pause_seconds)
    
    return result_url


def _batch_pause(pause_seconds):
    """Pause dengan hitungan mundur (hemat rate limit)."""
    with _STDOUT_LOCK:
        sys.stdout.write(
            f"\n  {C_YELLOW}⏸️\033[7GBatch selesai. Istirahat dulu biar aman!{C_RESET}\n"
        )
        sys.stdout.flush()
    
    for remaining in range(pause_seconds, 0, -1):
        if remaining >= 60:
            mins = remaining // 60
            secs = remaining % 60
            time_display = f"{mins}:{secs:02d}"
        else:
            time_display = f"{remaining} detik"
        
        bar_len = 20
        filled = int(bar_len * (pause_seconds - remaining) / pause_seconds)
        bar = f"{C_MOSS_1}{'█' * filled}{C_SILVER}{'░' * (bar_len - filled)}{C_RESET}"
        
        with _STDOUT_LOCK:
            sys.stdout.write(
                f"\r  {C_MOSS_3}⏳{C_RESET}\033[6GLanjut dalam "
                f"{C_MOSS_2}{time_display:>10}{C_RESET}  {bar}  "
            )
            sys.stdout.flush()
        
        time.sleep(1)
    
    with _STDOUT_LOCK:
        sys.stdout.write("\r" + " " * 80 + "\r")
        sys.stdout.write(f"  {C_GREEN}▶️\033[7GGas! Lanjut upload...{C_RESET}\n\n")
        sys.stdout.flush()


# ═══════════════════════════════════════════════════════════
# PUBLIC API — VERIFY
# ═══════════════════════════════════════════════════════════

def verify_uploaded_file(url, original_size, tolerance=0.05):
    """Verifikasi file yang di-upload punya ukuran wajar."""
    try:
        r = requests.head(url, timeout=10, allow_redirects=True)
        remote_size = int(r.headers.get("Content-Length", 0))
        
        if remote_size == 0:
            return True, "size unknown"
        
        ratio = remote_size / original_size
        if ratio < (1 - tolerance):
            return False, f"file dikompres: {original_size} → {remote_size} bytes ({ratio * 100:.0f}%)"
        
        return True, "OK"
    except Exception as e:
        return True, f"verify gagal: {e}"


def check_url_active(url, timeout=15, retry=2):
    """Cek URL aktif."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
        ),
    }
    
    for attempt in range(retry + 1):
        try:
            r = requests.head(url, headers=headers, timeout=timeout, allow_redirects=True)
            if r.status_code in (200, 206):
                return True
            if r.status_code in (404, 410):
                return False
            
            r = requests.get(url, headers=headers, timeout=timeout,
                             stream=True, allow_redirects=True)
            try:
                if r.status_code in (200, 206):
                    return True
                if r.status_code in (404, 410):
                    return False
            finally:
                r.close()
            return None
        except requests.Timeout:
            if attempt < retry:
                time.sleep(2 ** attempt)
                continue
            return None
        except requests.RequestException:
            return None
    
    return None


# ═══════════════════════════════════════════════════════════
# SUMMARY REPORT (v7.1.0 — LUMINOUS MOSS)
# ═══════════════════════════════════════════════════════════

def print_summary_report():
    """Cetak laporan akhir upload dengan cursor-positioning."""
    s = stats_snapshot()
    
    # Hitung durasi
    start = s.get("start_time", 0) or 0
    end = s.get("end_time", 0) or 0
    if start > 0 and end > start:
        duration = int(end - start)
    else:
        duration = 0
    
    mins, secs = divmod(duration, 60)
    if mins > 0:
        dur_str = f"{mins}m {secs}s"
    else:
        dur_str = f"{secs}s"
    
    # Hitung kecepatan
    if duration > 0 and s["total_bytes_sent"] > 0:
        speed_bps = s["total_bytes_sent"] / duration
    else:
        speed_bps = 0
    
    # Format bytes
    total_kb = s["total_bytes_sent"] / 1024
    if total_kb < 1024:
        kuota_str = f"{total_kb:.1f} kB"
    elif total_kb < 1024 * 1024:
        kuota_str = f"{total_kb / 1024:.2f} MB"
    else:
        kuota_str = f"{total_kb / (1024 * 1024):.2f} GB"
    
    if speed_bps < 1024:
        speed_str = f"{speed_bps:.1f} B/s"
    elif speed_bps < 1024 * 1024:
        speed_str = f"{speed_bps / 1024:.1f} kB/s"
    else:
        speed_str = f"{speed_bps / (1024 * 1024):.2f} MB/s"
    
    # Waktu
    start_str = time.strftime("%H:%M:%S", time.localtime(start)) if start > 0 else "—"
    end_str = time.strftime("%H:%M:%S", time.localtime(end)) if end > 0 else "—"
    
    # ═══════════════════════════════════════════════════════════
    # TAMPILAN LAPORAN (Cursor-positioned)
    # ═══════════════════════════════════════════════════════════
    print()
    print(f"{C_MOSS_1}━━━ ✅\033[8GATOS BERES BOSS! ━━━{C_RESET}")
    print()
    print(f"  {C_MOSS_3}📂\033[6GTotal File Terdeteksi\033[30G{C_SILVER}›{C_RESET}  {C_WHITE}{s['total_scanned']} file{C_RESET}")
    print(f"  {C_SILVER}⚡\033[6GMenggunakan Cache\033[30G{C_SILVER}›{C_RESET}  {C_SILVER}{s['cached_count']} file (skip){C_RESET}")
    print(f"  {C_GREEN}✅\033[6GBerhasil Diupload\033[30G{C_SILVER}›{C_RESET}  {C_GREEN}{s['success_uploads']} file{C_RESET}")
    
    if s['failed_uploads'] > 0:
        print(f"  {C_RED}❌\033[6GGagal Diupload\033[30G{C_SILVER}›{C_RESET}  {C_RED}{s['failed_uploads']} file{C_RESET}")
    else:
        print(f"  {C_SILVER}❌\033[6GGagal Diupload\033[30G{C_SILVER}›{C_RESET}  {C_SILVER}{s['failed_uploads']} file{C_RESET}")
    
    print()
    print(f"  {C_SILVER}{'─' * 38}{C_RESET}")
    print()
    print(f"  {C_MOSS_3}🕐\033[6GMulai\033[30G{C_SILVER}›{C_RESET}  {C_WHITE}{start_str}{C_RESET}")
    print(f"  {C_MOSS_3}🕐\033[6GSelesai\033[30G{C_SILVER}›{C_RESET}  {C_WHITE}{end_str}{C_RESET}")
    print(f"  {C_MOSS_2}⏱️\033[6GDurasi\033[30G{C_SILVER}›{C_RESET}  {C_MOSS_2}{dur_str}{C_RESET}")
    print()
    print(f"  {C_SILVER}{'─' * 38}{C_RESET}")
    print()
    print(f"  {C_MOSS_1}🌐\033[6GKuota Internet Dipakai\033[30G{C_SILVER}›{C_RESET}  {C_MOSS_1}{C_BOLD}{kuota_str}{C_RESET}")
    print(f"  {C_MOSS_2}🚀\033[6GRata-rata Kecepatan\033[30G{C_SILVER}›{C_RESET}  {C_MOSS_2}{speed_str}{C_RESET}")
    print()
    print(f"  {C_SILVER}╰─ 💡 Total = upload utama + thumbnail{C_RESET}")
    print()


# ═══════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════

__all__ = [
    "CATBOX_API", "CATBOX_MAX_FILE_SIZE",
    "TOOLBELT_AVAILABLE",
    "SESSION_STATS",
    "stats_reset", "stats_inc", "stats_next_counter", "stats_snapshot",
    "ProgressPrinter",
    "upload_to_catbox",
    "verify_uploaded_file", "check_url_active",
    "print_summary_report",
]