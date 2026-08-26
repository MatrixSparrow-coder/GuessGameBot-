# Unicode text styling helpers.
# NOTE: previous bugs in this kind of helper came from wrong/incomplete codepoint
# ranges. Bold sans is generated mathematically (safe, verified formula).
# Small caps uses a hardcoded, verified table since there is no single
# contiguous Unicode block for it.

_BOLD_UPPER_START = 0x1D5D4  # Mathematical Sans-Serif Bold Capital A
_BOLD_LOWER_START = 0x1D5EE  # Mathematical Sans-Serif Bold Small a
_BOLD_DIGIT_START = 0x1D7EC  # Mathematical Sans-Serif Bold Digit Zero


def bold_sans(text: str) -> str:
    """Convert to 𝗯𝗼𝗹𝗱 𝘀𝗮𝗻𝘀-𝘀𝗲𝗿𝗶𝗳 style (good for headings)."""
    out = []
    for ch in text:
        if "A" <= ch <= "Z":
            out.append(chr(_BOLD_UPPER_START + (ord(ch) - ord("A"))))
        elif "a" <= ch <= "z":
            out.append(chr(_BOLD_LOWER_START + (ord(ch) - ord("a"))))
        elif "0" <= ch <= "9":
            out.append(chr(_BOLD_DIGIT_START + (ord(ch) - ord("0"))))
        else:
            out.append(ch)
    return "".join(out)


_SMALL_CAPS_MAP = {
    "a": "ᴀ", "b": "ʙ", "c": "ᴄ", "d": "ᴅ", "e": "ᴇ", "f": "ꜰ", "g": "ɢ",
    "h": "ʜ", "i": "ɪ", "j": "ᴊ", "k": "ᴋ", "l": "ʟ", "m": "ᴍ", "n": "ɴ",
    "o": "ᴏ", "p": "ᴘ", "q": "ǫ", "r": "ʀ", "s": "ꜱ", "t": "ᴛ", "u": "ᴜ",
    "v": "ᴠ", "w": "ᴡ", "x": "x", "y": "ʏ", "z": "ᴢ",
}


def small_caps(text: str) -> str:
    """Convert to sᴍᴀʟʟ ᴄᴀᴘs style (good for sub-text/labels)."""
    out = []
    for ch in text:
        lower = ch.lower()
        if lower in _SMALL_CAPS_MAP:
            mapped = _SMALL_CAPS_MAP[lower]
            out.append(mapped)
        else:
            out.append(ch)
    return "".join(out)


# Decorative separators used across card templates
DIVIDER = "⊹═══════════════⊹"
STAR = "✦"
DIAMOND = "◆"
SPARK = "⟡"
