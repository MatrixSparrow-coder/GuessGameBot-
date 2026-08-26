from pyrogram import filters
from pyrogram.types import Message

from bot_instance import app
from database.models import (
    top_group_scores, top_global_scores, get_user_name, get_leaderboard_image,
)
from utils.formatting import leaderboard_text


def _mention(user_id, name):
    return f'<a href="tg://user?id={user_id}">{name}</a>'


@app.on_message(filters.command("top") & filters.group)
async def top_cmd(client, message: Message):
    scores = await top_group_scores(message.chat.id, limit=10)
    rows = []
    for i, s in enumerate(scores, start=1):
        name = await get_user_name(s["user_id"])
        rows.append((i, _mention(s["user_id"], name), s["points"]))

    text = leaderboard_text("Top Guessers", rows)
    image = await get_leaderboard_image()
    if image:
        await message.reply_photo(image, caption=text)
    else:
        await message.reply_text(text)


@app.on_message(filters.command("gtop"))
async def gtop_cmd(client, message: Message):
    scores = await top_global_scores(limit=10)
    rows = []
    for i, s in enumerate(scores, start=1):
        name = await get_user_name(s["user_id"])
        rows.append((i, _mention(s["user_id"], name), s["points"]))

    text = leaderboard_text("Global Leaderboard", rows)
    image = await get_leaderboard_image()
    if image:
        await message.reply_photo(image, caption=text)
    else:
        await message.reply_text(text)
