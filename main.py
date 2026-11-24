#!/usr/bin/env python3
"""THE WORLD TODAY - Tuesday 24 November 2026.

A newspaper front page summarising the world's news of 24 November 2026,
drawn entirely with a hand-authored 5x7 bitmap font and a hand-rolled PNG
encoder. Stdlib only (os, struct, zlib). No network, no clock, no random
input: the same input always produces the same bytes.

Run:  python3 main.py
Output: $MAKEFUN_OUTPUT_DIR/entry.png (or ./entry.png if unset).
"""

import os
import struct
import zlib

W = 1024
H = 1024

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (176, 0, 0)
GREY = (96, 96, 96)
NAVY = (0, 46, 92)
PAPER = (252, 250, 244)

# ---------------------------------------------------------------------------
# Hand-authored 5x7 bitmap font. Each glyph is 7 rows of 5 bits, '#' = ink.
# Authored in this session; uppercase only (all copy is uppercased first).
# ---------------------------------------------------------------------------
GLYPHS = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "00000", "01100"),
    ",": ("00000", "00000", "00000", "00000", "00000", "01100", "00100"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "*": ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "@": ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
}

BLANK = ("00000",) * 7


def glyph(ch):
    return GLYPHS.get(ch, BLANK)


# ---------------------------------------------------------------------------
# Canvas: RGB bytearray, origin top-left.
# ---------------------------------------------------------------------------
canvas = bytearray([255]) * (W * H * 3)


def fill(r, g, b):
    for i in range(0, len(canvas), 3):
        canvas[i] = r
        canvas[i + 1] = g
        canvas[i + 2] = b


