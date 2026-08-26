from pyrogram import Client
from pyrogram.enums import ParseMode
from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "guessbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=False,  # keep session persisted; avoids re-auth / flood issues on restart
    parse_mode=ParseMode.HTML,  # all card/leaderboard templates use HTML tags (<b>, <code>, <a href>)
)
