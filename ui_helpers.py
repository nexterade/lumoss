"""
lumoss — UI Helpers (v7.2.6 MEDIA GARDEN)
Kumpulan utility tampilan terminal:
- ANSI colors (palette hijau neon + silver dark)
- Banner ASCII art "LUMOSS" (auto-width, ASCII-only)
- Input prompt dengan default
- Box renderer (full-width, 2 kolom, merged, vertical)
- Layout helpers (auto-resize dari lebar terminal)
- Emoji converter (auto-convert emoji → Unicode symbol)

Changelog v7.2.6:
- NEW: EMOJI_TO_UNICODE — mapping emoji → Unicode symbol (1-cell)
- NEW: convert_emoji() — auto-convert emoji, KECUALI 🌿 (simbol Lumoss)
- NEW: strip_emoji() — strip sisa emoji yang gak ada di mapping
- KEEP: 🌿 sebagai simbol utama Lumoss (gak di-convert)
- UPDATE: PROJECT_VERSION → 7.2.6

Changelog v7.2.5:
- NEW: render_vertical_box() — 1 box, section vertikal (stack atas-bawah)
- NEW: render_vertical_group() — 1 box, grup menu vertikal

Changelog v7.2.4:
- NEW: render_merged_box() — 1 box, multiple section (divider tengah)
- NEW: render_merged_group() — 1 box, multiple grup menu

Changelog v7.2.3:
- FIX: Banner LUMOSS — border ngikutin lebar ASCII art (bukan hardcoded 41)
- FIX: Emoji 🌿 di tagline diganti '*' biar lebar visual stabil
- NEW: layout_widths() — hitung lebar box otomatis dari term_width()
- NEW: render_full_box() — 1 box full-width
- NEW: render_two_col_box() — 2 kolom dalam 1 border utuh (no tabrakan)
- NEW: render_group_box() — grup menu border utuh
- NEW: render_group_box_two_col() — grup menu 2 kolom 1 border
- KEEP: semua helper lama (backward-compat)

Changelog v7.2.2:
- REBRANDING: amuv7 → lumoss
- PROJECT_NAME: "lumoss"
- PROJECT_FULL: "Lumoss — Media Garden"
- Banner: LUMOSS (bukan NEXTER)
- Tagline: "Media Garden, in bloom"
- Fix: vwidth() & vpad() buat alignment emoji presisi
"""

import os
import re
import shutil


# ═══════════════════════════════════════════════════════════
# ANSI COLOR CODES
# ═══════════════════════════════════════════════════════════

C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_DIM = "\033[2m"

