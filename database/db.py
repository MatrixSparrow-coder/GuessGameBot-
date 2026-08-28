from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, MONGO_DB_NAME

_client = AsyncIOMotorClient(MONGO_URI)
db = _client[MONGO_DB_NAME]

# Collections
characters_col = db["characters"]          # character cards
groups_col = db["groups"]                  # per-group game state/settings
group_scores_col = db["group_scores"]      # per-group per-user points (all-time cache)
global_scores_col = db["global_scores"]    # global per-user points (all-time cache)
score_events_col = db["score_events"]      # every correct-guess event, timestamped (for daily/weekly leaderboards)
admins_col = db["admins"]                  # bot admins (besides owner)
settings_col = db["settings"]              # singleton bot-wide settings (log channel, start media, leaderboard image)
users_col = db["users"]                    # cache of user_id -> name (for leaderboard mentions)
banned_users_col = db["banned_users"]      # users banned from playing (by bot admin/owner)


async def ensure_indexes():
    await characters_col.create_index("card_id", unique=True)
    await group_scores_col.create_index([("chat_id", 1), ("user_id", 1)], unique=True)
    await global_scores_col.create_index("user_id", unique=True)
    await score_events_col.create_index([("chat_id", 1), ("timestamp", 1)])
    await score_events_col.create_index("timestamp")
    await admins_col.create_index("user_id", unique=True)
    await groups_col.create_index("chat_id", unique=True)
    await users_col.create_index("user_id", unique=True)
    await banned_users_col.create_index("user_id", unique=True)