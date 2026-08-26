from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup

from bot_instance import app
from config import SUPPORT_GROUP_LINK, DEVELOPER_USERNAME
from database.models import (
    cache_user, get_start_media, set_start_media, is_admin,
)
from utils.formatting import welcome_text, help_text
from utils.keyboards import inline_btn


def _start_keyboard():
    bot_username = app.me.username if app.me else ""
    return InlineKeyboardMarkup([
        [
            inline_btn("Help", callback_data="show_help", style="primary"),
            inline_btn("Support Group", url=SUPPORT_GROUP_LINK, style="success"),
        ],
        [
            inline_btn("Developer", url=f"https://t.me/{DEVELOPER_USERNAME}", style="danger"),
        ],
    ])


@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message: Message):
    user = message.from_user
    await cache_user(user.id, user.first_name or user.username or str(user.id))

    text = welcome_text(user.first_name or "there", user.id)
    kb = _start_keyboard()

    file_id, media_type = await get_start_media()
    if file_id and media_type == "photo":
        await message.reply_photo(file_id, caption=text, reply_markup=kb)
    elif file_id and media_type == "video":
        await message.reply_video(file_id, caption=text, reply_markup=kb)
    else:
        await message.reply_text(text, reply_markup=kb, disable_web_page_preview=True)


@app.on_message(filters.command("help"))
async def help_cmd(client, message: Message):
    await message.reply_text(help_text())


@app.on_callback_query(filters.regex("^show_help$"))
async def show_help_cb(client, callback_query):
    await callback_query.answer()
    await callback_query.message.reply_text(help_text())


@app.on_message(filters.command("startmedia") & filters.private)
async def startmedia_cmd(client, message: Message):
    if not await is_admin(message.from_user.id):
        await message.reply_text("⛔ This command is for bot admins/owner only.")
        return

    replied = message.reply_to_message
    if not replied or not (replied.photo or replied.video):
        await message.reply_text(
            "↩️ Reply to a photo or video (max 60 seconds) with /startmedia to set it as the /start attachment."
        )
        return

    if replied.video and replied.video.duration and replied.video.duration > 60:
        await message.reply_text("⛔ Video is too long. Max allowed is 60 seconds.")
        return

    if replied.photo:
        await set_start_media(replied.photo.file_id, "photo")
    else:
        await set_start_media(replied.video.file_id, "video")

    await message.reply_text("✅ Start media updated! It will now show with every /start message.")
