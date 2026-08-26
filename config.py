import os

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
MONGO_URI = os.environ.get("MONGO_URI", "")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "guessbot")

# Owner user_id (Telegram numeric ID) - has full control, can add other admins
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))

SUPPORT_GROUP_LINK = os.environ.get("SUPPORT_GROUP_LINK", "https://t.me/InfiniteSelller")
DEVELOPER_USERNAME = os.environ.get("DEVELOPER_USERNAME", "Crew_allied")

# Game timing (seconds)
GUESS_WINDOW_SECONDS = int(os.environ.get("GUESS_WINDOW_SECONDS", "20"))
GAP_BETWEEN_DROPS_SECONDS = int(os.environ.get("GAP_BETWEEN_DROPS_SECONDS", "2"))

# How many recent drops to remember per group to avoid quick repeats
NO_REPEAT_HISTORY = int(os.environ.get("NO_REPEAT_HISTORY", "50"))

# Health check server port (for Render web service / uptime pings)
PORT = int(os.environ.get("PORT", "8080"))
