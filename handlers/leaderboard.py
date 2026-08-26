from pyrogram import filters
from pyrogram.types import Message, CallbackQuery

from bot_instance import app
from database.models import aggregate_scores, get_user_name, get_leaderboard_image
from utils.formatting import leaderboard_text
from utils.keyboards import leaderboard_keyboard
from utils.timeutils import since_epoch_for_period

PERIOD_TITLE = {"daily": "Today", "weekly": "This Week", "overall": "All Time"}


def _mention(user_id, name):
    return f'<a href="tg://user?id={user_id}">{name}</a>'


async def _build_leaderboard(scope: str, period: str, chat_id: int):
    since_epoch = since_epoch_for_period(period)
    target_chat = chat_id if scope == "group" else None

    scores = await aggregate_scores(target_chat, since_epoch, limit=10)
    rows = []
    for i, s in enumerate(scores, start=1):
        name = await get_user_name(s["user_id"])
        rows.append((i, _mention(s["user_id"], name), s["points"]))

    scope_label = "Group Leaderboard" if scope == "group" else "Global Leaderboard"
    title = f"{scope_label} — {PERIOD_TITLE[period]}"
    return leaderboard_text(title, rows)


async def _send_leaderboard(message: Message, scope: str, chat_id: int):
    period = "overall"
    text = await _build_leaderboard(scope, period, chat_id)
    kb = leaderboard_keyboard(scope, period)
    image = await get_leaderboard_image()
    if image:
        await message.reply_photo(image, caption=text, reply_markup=kb)
    else:
        await message.reply_text(text, reply_markup=kb)


@app.on_message(filters.command("top") & filters.group)
async def top_cmd(client, message: Message):
    await _send_leaderboard(message, "group", message.chat.id)


@app.on_message(filters.command("gtop"))
async def gtop_cmd(client, message: Message):
    await _send_leaderboard(message, "global", message.chat.id)


@app.on_callback_query(filters.regex(r"^lb_(group|global)_(daily|weekly|overall)$"))
async def leaderboard_switch_cb(client, callback_query: CallbackQuery):
    _, scope, period = callback_query.data.split("_")
    chat_id = callback_query.message.chat.id

    text = await _build_leaderboard(scope, period, chat_id)
    kb = leaderboard_keyboard(scope, period)

    await callback_query.answer()
    try:
        if callback_query.message.photo:
            await callback_query.message.edit_caption(text, reply_markup=kb)
        else:
            await callback_query.message.edit_text(text, reply_markup=kb)
    except Exception:
        # e.g. "message not modified" if tapping the already-active tab again
        pass