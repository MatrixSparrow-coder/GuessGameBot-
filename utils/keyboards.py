# Colored buttons require Telegram Bot API 9.4+ (Feb 2026) and a Pyrogram/Pyrofork
# version that has been updated to expose the `style` field on button objects.
# Since this is a very recent Telegram feature, we defensively try to use it and
# fall back to a plain button (with a colored-emoji hint in the label) if the
# installed library version doesn't support the kwarg yet.
#
# If styled buttons don't render as colored on your bot, run:
#   pip install -U pyrofork
# to make sure you're on a version that ships Bot API 9.4 support.

from pyrogram.types import InlineKeyboardButton, KeyboardButton

_STYLE_EMOJI = {
    "primary": "🔵",
    "success": "🟢",
    "danger": "🔴",
}


def inline_btn(text, callback_data=None, url=None, style=None):
    kwargs = {"text": text}
    if callback_data is not None:
        kwargs["callback_data"] = callback_data
    if url is not None:
        kwargs["url"] = url
    if style:
        try:
            return InlineKeyboardButton(**kwargs, style=style)
        except TypeError:
            pass
    if style and style in _STYLE_EMOJI and not text.startswith(_STYLE_EMOJI[style]):
        kwargs["text"] = f"{_STYLE_EMOJI[style]} {text}"
    return InlineKeyboardButton(**kwargs)


def keyboard_btn(text, style=None, web_app_url=None):
    kwargs = {"text": text}
    if web_app_url:
        from pyrogram.types import WebAppInfo
        kwargs["web_app"] = WebAppInfo(url=web_app_url)
    if style:
        try:
            return KeyboardButton(**kwargs, style=style)
        except TypeError:
            pass
    if style and style in _STYLE_EMOJI and not text.startswith(_STYLE_EMOJI[style]):
        kwargs["text"] = f"{_STYLE_EMOJI[style]} {text}"
    return KeyboardButton(**kwargs)


_PERIOD_META = {
    "daily": ("📅", "Daily"),
    "weekly": ("🗓", "Weekly"),
    "overall": ("♾", "Overall"),
}


def leaderboard_keyboard(scope: str, active_period: str):
    """scope: 'group' or 'global'. active_period: 'daily' | 'weekly' | 'overall'."""
    from pyrogram.types import InlineKeyboardMarkup

    buttons = []
    for period, (emoji, label) in _PERIOD_META.items():
        prefix = "✅ " if period == active_period else ""
        buttons.append(
            inline_btn(f"{prefix}{emoji} {label}", callback_data=f"lb_{scope}_{period}")
        )
    return InlineKeyboardMarkup([buttons])