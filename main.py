import logging

from pyrogram import idle

from bot_instance import app
from database.db import ensure_indexes
from database.models import all_active_groups

# Import handler modules so their @app.on_message / @app.on_callback_query
# decorators register with the shared `app` client instance.
import handlers.start        # noqa: F401
import handlers.admin        # noqa: F401
import handlers.game          # noqa: F401
import handlers.leaderboard  # noqa: F401

from handlers.game import start_game_for_group
from utils.health import start_health_server

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
log = logging.getLogger("guessbot")


async def main():
    await app.start()
    log.info("Client started, ensuring database indexes...")
    await ensure_indexes()

    log.info("Starting health-check server (for Render uptime pings)...")
    await start_health_server()

    log.info("Resuming game loops for previously active groups...")
    groups = await all_active_groups()
    for g in groups:
        await start_game_for_group(app, g["chat_id"], g.get("title"))
    log.info(f"Resumed {len(groups)} group(s).")

    me = await app.get_me()
    log.info(f"Bot @{me.username} is up and running!")

    await idle()

    log.info("Shutting down...")
    await app.stop()


if __name__ == "__main__":
    # IMPORTANT: do not use asyncio.run() here — pass the coroutine to app.run()
    # instead so Pyrogram manages the single event loop itself. Using a separate
    # asyncio.run() has previously caused the bot to connect but silently ignore
    # all incoming updates.
    app.run(main())
