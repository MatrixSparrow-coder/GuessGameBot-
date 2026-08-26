from utils.fonts import bold_sans, small_caps, DIVIDER

RARITY_EMOJI = {
    "Common": "🟤",
    "Rare": "🟢",
    "Epic": "🔵",
    "Legendary": "🟣",
}


def welcome_text(user_name, user_id):
    mention = f'<a href="tg://user?id={user_id}">{user_name}</a>'
    heading = bold_sans("Welcome")
    tag = small_caps("this is a character guessing game bot")
    return (
        f"✧ {heading}, {mention} ✧\n\n"
        f"⟡ {tag}\n\n"
        f"⌬ Guess anime characters every drop, earn points, and top the leaderboard!\n\n"
        f"⊹ Add me to your group and let the game begin ⊹"
    )


def help_text():
    heading = bold_sans("Help & Commands")
    return (
        f"✦ {heading} ✦\n{DIVIDER}\n\n"
        f"⟡ <b>{small_caps('game commands')}</b>\n"
        f"◆ /top — group leaderboard\n"
        f"◆ /gtop — global leaderboard\n"
        f"◆ /stopgame — pause the game (admin only)\n"
        f"◆ /startgame — resume the game (admin only)\n\n"
        f"⟡ <b>{small_caps('owner / admin commands')}</b>\n"
        f"◆ /addadmin — reply to a user to make them bot admin\n"
        f"◆ /addlog — run inside a channel (bot must be admin there) to set it as the card logs channel\n"
        f"◆ /addcard — start the guided card creation flow\n"
        f"◆ /startmedia — reply to a photo/video (max 60s) to attach it to /start\n"
        f"◆ /imageleb — reply to a photo to set the leaderboard banner image\n\n"
        f"{DIVIDER}\n"
        f"⌬ Guess the character's name in the group chat within the time limit to earn points!"
    )


def drop_caption():
    heading = bold_sans("Unknown Character")
    tag = small_caps("who is this? guess the name!")
    return (
        f"⛧ ⟢ {heading} ⟣ ⛧\n"
        f"❖ {tag}\n"
        f"⏱ 20 seconds • 💬 reply with the name"
    )


def correct_caption(name, anime, rarity, points, winner_mention):
    heading = bold_sans("Character Revealed")
    rarity_e = RARITY_EMOJI.get(rarity, "⚪")
    return (
        f"✦ ⟡ {heading} ⟡ ✦\n\n"
        f"⌬ {small_caps('name')}: <b>{name}</b>\n"
        f"❖ {small_caps('anime')}: {anime}\n"
        f"◆ {small_caps('rarity')}: {rarity_e} {rarity}\n"
        f"🏅 {small_caps('winner')}: {winner_mention}\n"
        f"💎 +{points} {small_caps('points')}"
    )


def timeout_caption(name, anime, rarity):
    heading = bold_sans("Character Revealed")
    rarity_e = RARITY_EMOJI.get(rarity, "⚪")
    return (
        f"✦ ⟡ {heading} ⟡ ✦\n\n"
        f"⌬ {small_caps('name')}: <b>{name}</b>\n"
        f"❖ {small_caps('anime')}: {anime}\n"
        f"◆ {small_caps('rarity')}: {rarity_e} {rarity}\n"
        f"⏰ {small_caps('nobody guessed it right')}"
    )


def leaderboard_text(title, rows):
    """rows: list of (rank, mention_html, points)"""
    heading = bold_sans(title)
    lines = [f"⛧ ✦ {heading} ✦ ⛧", DIVIDER, ""]
    medals = ["🥇", "🥈", "🥉"]
    if not rows:
        lines.append(small_caps("no scores yet"))
    for i, (rank, mention, points) in enumerate(rows):
        prefix = medals[i] if i < 3 else f"{rank}."
        lines.append(f"{prefix} {mention} — {points} pts")
    return "\n".join(lines)


def card_preview_caption(name, anime, rarity, points):
    heading = bold_sans("Card Preview")
    rarity_e = RARITY_EMOJI.get(rarity, "⚪")
    return (
        f"⧫ {heading} ⧫\n{DIVIDER}\n\n"
        f"⌬ {small_caps('name')}: <b>{name}</b>\n"
        f"❖ {small_caps('anime')}: {anime}\n"
        f"◆ {small_caps('rarity')}: {rarity_e} {rarity}\n"
        f"⭐ {small_caps('points')}: {points}\n"
        f"{DIVIDER}\n"
        f"{small_caps('confirm to save this card')}"
    )


def log_channel_caption(card_id, name, anime, rarity, points, added_by_mention):
    heading = bold_sans(name)
    rarity_e = RARITY_EMOJI.get(rarity, "⚪")
    return (
        f"⧫ {heading} ⧫\n{DIVIDER}\n"
        f"🆔 {small_caps('card id')}: #{card_id}\n"
        f"❖ {small_caps('anime')}: {anime}\n"
        f"◆ {small_caps('rarity')}: {rarity_e} {rarity}\n"
        f"⭐ {small_caps('points')}: {points}\n"
        f"👤 {small_caps('added by')}: {added_by_mention}\n"
        f"{DIVIDER}\n"
        f"<code>CARD_ID:{card_id}</code>"
    )
