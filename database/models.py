import random
import time
from database.db import (
    characters_col, groups_col, group_scores_col,
    global_scores_col, admins_col, settings_col, users_col,
)
from config import OWNER_ID, NO_REPEAT_HISTORY

SETTINGS_ID = "bot_settings"


# ---------------- Characters ----------------

async def next_card_id() -> int:
    doc = await settings_col.find_one_and_update(
        {"_id": SETTINGS_ID},
        {"$inc": {"card_counter": 1}},
        upsert=True,
        return_document=True,
    )
    return doc["card_counter"]


async def add_character(card_id, file_id, name, anime, rarity, points, added_by, log_message_id=None):
    doc = {
        "card_id": card_id,
        "file_id": file_id,
        "name": name,
        "anime": anime,
        "rarity": rarity,
        "points": points,
        "added_by": added_by,
        "log_message_id": log_message_id,
        "created_at": time.time(),
    }
    await characters_col.insert_one(doc)
    return doc


async def get_character(card_id):
    return await characters_col.find_one({"card_id": card_id})


async def total_characters():
    return await characters_col.count_documents({})


async def random_character(exclude_ids):
    """Pick a random character not in exclude_ids. Falls back to full pool if everything is excluded."""
    cursor = characters_col.aggregate([
        {"$match": {"card_id": {"$nin": list(exclude_ids)}}},
        {"$sample": {"size": 1}},
    ])
    results = await cursor.to_list(length=1)
    if not results:
        cursor = characters_col.aggregate([{"$sample": {"size": 1}}])
        results = await cursor.to_list(length=1)
    return results[0] if results else None


# ---------------- Groups / Game state ----------------

async def get_group(chat_id):
    return await groups_col.find_one({"chat_id": chat_id})


async def ensure_group(chat_id, title=None):
    await groups_col.update_one(
        {"chat_id": chat_id},
        {
            "$setOnInsert": {
                "chat_id": chat_id,
                "title": title,
                "active": True,
                "recent_card_ids": [],
                "current_drop": None,
            }
        },
        upsert=True,
    )
    return await get_group(chat_id)


async def set_group_active(chat_id, active: bool):
    await groups_col.update_one({"chat_id": chat_id}, {"$set": {"active": active}}, upsert=True)


async def push_recent_card(chat_id, card_id):
    await groups_col.update_one(
        {"chat_id": chat_id},
        {
            "$push": {
                "recent_card_ids": {
                    "$each": [card_id],
                    "$slice": -NO_REPEAT_HISTORY,
                }
            }
        },
    )


async def set_current_drop(chat_id, drop_data):
    await groups_col.update_one({"chat_id": chat_id}, {"$set": {"current_drop": drop_data}})


async def clear_current_drop(chat_id):
    await groups_col.update_one({"chat_id": chat_id}, {"$set": {"current_drop": None}})


async def all_active_groups():
    cursor = groups_col.find({"active": True})
    return await cursor.to_list(length=None)


# ---------------- Scores ----------------

async def add_points(chat_id, user_id, points):
    await group_scores_col.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$inc": {"points": points}},
        upsert=True,
    )
    await global_scores_col.update_one(
        {"user_id": user_id},
        {"$inc": {"points": points}},
        upsert=True,
    )


async def top_group_scores(chat_id, limit=10):
    cursor = group_scores_col.find({"chat_id": chat_id}).sort("points", -1).limit(limit)
    return await cursor.to_list(length=limit)


async def top_global_scores(limit=10):
    cursor = global_scores_col.find({}).sort("points", -1).limit(limit)
    return await cursor.to_list(length=limit)


# ---------------- Users cache (for mention links on leaderboard) ----------------

async def cache_user(user_id, name):
    await users_col.update_one(
        {"user_id": user_id},
        {"$set": {"name": name}},
        upsert=True,
    )


async def get_user_name(user_id):
    doc = await users_col.find_one({"user_id": user_id})
    return doc["name"] if doc else str(user_id)


# ---------------- Admins ----------------

async def is_owner(user_id):
    return user_id == OWNER_ID


async def is_admin(user_id):
    if user_id == OWNER_ID:
        return True
    doc = await admins_col.find_one({"user_id": user_id})
    return doc is not None


async def add_admin(user_id, added_by):
    await admins_col.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id, "added_by": added_by, "added_at": time.time()}},
        upsert=True,
    )


async def remove_admin(user_id):
    await admins_col.delete_one({"user_id": user_id})


async def list_admins():
    cursor = admins_col.find({})
    return await cursor.to_list(length=None)


# ---------------- Bot-wide settings (log channel, start media, leaderboard image) ----------------

async def get_settings():
    doc = await settings_col.find_one({"_id": SETTINGS_ID})
    return doc or {}


async def set_log_channel(chat_id):
    await settings_col.update_one({"_id": SETTINGS_ID}, {"$set": {"log_channel_id": chat_id}}, upsert=True)


async def get_log_channel():
    doc = await get_settings()
    return doc.get("log_channel_id")


async def set_start_media(file_id, media_type):
    await settings_col.update_one(
        {"_id": SETTINGS_ID},
        {"$set": {"start_media_file_id": file_id, "start_media_type": media_type}},
        upsert=True,
    )


async def get_start_media():
    doc = await get_settings()
    return doc.get("start_media_file_id"), doc.get("start_media_type")


async def set_leaderboard_image(file_id):
    await settings_col.update_one({"_id": SETTINGS_ID}, {"$set": {"leaderboard_image_id": file_id}}, upsert=True)


async def get_leaderboard_image():
    doc = await get_settings()
    return doc.get("leaderboard_image_id")