C_BLACK = "\033[30m"
C_RED = "\033[91m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_BLUE = "\033[94m"
C_MAGENTA = "\033[95m"
C_CYAN = "\033[96m"
C_WHITE = "\033[97m"
C_GRAY = "\033[90m"
C_PURPLE = "\033[95m"
C_ORANGE = "\033[33m"

C_DIM_WHITE = "\033[2;37m"
C_DIM_CYAN = "\033[2;36m"
C_BRIGHT_MAGENTA = "\033[1;95m"
C_BRIGHT_CYAN = "\033[1;96m"
C_BRIGHT_YELLOW = "\033[1;93m"


# ═══════════════════════════════════════════════════════════
# LUMINOUS MOSS PALETTE
# Referensi: #2BEE34 (hijau neon) + #141414 (silver dark)
# ═══════════════════════════════════════════════════════════

C_MOSS_1 = "\033[38;5;46m"     # bright neon green (~#2BEE34)
C_MOSS_2 = "\033[38;5;82m"     # vivid green (mid)
C_MOSS_3 = "\033[38;5;118m"    # lighter green
C_MOSS_4 = "\033[38;5;155m"    # pale green
C_MOSS_DARK = "\033[38;5;22m"  # dark green (background hint)
C_SILVER = "\033[38;5;245m"    # silver gray
C_SILVER_LIGHT = "\033[38;5;250m"  # light silver

# Alias backward-compat
C_GRAD_1 = C_MOSS_1
C_GRAD_2 = C_MOSS_2
C_GRAD_3 = C_MOSS_3
C_GRAD_4 = C_MOSS_4
C_GRAD_5 = C_MOSS_3
C_GRAD_6 = C_MOSS_2
C_GRAD_7 = C_MOSS_1


# ═══════════════════════════════════════════════════════════
# PROJECT CONSTANTS (v7.2.6 — REBRANDING)
# ═══════════════════════════════════════════════════════════

PROJECT_NAME = "lumoss"
PROJECT_FULL = "Lumoss — Media Garden"
PROJECT_VERSION = "7.2.6"
PROJECT_AUTHOR = "@nexterade"
PROJECT_DESC = "Media Garden, in bloom"
PROJECT_TAGLINE = "Media Garden, in bloom"

# Simbol utama Lumoss — JANGAN di-convert
LUMOSS_SYMBOL = "🌿"

DIVIDER_CHAR = "─"
DIVIDER_WIDTH = 53
ARROW = "→"


# ═══════════════════════════════════════════════════════════
# VISUAL PADDING — presisi buat emoji & unicode
# ═══════════════════════════════════════════════════════════

try:
    from wcwidth import wcswidth as _wcswidth
except ImportError:
    def _wcswidth(s):
        return len(s)

_ZERO_WIDTH_MARKS = ("\uFE0E", "\uFE0F", "\u200D")


def _is_wide_emoji_range(cp: int) -> bool:
    """True kalau codepoint dirender 2 kolom penuh warna."""
    return (
        0x1F000 <= cp <= 0x1FFFF or
        0x2600 <= cp <= 0x27BF or
        0x2B00 <= cp <= 0x2BFF
    )


def vwidth(text: str) -> int:
    """Hitung lebar VISUAL teks di terminal Android/Termux."""
    total = 0
    for ch in text:
        if ch in _ZERO_WIDTH_MARKS:
            continue
        if _is_wide_emoji_range(ord(ch)):
            total += 2
            continue
        w = _wcswidth(ch)
        if w is None or w < 0:
            w = 1
        total += w
    return total


def vpad(text: str, width: int, align: str = "left") -> str:
    """Padding berdasarkan lebar VISUAL."""
    cur = vwidth(text)
    gap = max(0, width - cur)
    if align == "right":
        return " " * gap + text
    if align == "center":
        left = gap // 2
        return " " * left + text + " " * (gap - left)
    return text + " " * gap


# ═══════════════════════════════════════════════════════════
# EMOJI REGEX & STRIPPER (v7.2.6)
# ═══════════════════════════════════════════════════════════

# Regex: match emoji warna (≥ U+1F000) + variation selector + ZWJ
_EMOJI_WIDE_RE = re.compile(
    "["
    "\U0001F000-\U0001FAFF"  # emoji warna (blocks, faces, symbols)
    "\U0000FE00-\U0000FE0F"  # variation selectors
    "\U0000200D"             # ZWJ (zero-width joiner)
    "\U000020E3"             # combining enclosing keycap
    "]+",
    flags=re.UNICODE,
)

# Regex: match emoji + symbol dekoratif (buat strip total)
_EMOJI_ALL_RE = re.compile(
    "["
    "\U0001F000-\U0001FAFF"
    "\U00002600-\U000027BF"  # misc symbols + dingbats
    "\U00002B00-\U00002BFF"  # arrows, stars
    "\U0000FE00-\U0000FE0F"
    "\U0000200D"
    "\U000020E3"
    "\U00002190-\U000021FF"  # arrows
    "\U000025A0-\U000025FF"  # geometric shapes
    "]+",
    flags=re.UNICODE,
)


def strip_emoji(text: str, keep_symbols: bool = False) -> str:
    """Hapus emoji dari string — biar border box rapi.

    Args:
        text          : string yang mau di-clean
        keep_symbols  : kalo True, simpan Unicode symbol (◉ ▸ ◆ dll),
                        cuma buang emoji warna (💖 🚀 dll)

    Contoh:
        strip_emoji("Cantika 💖")  → "Cantika"
        strip_emoji("🚀 Upload")    → "Upload"
    """
    if not text:
        return text

    if keep_symbols:
        # Cuma buang emoji di range warna (≥ U+1F000) + variation selector
        result = _EMOJI_WIDE_RE.sub("", text)
    else:
        result = _EMOJI_ALL_RE.sub("", text)

    # Rapihin spasi double
    result = " ".join(result.split())
    return result


# ═══════════════════════════════════════════════════════════
# EMOJI → UNICODE CONVERTER (v7.2.6)
# ═══════════════════════════════════════════════════════════

# Mapping emoji → Unicode symbol (1-cell stabil)
# CATATAN: 🌿 (LUMOSS_SYMBOL) sengaja TIDAK ada di mapping
#          biar tetep jadi simbol Lumoss
EMOJI_TO_UNICODE = {
    # ── Hati / Love ──
    "❤": "♥", "❤️": "♥", "🧡": "♥", "💛": "♥", "💚": "♥", "💙": "♥",
    "💜": "♥", "🖤": "♥", "🤍": "♥", "🤎": "♥", "💖": "♥", "💗": "♥",
    "💓": "♥", "💕": "♥", "💞": "♥", "💘": "♥", "💝": "♥", "💟": "♡",
    "❣": "♥", "❣️": "♥", "💔": "♡",

    # ── Bintang / Star ──
    "⭐": "★", "🌟": "★", "✨": "✦", "💫": "✦", "🌠": "✦",
    "✩": "☆", "✪": "★",

    # ── Fire / Power ──
    "🔥": "✦", "💥": "✗", "⚡": "⚡", "💢": "✗",

    # ── Check / Cross ──
    "✅": "✓", "☑": "✓", "☑️": "✓", "✔": "✓", "✔️": "✓",
    "❌": "✗", "❎": "✗", "✖": "✗", "✖️": "✗", "⛔": "✗",

    # ── Warning / Info ──
    "⚠": "⚠", "⚠️": "⚠", "🚨": "!!", "❗": "!", "❕": "!",
    "❓": "?", "❔": "?", "💡": "✦", "ℹ": "ℹ", "ℹ️": "ℹ",

    # ── Arrow ──
    "⬆": "▲", "⬆️": "▲", "⬇": "▼", "⬇️": "▼",
    "⬅": "◀", "⬅️": "◀", "➡": "▶", "➡️": "▶",
    "↗": "↗", "↘": "↘", "↙": "↙", "↖": "↖",
    "🔄": "↻", "🔃": "↻", "🔁": "↻", "🔂": "↻",

    # ── Media / File ──
    "📄": "▪", "📃": "▪", "📑": "▪", "📋": "▪", "📌": "◆",
    "📍": "◆", "📎": "⚿", "🖇": "⚿", "🖇️": "⚿",
    "📁": "▸", "📂": "▣", "🗂": "▣", "🗂️": "▣", "🗃": "▣", "🗃️": "▣",
    "💾": "=", "💿": "◉", "📀": "◉", "🖥": "▣", "🖥️": "▣",
    "📱": "▣", "📷": "◉", "📸": "◉", "🎥": "▶", "🎬": "▶",
    "🎵": "♪", "🎶": "♪", "🎤": "♪", "🎧": "♪",

    # ── User / People ──
    "👤": "◉", "👥": "❖", "👨": "◉", "👩": "◉", "🧑": "◉",
    "👶": "◉", "👴": "◉", "👵": "◉", "🙋": "◉", "🙋‍♂️": "◉",
    "🙋‍♀️": "◉", "💁": "◉", "🤝": "❖",

    # ── Tools / Setting ──
    "⚙": "⚙", "⚙️": "⚙", "🔧": "⚒", "🔨": "⚒", "🛠": "⚒", "🛠️": "⚒",
    "🔩": "⚒", "⚒": "⚒", "⚒️": "⚒", "🔑": "⚿", "🗝": "⚿", "🗝️": "⚿",
    "🔒": "⚿", "🔓": "⚿", "🔐": "⚿", "🔏": "⚿",

    # ── Aksi / Target ──
    "🎯": "◆", "🎪": "◆", "🎨": "◈", "🖌": "✎", "🖌️": "✎",
    "✏": "✎", "✏️": "✎", "📝": "✎", "🖊": "✎", "🖊️": "✎",
    "🚀": "▶", "🛫": "▶", "✈": "▶", "✈️": "▶", "🛸": "◐",

    # ── Symbol / Status ──
    "💯": "★", "🆗": "✓", "🆕": "✦", "🆒": "★", "🆓": "✦",
    "🔴": "●", "🟠": "●", "🟡": "●", "🟢": "●", "🔵": "●",
    "🟣": "●", "⚫": "●", "⚪": "○", "🟤": "●",

    # ── Nature / Plant (KECUALI 🌿) ──
    "🍀": "❦", "🌱": "❦", "🌲": "❦", "🌳": "❦",
    "🌴": "❦", "🌵": "❦", "🌾": "❦", "🌷": "❦", "🌹": "❦",
    "🌸": "❦", "🌺": "❦", "🌻": "❦", "🌼": "❦", "💐": "❦",

    # ── Network / Web ──
    "🌐": "◐", "🌍": "◐", "🌎": "◐", "🌏": "◐", "🗺": "◐", "🗺️": "◐",

    # ── GitHub / Code ──
    "🐙": "⚑", "💻": "▣", "⌨": "▣", "⌨️": "▣", "🖱": "▣", "🖱️": "▣",

    # ── Party / Fun ──
    "🎉": "✦", "🎊": "✦", "🎈": "✦", "🎁": "✦", "🏆": "★",
    "🥇": "★", "🥈": "★", "🥉": "★", "🏅": "★", "🎖": "★", "🎖️": "★",

    # ── Other ──
    "🔔": "◆", "🔕": "◆", "💬": "▪", "💭": "▪", "🗯": "▪", "🗯️": "▪",
    "📢": "◆", "📣": "◆", "📡": "~", "🛰": "◐", "🛰️": "◐",
    "🎓": "◆", "📚": "❓", "📖": "?", "📕": "?", "📗": "?", "📘": "?",
    "📙": "?", "📓": "?", "📔": "?", "📒": "?",
    "🕐": "◷", "🕑": "◷", "🕒": "◷", "⏰": "◷", "⏱": "◷", "⏱️": "◷",
    "⏳": "◷", "⌛": "◷", "📅": "▤", "📆": "▤", "🗓": "▤", "🗓️": "▤",
}


def convert_emoji(text: str) -> str:
    """Auto-convert emoji ke Unicode symbol (1-cell stabil).

    User input emoji → output unicode symbol.
    KECUALI 🌿 (LUMOSS_SYMBOL) — tetap dipertahankan.
    Emoji yang gak ada di mapping → di-strip.

    Contoh:
        convert_emoji("Cantika 💖")    → "Cantika ♥"
        convert_emoji("🚀 Upload")      → "▶ Upload"
        convert_emoji("🌿 Lumoss")      → "🌿 Lumoss"  (KEEP!)
        convert_emoji("Hello 🦄")       → "Hello"  (🦄 gak ada di mapping)

    Args:
        text: string yang mau di-convert

    Returns:
        string dengan emoji → unicode symbol
    """
    if not text:
        return text

    # Simpan 🌿 dulu (replace dengan placeholder)
    placeholder = "\u0000LUMOSS_SYMBOL\u0000"
    result = text.replace(LUMOSS_SYMBOL, placeholder)

    # Convert emoji di mapping
    for emoji, symbol in EMOJI_TO_UNICODE.items():
        result = result.replace(emoji, symbol)

    # Sisa emoji yang gak ada di mapping — di-strip
    result = strip_emoji(result, keep_symbols=True)

    # Balikin 🌿
    result = result.replace(placeholder, LUMOSS_SYMBOL)

    # Rapihin spasi double
    result = " ".join(result.split())

    return result


# ═══════════════════════════════════════════════════════════
# TERMINAL UTILS
# ═══════════════════════════════════════════════════════════

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def term_width(fallback=60):
    try:
        return shutil.get_terminal_size(fallback=(fallback, 20)).columns
    except Exception:
        return fallback


def term_height(fallback=20):
    try:
        return shutil.get_terminal_size(fallback=(60, fallback)).lines
    except Exception:
        return fallback


# ═══════════════════════════════════════════════════════════
# LAYOUT HELPERS (v7.2.6 — full-width + 2 kolom + merged + vertical)
# ═══════════════════════════════════════════════════════════

def layout_widths(fallback=62):
    """Hitung lebar layout optimal dari lebar terminal.

    Return: (total, box_l, box_r, gap)
    """
    tw = term_width(fallback)
    total = max(58, tw - 6)
    gap = 1
    box_l = (total - gap) // 2
    box_r = total - gap - box_l
    return total, box_l, box_r, gap


def render_full_box(title, emoji, lines, width=None, color=None):
    """Render 1 box full-width (1 kolom)."""
    if width is None:
        total, _, _, _ = layout_widths()
        width = total
    c = color or C_MOSS_1

    label = f" {emoji} {title} " if emoji else f" {title} "
    label_vis = vwidth(label)
    dashes = max(0, width - label_vis - 3)
    print(f"  {c}┌─{label}{'─' * dashes}┐{C_RESET}")

    inner_w = width - 2
    for line in lines:
        line_vis = vwidth(line)
        pad = max(0, inner_w - 2 - line_vis)
        print(f"  {c}│{C_RESET} {line}{' ' * pad} {c}│{C_RESET}")

    print(f"  {c}└{'─' * (width - 2)}┘{C_RESET}")


def render_two_col_box(
    title_l, emoji_l, lines_l,
    title_r, emoji_r, lines_r,
    width=None, color=None,
):
    """Render 1 border utuh dengan 2 kolom di dalamnya."""
    if width is None:
        total, box_l, box_r, gap = layout_widths()
        width = total
    else:
        gap = 1
        box_l = (width - gap) // 2
        box_r = width - gap - box_l

    c = color or C_MOSS_1

    label_l = f" {emoji_l} {title_l} " if emoji_l else f" {title_l} "
    label_r = f" {emoji_r} {title_r} " if emoji_r else f" {title_r} "

    dashes_l = max(0, box_l - vwidth(label_l) - 3)
    dashes_r = max(0, box_r - vwidth(label_r) - 3)

    print(
        f"  {c}┌─{label_l}{'─' * dashes_l}┬"
        f"{label_r}{'─' * dashes_r}┐{C_RESET}"
    )

    max_rows = max(len(lines_l), len(lines_r))
    for i in range(max_rows):
        line_l = lines_l[i] if i < len(lines_l) else ""
        line_r = lines_r[i] if i < len(lines_r) else ""

        pad_l = max(0, box_l - 2 - vwidth(line_l))
        pad_r = max(0, box_r - 2 - vwidth(line_r))

        print(
            f"  {c}│{C_RESET} {line_l}{' ' * pad_l} "
            f"{c}│{C_RESET} {line_r}{' ' * pad_r} {c}│{C_RESET}"
        )

    print(f"  {c}└{'─' * box_l}┴{'─' * box_r}┘{C_RESET}")


def render_group_box(title, emoji, items, width=None, color=None):
    """Render grup menu dengan border utuh (1 kolom)."""
    if width is None:
        total, _, _, _ = layout_widths()
        width = total
    c = color or C_MOSS_1

    label = f" {emoji} {title} " if emoji else f" {title} "
    dashes = max(0, width - vwidth(label) - 3)
    print(f"  {c}┌─{label}{'─' * dashes}┐{C_RESET}")

    inner_w = width - 2
    for item in items:
        key, m_emoji, label_txt = item[:3]
        key_str = f"[{key}]"
        plain = f"  {key_str:>4}  {m_emoji}  {label_txt}"
        colored = (
            f"  {C_MOSS_1}{C_BOLD}{key_str:>4}{C_RESET}  "
            f"{m_emoji}  {C_WHITE}{label_txt}{C_RESET}"
        )
        pad = max(0, inner_w - 2 - vwidth(plain))
        print(f"  {c}│{C_RESET} {colored}{' ' * pad} {c}│{C_RESET}")

    print(f"  {c}└{'─' * (width - 2)}┘{C_RESET}")


def render_group_box_two_col(title, emoji, left, right, width=None, color=None):
    """Render grup menu 2 kolom dalam 1 border utuh."""
    if width is None:
        total, box_l, box_r, gap = layout_widths()
        width = total
    else:
        gap = 1
        box_l = (width - gap) // 2
        box_r = width - gap - box_l

    c = color or C_MOSS_1
    label = f" {emoji} {title} " if emoji else f" {title} "
    dashes = max(0, width - vwidth(label) - 3)
    print(f"  {c}┌─{label}{'─' * dashes}┐{C_RESET}")

    max_rows = max(len(left), len(right))
    for i in range(max_rows):
        l_item = left[i] if i < len(left) else None
        r_item = right[i] if i < len(right) else None

        def fmt(item, w):
            if item is None:
                return " " * (w - 2)
            key, m_emoji, label_txt = item[:3]
            key_str = f"[{key}]"
            plain = f"  {key_str:>4}  {m_emoji}  {label_txt}"
            colored = (
                f"  {C_MOSS_1}{C_BOLD}{key_str:>4}{C_RESET}  "
                f"{m_emoji}  {C_WHITE}{label_txt}{C_RESET}"
            )
            pad = max(0, w - 2 - vwidth(plain))
            return f"{colored}{' ' * pad}"

        line_l = fmt(l_item, box_l)
        line_r = fmt(r_item, box_r)
        print(f"  {c}│{C_RESET} {line_l} {c}│{C_RESET} {line_r} {c}│{C_RESET}")

    print(f"  {c}└{'─' * box_l}┴{'─' * box_r}┘{C_RESET}")


def render_merged_box(title, emoji, sections, width=None, color=None):
    """Render 1 box full-width dengan beberapa section (horizontal)."""
    if width is None:
        total, _, _, _ = layout_widths()
        width = total
    c = color or C_MOSS_1

    label = f" {emoji} {title} " if emoji else f" {title} "
    dashes = max(0, width - vwidth(label) - 3)
    print(f"  {c}┌─{label}{'─' * dashes}┐{C_RESET}")

    inner_w = width - 2
    n_sec = len(sections)
    if n_sec == 0:
        print(f"  {c}└{'─' * (width - 2)}┘{C_RESET}")
        return

    divider_w = 3
    total_divider = divider_w * (n_sec - 1)
    col_w = (inner_w - total_divider) // n_sec

    header_line = ""
    for i, sec in enumerate(sections):
        s_title = sec.get("title", "")
        s_emoji = sec.get("emoji", "")
        head = f" {s_emoji} {s_title} " if s_emoji else f" {s_title} "
        head_pad = vpad(head, col_w, "left")
        header_line += f"{C_MOSS_3}{head_pad}{C_RESET}"
        if i < n_sec - 1:
            header_line += f" {c}│{C_RESET} "
    print(f"  {c}│{C_RESET} {header_line} {c}│{C_RESET}")

    sep_line = ""
    for i in range(n_sec):
        sep_line += f"{C_SILVER}{'─' * col_w}{C_RESET}"
        if i < n_sec - 1:
            sep_line += f" {c}┼{C_RESET} "
    print(f"  {c}│{C_RESET} {sep_line} {c}│{C_RESET}")

    max_rows = max(len(sec.get("lines", [])) for sec in sections)
    for r in range(max_rows):
        row_parts = []
        for sec in sections:
            lines = sec.get("lines", [])
            content = lines[r] if r < len(lines) else ""
            content_pad = content + " " * max(0, col_w - vwidth(content))
            row_parts.append(content_pad)
        row_line = ""
        for i, part in enumerate(row_parts):
            row_line += part
            if i < n_sec - 1:
                row_line += f" {c}│{C_RESET} "
        print(f"  {c}│{C_RESET} {row_line} {c}│{C_RESET}")

    print(f"  {c}└{'─' * (width - 2)}┘{C_RESET}")


def render_merged_group(title, emoji, groups, width=None, color=None):
    """Render 1 box full-width dengan beberapa grup menu (horizontal)."""
    if width is None:
        total, _, _, _ = layout_widths()
        width = total
    c = color or C_MOSS_1

    label = f" {emoji} {title} " if emoji else f" {title} "
    dashes = max(0, width - vwidth(label) - 3)
    print(f"  {c}┌─{label}{'─' * dashes}┐{C_RESET}")

    inner_w = width - 2
    n_grp = len(groups)
    if n_grp == 0:
        print(f"  {c}└{'─' * (width - 2)}┘{C_RESET}")
        return

    divider_w = 3
    total_divider = divider_w * (n_grp - 1)
    col_w = (inner_w - total_divider) // n_grp

    header_line = ""
    for i, grp in enumerate(groups):
        g_title = grp.get("title", "")
        g_emoji = grp.get("emoji", "")
        head = f" {g_emoji} {g_title} " if g_emoji else f" {g_title} "
        head_pad = vpad(head, col_w, "left")
        header_line += f"{C_MOSS_3}{head_pad}{C_RESET}"
        if i < n_grp - 1:
            header_line += f" {c}│{C_RESET} "
    print(f"  {c}│{C_RESET} {header_line} {c}│{C_RESET}")

    sep_line = ""
    for i in range(n_grp):
        sep_line += f"{C_SILVER}{'─' * col_w}{C_RESET}"
        if i < n_grp - 1:
            sep_line += f" {c}┼{C_RESET} "
    print(f"  {c}│{C_RESET} {sep_line} {c}│{C_RESET}")

    max_rows = max(len(grp.get("items", [])) for grp in groups)

    for r in range(max_rows):
        row_parts = []
        for grp in groups:
            items = grp.get("items", [])
            if r < len(items):
                key, m_emoji, label_txt = items[r][:3]
                key_str = f"[{key}]"
                plain = f"  {key_str:>4}  {m_emoji}  {label_txt}"
                colored = (
                    f"  {C_MOSS_1}{C_BOLD}{key_str:>4}{C_RESET}  "
                    f"{m_emoji}  {C_WHITE}{label_txt}{C_RESET}"
                )
                pad = max(0, col_w - vwidth(plain))
                row_parts.append(f"{colored}{' ' * pad}")
            else:
                row_parts.append(" " * col_w)

        row_line = ""
        for i, part in enumerate(row_parts):
            row_line += part
            if i < n_grp - 1:
                row_line += f" {c}│{C_RESET} "
        print(f"  {c}│{C_RESET} {row_line} {c}│{C_RESET}")

    print(f"  {c}└{'─' * (width - 2)}┘{C_RESET}")


def render_vertical_box(title, emoji, sections, width=None, color=None):
    """Render 1 box full-width dengan section vertikal (stack atas-bawah)."""
    if width is None:
        total, _, _, _ = layout_widths()
        width = total
    c = color or C_MOSS_1

    label = f" {emoji} {title} " if emoji else f" {title} "
    dashes = max(0, width - vwidth(label) - 3)
    print(f"  {c}┌─{label}{'─' * dashes}┐{C_RESET}")

    print(f"  {c}│{C_RESET}{' ' * (width - 2)}{c}│{C_RESET}")

    for sec_idx, sec in enumerate(sections):
        s_title = sec.get("title", "")
        s_emoji = sec.get("emoji", "")
        s_lines = sec.get("lines", [])

        head = f"{s_emoji} {s_title}" if s_emoji else s_title
        head_vis = vwidth(f"  {head}")
        head_pad = max(0, width - 2 - head_vis)
        print(f"  {c}│{C_RESET}  {C_MOSS_2}{C_BOLD}{head}{C_RESET}{' ' * head_pad}{c}│{C_RESET}")

        for line in s_lines:
            line_vis = vwidth(line)
            pad = max(0, width - 4 - line_vis)
            print(f"  {c}│{C_RESET}  {line}{' ' * pad}  {c}│{C_RESET}")

        if sec_idx < len(sections) - 1:
            print(f"  {c}│{C_RESET}{' ' * (width - 2)}{c}│{C_RESET}")

    print(f"  {c}│{C_RESET}{' ' * (width - 2)}{c}│{C_RESET}")

    print(f"  {c}└{'─' * (width - 2)}┘{C_RESET}")


def render_vertical_group(title, emoji, groups, width=None, color=None):
    """Render 1 box full-width dengan grup menu vertikal (stack atas-bawah)."""
    if width is None:
        total, _, _, _ = layout_widths()
        width = total
    c = color or C_MOSS_1

    label = f" {emoji} {title} " if emoji else f" {title} "
    dashes = max(0, width - vwidth(label) - 3)
    print(f"  {c}┌─{label}{'─' * dashes}┐{C_RESET}")

    print(f"  {c}│{C_RESET}{' ' * (width - 2)}{c}│{C_RESET}")

    for grp_idx, grp in enumerate(groups):
        g_title = grp.get("title", "")
        g_emoji = grp.get("emoji", "")
        g_items = grp.get("items", [])

        head = f"{g_emoji} {g_title}" if g_emoji else g_title
        head_vis = vwidth(f"  {head}")
        head_pad = max(0, width - 2 - head_vis)
        print(f"  {c}│{C_RESET}  {C_MOSS_2}{C_BOLD}{head}{C_RESET}{' ' * head_pad}{c}│{C_RESET}")

        for item in g_items:
            key, m_emoji, label_txt = item[:3]
            key_str = f"[{key}]"
            plain = f"  {key_str:>4}  {m_emoji}  {label_txt}"
            colored = (
                f"  {C_MOSS_1}{C_BOLD}{key_str:>4}{C_RESET}  "
                f"{m_emoji}  {C_WHITE}{label_txt}{C_RESET}"
            )
            pad = max(0, width - 4 - vwidth(plain))
            print(f"  {c}│{C_RESET}  {colored}{' ' * pad}  {c}│{C_RESET}")

        if grp_idx < len(groups) - 1:
            print(f"  {c}│{C_RESET}{' ' * (width - 2)}{c}│{C_RESET}")

    print(f"  {c}│{C_RESET}{' ' * (width - 2)}{c}│{C_RESET}")

    print(f"  {c}└{'─' * (width - 2)}┘{C_RESET}")


# ═══════════════════════════════════════════════════════════
# BANNER (LUMOSS — v7.2.6) — ASCII-only, auto-width
# ═══════════════════════════════════════════════════════════

# ASCII art LUMOSS (tanpa emoji, biar lebar visual konsisten)
_LUMOSS_ART = [
    r"█╗     ██╗   ██╗███╗   ███╗ ██████╗ ███████╗███████╗",
    r"██║     ██║   ██║████╗ ████║██╔═══██╗██╔════╝██╔════╝",
    r"██║     ██║   ██║██╔████╔██║██║   ██║███████╗███████╗",
    r"██║     ██║   ██║██║╚██╔╝██║██║   ██║╚════██║╚════██║",
    r"███████╗╚██████╔╝██║ ╚═╝ ██║╚██████╔╝███████║███████║",
    r"╚══════╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚══════╝",
]

_LUMOSS_ART_WIDTH = max(len(line) for line in _LUMOSS_ART)


def print_banner(compact=False):
    """Cetak banner LUMOSS (v7.2.6 — Media Garden)."""
    if compact:
        print(f"\n{C_MOSS_1}─── {C_BOLD}lumoss{C_RESET}{C_MOSS_1} v{PROJECT_VERSION} ───{C_RESET}\n")
        return

    art_w = _LUMOSS_ART_WIDTH
    inner_w = art_w + 4
    border_top = "━" * (inner_w + 2)

    print()
    print(f"{C_MOSS_1}{C_BOLD}  ┏{border_top}┓{C_RESET}")

    print(f"{C_MOSS_1}{C_BOLD}  ┃{C_RESET}{' ' * (inner_w + 2)}{C_MOSS_1}{C_BOLD}┃{C_RESET}")

    for i, line in enumerate(_LUMOSS_ART):
        if i < 2:
            col = C_MOSS_1
        elif i < 4:
            col = C_MOSS_2
        elif i < 5:
            col = C_MOSS_3
        else:
            col = C_MOSS_4

        padded = line + " " * (art_w - len(line))
        print(f"{C_MOSS_2}{C_BOLD}  ┃{C_RESET}   {col}{padded}{C_RESET}   {C_MOSS_2}{C_BOLD}┃{C_RESET}")

    print(f"{C_MOSS_3}{C_BOLD}  ┃{C_RESET}{' ' * (inner_w + 2)}{C_MOSS_3}{C_BOLD}┃{C_RESET}")

    # Tagline — pake 🌿 sebagai simbol Lumoss
    tagline_vis = vwidth(f"  {LUMOSS_SYMBOL}  Media Garden, in bloom")
    tagline_pad = " " * max(0, inner_w + 2 - tagline_vis - 2)
    print(f"{C_MOSS_3}{C_BOLD}  ┃{C_RESET}   {LUMOSS_SYMBOL}  {C_WHITE}Media Garden, in bloom{C_RESET}{tagline_pad}{C_MOSS_3}{C_BOLD}┃{C_RESET}")

    # Author
    author_line = f"by {PROJECT_AUTHOR}"
    author_pad = " " * (inner_w + 2 - len(author_line) - 6)
    print(f"{C_MOSS_2}{C_BOLD}  ┃{C_RESET}       {C_SILVER}by {C_MOSS_1}{PROJECT_AUTHOR}{C_RESET}{author_pad}{C_MOSS_2}{C_BOLD}┃{C_RESET}")

    print(f"{C_MOSS_2}{C_BOLD}  ┃{C_RESET}{' ' * (inner_w + 2)}{C_MOSS_2}{C_BOLD}┃{C_RESET}")

    print(f"{C_MOSS_1}{C_BOLD}  ┗{border_top}┛{C_RESET}")
    print()


# ═══════════════════════════════════════════════════════════
# NOTIFIKASI SEDERHANA
# ═══════════════════════════════════════════════════════════

def print_success(msg):
    print(f"  {C_MOSS_1}✓{C_RESET} {msg}")


def print_error(msg):
    print(f"  {C_RED}✗{C_RESET} {msg}")


def print_warning(msg):
    print(f"  {C_YELLOW}⚠{C_RESET} {msg}")


def print_info(msg):
    print(f"  {C_MOSS_3}ℹ{C_RESET} {msg}")


def print_section(title, char="─", width=46):
    line = char * width
    print(f"\n{C_MOSS_2}{line}{C_RESET}")
    print(f"{C_MOSS_2}{C_BOLD}  {title}{C_RESET}")
    print(f"{C_MOSS_2}{line}{C_RESET}\n")


# ═══════════════════════════════════════════════════════════
# INPUT PROMPT
# ═══════════════════════════════════════════════════════════

def input_prompt(text, default=None, allow_empty=False):
    if default is not None and str(default) != "":
        prompt = f"{C_MOSS_1}{text}{C_RESET} {C_SILVER}[{default}]{C_RESET}: "
    else:
        prompt = f"{C_MOSS_1}{text}{C_RESET}: "

    try:
        val = input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return default if default is not None else ""

    if not val:
        if default is not None:
            return str(default)
        return ""
    return val


def input_yes_no(text, default="n"):
    default = default.lower()
    prompt = f"{C_MOSS_1}{text}{C_RESET} {C_SILVER}[y/n] (default: {default}){C_RESET}: "
    try:
        val = input(prompt).strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return default == "y"

    if not val:
        return default == "y"
    return val in ("y", "ya", "yes", "1", "true")


def input_int(text, default=0, min_val=None, max_val=None):
    while True:
        val = input_prompt(text, default=default)
        try:
            n = int(val)
            if min_val is not None and n < min_val:
                print_error(f"Nilai minimal {min_val}")
                continue
            if max_val is not None and n > max_val:
                print_error(f"Nilai maksimal {max_val}")
                continue
            return n
        except ValueError:
            print_error("Harus berupa angka")


def press_enter(msg="[Enter untuk lanjut]"):
    try:
        input(f"\n{C_SILVER}  {msg}{C_RESET}")
    except (EOFError, KeyboardInterrupt):
        print()


def confirm_action(text="Lanjutkan?"):
    return input_yes_no(f"{C_YELLOW}{text}{C_RESET}", default="n")


# ═══════════════════════════════════════════════════════════
# FORMATTERS
# ═══════════════════════════════════════════════════════════

def format_bytes(bytes_val, precision=1):
    if not bytes_val or bytes_val == 0:
        return "0 B"
    val = float(bytes_val)
    units = ["B", "kB", "MB", "GB", "TB"]
    i = 0
    while val >= 1024 and i < len(units) - 1:
        val /= 1024
        i += 1
    return f"{val:.{precision}f} {units[i]}"


def short_label(name, max_len=42):
    if len(name) <= max_len:
        return name
    keep = max_len - 3
    head = keep // 2
    tail = keep - head
    return f"{name[:head]}…{name[-tail:]}"


def truncate(text, max_len=32, ellipsis="…"):
    if len(text) <= max_len:
        return text
    return text[:max_len - len(ellipsis)] + ellipsis


def mask_secret(secret, show_first=6, show_last=4):
    if not secret:
        return "(kosong)"
    if len(secret) <= show_first + show_last:
        return "•" * len(secret)
    return f"{secret[:show_first]}...{secret[-show_last:]}"


def print_table(headers, rows, col_widths=None):
    if not col_widths:
        col_widths = []
        for i, h in enumerate(headers):
            max_w = len(h)
            for r in rows:
                if i < len(r):
                    max_w = max(max_w, len(str(r[i])))
            col_widths.append(min(max_w, 40))

    header_line = "  ".join(
        f"{C_BOLD}{C_MOSS_1}{h:<{w}}{C_RESET}"
        for h, w in zip(headers, col_widths)
    )
    print(f"  {header_line}")
    print(f"  {C_SILVER}{'─' * (sum(col_widths) + 2 * (len(headers) - 1))}{C_RESET}")

    for row in rows:
        line = "  ".join(
            f"{str(c)[:w]:<{w}}" if i < len(row) else " " * w
            for i, (c, w) in enumerate(zip(row + [""] * len(headers), col_widths))
        )
        print(f"  {line}")


# ═══════════════════════════════════════════════════════════
# BREADCRUMB
# ═══════════════════════════════════════════════════════════

def print_breadcrumb(items):
    if not items:
        return
    crumbs = []
    for i, item in enumerate(items):
        if i == len(items) - 1:
            crumbs.append(f"{C_BOLD}{C_MOSS_1}{item}{C_RESET}")
        else:
            crumbs.append(f"{C_SILVER}{item}{C_RESET}")
    sep = f" {C_SILVER}›{C_RESET} "
    print(f"\n  {sep.join(crumbs)}\n")


# ═══════════════════════════════════════════════════════════
# AESTHETIC MODERN UI
# ═══════════════════════════════════════════════════════════

def divider(color=None, char=DIVIDER_CHAR, width=DIVIDER_WIDTH):
    """Cetak garis divider aesthetic."""
    if color:
        print(f"{color}{char * width}{C_RESET}")
        return
    half = width // 2
    print(f"{C_MOSS_1}{char * half}{C_MOSS_3}{char * (width - half)}{C_RESET}")


def section_title(title, emoji="", subtitle="", color=None):
    """Cetak judul section gaya aesthetic."""
    c = color if color else C_MOSS_1
    divider()

    if emoji:
        title_full = f"{emoji}  {title}  ✦"
    else:
        title_full = f"{title}  ✦"

    padding = max(0, (DIVIDER_WIDTH - vwidth(title_full)) // 2)
    indent = " " * padding
    print(f"{indent}{c}{C_BOLD}{title_full}{C_RESET}")

    if subtitle:
        sub_padding = max(0, (DIVIDER_WIDTH - vwidth(subtitle)) // 2)
        print(f"{' ' * sub_padding}{C_SILVER}{subtitle}{C_RESET}")

    divider()


def kv_line(label, value, value_color=None, label_color=None, arrow=None):
    """Cetak baris key-value."""
    lc = label_color if label_color else C_MOSS_1
    vc = value_color if value_color else C_WHITE
    ar = arrow if arrow else ARROW

    label_padded = f"{label:<12}"

    value_str = str(value)
    if len(value_str) > 32:
        value_str = value_str[:31] + "…"

    print(
        f"  {lc}{label_padded}{C_RESET}"
        f"{C_SILVER} {ar}  {C_RESET}"
        f"{vc}{value_str}{C_RESET}"
    )


def menu_item(key, label, emoji="", key_color=None, label_col=12):
    """Cetak 1 item menu — alignment presisi pakai ANSI cursor."""
    kc = key_color if key_color else C_MOSS_1
    key_str = f"{key:>3}"

    print(f"  {kc}{C_BOLD}{key_str}{C_RESET}  {emoji}", end="")
    print(f"\033[{label_col}G{C_WHITE}{label}{C_RESET}")


def render_menu_item(
    num: str,
    emoji: str,
    label: str,
    num_w: int = 4,
    emoji_w: int = 4,
    label_w: int = 32,
    color_num: str = None,
    color_label: str = None,
    reset: str = None,
) -> str:
    """Render satu baris menu dengan alignment presisi."""
    if color_num is None:
        color_num = C_MOSS_1
    if color_label is None:
        color_label = C_WHITE
    if reset is None:
        reset = C_RESET

    n = vpad(num, num_w, "right")
    e = vpad(emoji, emoji_w, "center")
    l = vpad(label, label_w, "left")
    return f"  {color_num}{n}{reset}  {e}  {color_label}{l}{reset}"


def print_account_card(name="", slug="", userhash="", files_str="",
                       extra_lines=None, title="AKUN AKTIF", emoji="◉"):
    """Card akun gaya minimalist modern."""
    print()
    section_title(title, emoji=emoji)
    print()

    kv_line("Nama", name)
    kv_line("Slug", slug, value_color=C_MOSS_2)
    kv_line("Userhash", userhash, value_color=C_SILVER)
    kv_line("Files", files_str, value_color=C_MOSS_1)

    if extra_lines:
        for item in extra_lines:
            if len(item) == 2:
                lbl, val = item
                kv_line(lbl, val)
            elif len(item) == 3:
                _, lbl, val = item
                kv_line(lbl, val)

    print()
    divider()


def print_menu_card(title, items, emoji="◆", subtitle=""):
    """Menu card gaya minimalist modern."""
    print()
    section_title(title, emoji=emoji, subtitle=subtitle)
    print()

    for item in items:
        if len(item) == 2:
            key, label = item
            menu_item(key, label)
        elif len(item) == 3:
            key, label, m_emoji = item
            menu_item(key, label, emoji=m_emoji)

    print()
    divider()


def print_success_aesthetic(msg, emoji="✦"):
    print(f"  {C_MOSS_1}{emoji}{C_RESET}  {C_MOSS_1}{msg}{C_RESET}")


def print_error_aesthetic(msg, emoji="✗"):
    print(f"  {C_RED}{emoji}{C_RESET}  {C_RED}{msg}{C_RESET}")


def print_warning_aesthetic(msg, emoji="⚠"):
    print(f"  {C_YELLOW}{emoji}{C_RESET}  {C_YELLOW}{msg}{C_RESET}")


def print_info_aesthetic(msg, emoji="✦"):
    print(f"  {C_MOSS_3}{emoji}{C_RESET}  {C_SILVER}{msg}{C_RESET}")


def print_step(step_num, total, msg, emoji="◆"):
    print(f"  {C_MOSS_2}[{step_num}/{total}]{C_RESET}  {emoji}  {C_WHITE}{msg}{C_RESET}")


def print_highlight(label, value, emoji="✦"):
    print(f"  {C_MOSS_1}{emoji}  {C_BOLD}{label}:{C_RESET}  {C_MOSS_3}{value}{C_RESET}")


# ═══════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════

__all__ = [
    # Colors (standar)
    "C_RESET", "C_BOLD", "C_DIM",
    "C_BLACK", "C_RED", "C_GREEN", "C_YELLOW", "C_BLUE",
    "C_MAGENTA", "C_CYAN", "C_WHITE", "C_GRAY", "C_PURPLE", "C_ORANGE",
    "C_DIM_WHITE", "C_DIM_CYAN", "C_BRIGHT_MAGENTA", "C_BRIGHT_CYAN", "C_BRIGHT_YELLOW",
    # Luminous Moss palette
    "C_MOSS_1", "C_MOSS_2", "C_MOSS_3", "C_MOSS_4", "C_MOSS_DARK",
    "C_SILVER", "C_SILVER_LIGHT",
    # Gradient alias
    "C_GRAD_1", "C_GRAD_2", "C_GRAD_3", "C_GRAD_4", "C_GRAD_5", "C_GRAD_6", "C_GRAD_7",
    # Constants
    "PROJECT_NAME", "PROJECT_FULL", "PROJECT_VERSION",
    "PROJECT_AUTHOR", "PROJECT_DESC", "PROJECT_TAGLINE",
    "LUMOSS_SYMBOL",
    "DIVIDER_CHAR", "DIVIDER_WIDTH", "ARROW",
    # Visual width
    "vwidth", "vpad", "render_menu_item",
    # Emoji converter (v7.2.6)
    "EMOJI_TO_UNICODE", "convert_emoji", "strip_emoji",
    # Layout (v7.2.3)
    "layout_widths",
    "render_full_box", "render_two_col_box",
    "render_group_box", "render_group_box_two_col",
    # Merged (v7.2.4)
    "render_merged_box", "render_merged_group",
    # Vertical (v7.2.5)
    "render_vertical_box", "render_vertical_group",
    # Functions
    "clear_screen", "term_width", "term_height",
    "print_banner", "print_section",
    "print_success", "print_error", "print_warning", "print_info",
    "input_prompt", "input_yes_no", "input_int",
    "press_enter", "confirm_action",
    "format_bytes", "short_label", "truncate", "mask_secret", "print_table",
    "print_breadcrumb",
    # Aesthetic
    "divider", "section_title", "kv_line", "menu_item",
    "print_account_card", "print_menu_card",
    "print_success_aesthetic", "print_error_aesthetic",
    "print_warning_aesthetic", "print_info_aesthetic",
    "print_step", "print_highlight",
]