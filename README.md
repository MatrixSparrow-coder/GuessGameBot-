# Character Guessing Bot

Auto-drops anime character images in a group every few seconds. First person to
type the correct name (partial match works) gets points. Card creation, log
channel, and leaderboard banners are all managed from inside Telegram — no
website, no external panel.

## 1. Get your credentials

| Variable | Where to get it |
|---|---|
| `API_ID`, `API_HASH` | https://my.telegram.org → API Development Tools |
| `BOT_TOKEN` | @BotFather → /newbot |
| `MONGO_URI` | MongoDB Atlas (free tier) → Connect → Drivers → copy connection string |
| `OWNER_ID` | @userinfobot → send any message, it replies with your numeric ID |

## 2. Deploy on Render

1. Push this folder to a GitHub repo.
2. On Render → New → Web Service → connect the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `python main.py`
5. Add all variables from `.env.example` under Environment.
6. Deploy. Once live, ping `https://your-app.onrender.com/health` every ~10 min
   with cron-job.org to keep the free tier awake (same as your VoteZen setup).

## 3. First-time bot setup (do this in order, from Telegram)

1. **Create a private channel** (or reuse one) that will store all character
   cards. Add the bot to it as **admin**.
2. Set it as the logs channel — DM the bot:
   ```
   /addlog @yourchannelusername
   ```
   (or `/addlog -100xxxxxxxxxx` if it's a private channel without a username —
   forward any message from the channel to @getidsbot or similar to get the ID)
3. Add yourself and any helpers as bot admins (only needed for people other
   than the `OWNER_ID` — the owner already has full access):
   ```
   /addadmin   (reply to their message in the bot's DM)
   ```
4. Add character cards:
   ```
   /addcard
   ```
   Follow the steps: send image → name → anime → rarity → points → confirm.
   Each confirmed card is posted to the logs channel and saved to the database.
5. (Optional) Set a welcome media for /start:
   ```
   /startmedia   (reply to a photo or video, max 60s)
   ```
6. (Optional) Set a leaderboard banner image:
   ```
   /imageleb   (reply to a photo)
   ```

## 4. Using it in a group

- Add the bot to any group and make it **admin** (needs permission to send
  photos/messages).
- The game **starts automatically** the moment it's added — no command needed.
- Group admins can pause/resume anytime with `/stopgame` and `/startgame`.
- `/top` → leaderboard for that group. `/gtop` → leaderboard across all groups.

## Notes on the "colored buttons"

Telegram added real button colors (`style: primary/success/danger`) in **Bot
API 9.4 (Feb 2026)**. This code already uses that field wherever it makes
sense (Help/Support/Developer buttons, Confirm/Cancel in card creation). If
your installed library is older and doesn't support it yet, buttons will
silently fall back to plain buttons with a colored emoji circle in the label
instead of crashing. Run this once in a while to stay current:
```
pip install -U pyrofork
```

## Project structure

```
main.py                 entry point
bot_instance.py          shared Client instance
config.py                env var loading
database/db.py           MongoDB collections
database/models.py       all DB read/write helpers
handlers/start.py        /start /help /startmedia
handlers/admin.py        /addadmin /addlog /addcard (card creation flow) /imageleb
handlers/game.py         auto drop loop, guessing, /startgame /stopgame
handlers/leaderboard.py  /top /gtop
utils/fonts.py           bold/small-caps text styling
utils/formatting.py      all message/card templates
utils/keyboards.py       colored-button helpers with safe fallback
utils/state.py           in-memory card-creation + active-game state
utils/health.py          aiohttp uptime endpoint
```

## Known limitations to mention to the client (v1 → will improve later)

- Rarity and per-card points exist, but there's no "collection/inventory" —
  it's points-only for now, as agreed.
- `/addlog` posted *inside* the channel only works if you're not posting
  anonymously — otherwise use the DM version (`/addlog @channel`).
- Guess matching is case-insensitive substring match (e.g. "Sakura" matches
  "Sakura Haruno"), not fuzzy/typo-tolerant yet.
