import asyncio

# ---- Card creation conversation state (admin/owner only) ----
# user_id -> {"step": str, "data": {...}}
card_creation_state = {}

STEP_WAIT_PHOTO = "wait_photo"
STEP_WAIT_NAME = "wait_name"
STEP_WAIT_ANIME = "wait_anime"
STEP_WAIT_RARITY = "wait_rarity"
STEP_WAIT_POINTS = "wait_points"
STEP_CONFIRM = "confirm"


def start_card_flow(user_id):
    card_creation_state[user_id] = {"step": STEP_WAIT_PHOTO, "data": {}}


def get_card_flow(user_id):
    return card_creation_state.get(user_id)


def update_card_flow(user_id, **kwargs):
    if user_id in card_creation_state:
        card_creation_state[user_id]["data"].update(kwargs)


def set_card_step(user_id, step):
    if user_id in card_creation_state:
        card_creation_state[user_id]["step"] = step


def cancel_card_flow(user_id):
    card_creation_state.pop(user_id, None)


# ---- Active game loop tasks, one per group ----
# chat_id -> asyncio.Task
active_game_tasks = {}

# chat_id -> {"future": asyncio.Future, "card": dict}
pending_drops = {}


def is_game_running(chat_id):
    task = active_game_tasks.get(chat_id)
    return task is not None and not task.done()


def register_game_task(chat_id, task):
    active_game_tasks[chat_id] = task


def stop_game_task(chat_id):
    task = active_game_tasks.get(chat_id)
    if task and not task.done():
        task.cancel()
    active_game_tasks.pop(chat_id, None)
    pending_drops.pop(chat_id, None)


def set_pending_drop(chat_id, future, card):
    pending_drops[chat_id] = {"future": future, "card": card}


def get_pending_drop(chat_id):
    return pending_drops.get(chat_id)


def clear_pending_drop(chat_id):
    pending_drops.pop(chat_id, None)