def px(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        canvas[i] = color[0]
        canvas[i + 1] = color[1]
        canvas[i + 2] = color[2]


def rect(x, y, w, h, color):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            px(xx, yy, color)


def hline(x, y, w, color, thick=1):
    rect(x, y, w, thick, color)


# ---------------------------------------------------------------------------
# Text: 6px advance per glyph (5 + 1 spacing), scaled.
# ---------------------------------------------------------------------------
def text_width(s, scale):
    return len(s) * 6 * scale - scale


def draw_char(x, y, ch, scale, color, bold=False):
    rows = glyph(ch)
    for r in range(7):
        row = rows[r]
        for c in range(5):
            if row[c] == "1":
                for dy in range(scale):
                    for dx in range(scale):
                        px(x + c * scale + dx, y + r * scale + dy, color)
                        if bold:
                            px(x + c * scale + dx + 1, y + r * scale + dy, color)


def draw_text(x, y, s, scale, color, bold=False):
    cx = x
    for ch in s:
        draw_char(cx, y, ch, scale, color, bold)
        cx += 6 * scale
    return cx


def wrap(s, max_w, scale):
    """Greedy word wrap; returns a list of lines that fit max_w pixels."""
    lines = []
    for para in s.split("\n"):
        words = para.split(" ")
        cur = ""
        for word in words:
            trial = word if not cur else cur + " " + word
            if text_width(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def draw_para(x, y, s, scale, color, max_w, line_h, bold=False):
    """Draw wrapped text; returns the y just below the last line."""
    for line in wrap(s, max_w, scale):
        draw_text(x, y, line, scale, color, bold)
        y += line_h
    return y


def centered(s, y, scale, color, bold=False):
    x = (W - text_width(s, scale)) // 2
    draw_text(x, y, s, scale, color, bold)
    return y + 7 * scale


# ---------------------------------------------------------------------------
# Content: the verified news of Tuesday 24 November 2026.
# Each story: (section, headline, deck-with-source).
# ---------------------------------------------------------------------------
LEAD = (
    "WAR IN EUROPE - LEAD STORY",
    "NATO SENDS AWACS TO POLAND AFTER RUSSIAN MISSILES LAND",
    "THREE KH-101 MISSILES LANDED ON FRIDAY, RAISING FEARS RUSSIA'S WAR IN "
    "UKRAINE COULD SPILL INTO NATO TERRITORY. SOURCE: REUTERS, 23-24 NOV.",
)

STORIES = [
    (
        "WAR IN EUROPE",
        "UKRAINE SINKS RUSSIAN CORVETTE IN LIBYA PORT",
        "MARITIME DRONES SANK THE MISSILE CORVETTE, BELIEVED TO BE THE "
        "MERKURY, IN BENGHAZI ON SUNDAY. A DAY EARLIER A DRONE HIT THE "
        "CARGO SHIP SPARTA II IN THE GULF OF FINLAND. SOURCE: REUTERS / "
        "NAVAL NEWS.",
    ),
    (
        "CLIMATE",
        "COP31 TALKS COLLAPSE WITHOUT A DEAL",
        "THE FIRST CLIMATE-SUMMIT FAILURE SINCE 2009. THE BLAME GAME BEGAN "
        "IN AUSTRALIA AS PACIFIC NATIONS EXPRESSED DESPAIR. SOURCE: BBC / "
        "REUTERS.",
    ),
    (
        "MIDDLE EAST",
        "IRAN: SINGER AND CREW GIVEN 74 LASHES EACH",
        "TEHRAN VOWS TO USE ALL ITS TOOLS AGAINST THE US NAVAL BLOCKADE AS "
        "WASHINGTON SANCTIONS DOZENS LINKED TO SHADOW BANKING. SOURCE: "
        "REUTERS.",
    ),
    (
        "MIDDLE EAST",
        "ISRAELI STRIKES KILL THREE IN GAZA; SETTLER ARSON HITS WEST BANK",
        "THE DEAD INCLUDE A WORKER WITH UNRWA. ARSON HIT FIVE PALESTINIAN "
        "VILLAGES OVERNIGHT, CONDEMNED AS JEWISH TERRORISM BY OPPOSITION "
        "LEADER GADI EISENKOT. SOURCE: REUTERS.",
    ),
    (
        "AMERICAS",
        "TRUMP HALTS DETONATION OF TOXIC LEAD AZIDE STOCKPILE",
        "THE US ARMY WAS ORDERED TO PAUSE DESTRUCTION OF THE DETERIORATING "
        "STOCKPILE IN IOWA. TRUMP SAYS HE SECURED A DEAL FOR JENSEN HUANG "
        "TO RETURN AS NVIDIA CEO. SOURCE: REUTERS / FRANCE 24.",
    ),
    (
        "ASIA",
        "INDONESIA CANDY FACTORY FIRE KILLS AT LEAST 24",
        "DOZENS ARE MISSING AS RESCUERS SEARCH THE SITE. SOURCE: REUTERS.",
    ),
    (
        "ASIA",
        "COURT RULES MYANMAR COMMITTED GENOCIDE AGAINST ROHINGYA",
        "THE INTERNATIONAL COURT OF JUSTICE DELIVERED ITS RULING ON "
        "TUESDAY. SOURCE: REUTERS.",
    ),
    (
        "AMERICAS",
        "WAYMO PULLS DRIVERLESS TAXIS FROM ALL US FREEWAYS",
        "THE SUSPENSION FOLLOWS A CALIFORNIA FREEWAY BAN AFTER TRAFFIC "
        "INCIDENTS. SOURCE: REUTERS.",
    ),
    (
        "SPORT",
        "ALCARAZ WINS MAIDEN ATP FINALS TITLE",
        "HE BEAT ALEXANDER ZVEREV IN TURIN. INDIA V NEW ZEALAND FIRST TEST "
        "DRAWN IN WELLINGTON; GUKESH BEGINS WORLD CHESS TITLE DEFENCE IN "
        "GENEVA. SOURCE: REUTERS / TIMES OF INDIA.",
    ),
]


# ---------------------------------------------------------------------------
# Page layout.
# ---------------------------------------------------------------------------
MX = 40                 # side margin
CW = W - 2 * MX         # content width


def draw_page():
    fill(*PAPER)
    # Outer frame.
    rect(0, 0, W, 6, BLACK)
    rect(0, H - 6, W, 6, BLACK)
    rect(0, 0, 6, H, BLACK)
    rect(W - 6, 0, 6, H, BLACK)

    y = 26
    # Masthead.
    y = centered("THE WORLD TODAY", y, 6, NAVY, bold=True)
    y += 6
    hline(MX, y, CW, RED, 4)
    y += 12
    y = centered("TUESDAY 24 NOVEMBER 2026", y, 2, BLACK, bold=True)
    y += 4
    y = centered("THE WORLD'S NEWS IN ONE PAGE", y, 1, GREY)
    y += 12
    hline(MX, y, CW, BLACK, 2)
    y += 12

    # Lead story.
    label, headline, deck = LEAD
    draw_text(MX, y, label, 1, RED, bold=True)
    y += 12
    y = draw_para(MX, y, headline, 3, BLACK, CW, 26, bold=True)
    y += 4
    y = draw_para(MX, y, deck, 2, BLACK, CW, 18)
    y += 8
    hline(MX, y, CW, BLACK, 2)
    y += 10

    # Remaining stories.
    for section, headline, deck in STORIES:
        draw_text(MX, y, section, 1, RED, bold=True)
        y += 11
        y = draw_para(MX, y, headline, 2, BLACK, CW, 18, bold=True)
        y += 2
        y = draw_para(MX, y, deck, 1, BLACK, CW, 12)
        y += 7
        hline(MX, y, CW, GREY, 1)
        y += 12

    # "By the numbers" strip: the day's key figures at a glance.
    draw_text(MX, y, "BY THE NUMBERS", 1, RED, bold=True)
    y += 12
    rect(MX, y, CW, 2, RED)
    y += 8
    y = draw_para(MX, y, "3 MISSILES IN POLAND - 74 LASHES EACH - "
                          "24 KILLED IN FACTORY FIRE", 2, BLACK, CW, 20, bold=True)
    y = draw_para(MX, y, "0 DEALS AT COP31 - 1 GENOCIDE RULING - "
                          "1 MAIDEN ATP FINALS TITLE", 2, BLACK, CW, 20, bold=True)
    y += 4
    rect(MX, y, CW, 2, RED)

    # Footer.
    y = H - 34
    hline(MX, y, CW, BLACK, 2)
    y += 8
    centered(
        "SOURCES: REUTERS - BBC - FRANCE 24 - NAVAL NEWS - TIMES OF INDIA",
        y, 1, GREY,
    )


# ---------------------------------------------------------------------------
# Minimal PNG encoder: 8-bit RGB, filter 0, fixed zlib level.
# ---------------------------------------------------------------------------
def png_chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png():
    raw = bytearray()
    for row in range(H):
        raw.append(0)
        raw += canvas[row * W * 3:(row + 1) * W * 3]
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + png_chunk(b"IHDR", ihdr)
        + png_chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + png_chunk(b"IEND", b"")
    )


def main():
    draw_page()
    data = encode_png()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "."
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
