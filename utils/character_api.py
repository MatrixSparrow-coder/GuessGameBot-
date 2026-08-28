"""
Fetches random anime characters from free public APIs, for the /startweb
auto-card feature. Tries multiple sources so one API being down/rate-limited
doesn't stop the feature — it just falls through to the next source.

Sources:
  - AniList (GraphQL) — pulls from their top-favourited characters list
  - Jikan (MyAnimeList unofficial API) — has a genuine /random/characters endpoint
  - Jikan Top Characters — a second, independent Jikan endpoint for more variety

Each source returns a dict: {name, anime, image_url, source_name, source_url}
or None if it failed. `fetch_random_character()` shuffles the sources and
tries them in order until one succeeds.
"""

import random
import logging
import aiohttp

log = logging.getLogger("guessbot.character_api")

_TIMEOUT = aiohttp.ClientTimeout(total=10)

ANILIST_URL = "https://graphql.anilist.co"
ANILIST_QUERY = """
query ($page: Int) {
  Page(page: $page, perPage: 1) {
    characters(sort: FAVOURITES_DESC) {
      id
      name { full }
      image { large }
      media(perPage: 1, sort: POPULARITY_DESC) {
        nodes { title { romaji } }
      }
    }
  }
}
"""

JIKAN_RANDOM_URL = "https://api.jikan.moe/v4/random/characters"
JIKAN_TOP_URL = "https://api.jikan.moe/v4/top/characters"


async def fetch_from_anilist():
    page = random.randint(1, 500)  # top ~500 most-favourited characters on AniList
    try:
        async with aiohttp.ClientSession(timeout=_TIMEOUT) as session:
            async with session.post(
                ANILIST_URL, json={"query": ANILIST_QUERY, "variables": {"page": page}}
            ) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()

        chars = (((data.get("data") or {}).get("Page") or {}).get("characters")) or []
        if not chars:
            return None
        char = chars[0]
        name = (char.get("name") or {}).get("full")
        image_url = (char.get("image") or {}).get("large")
        media_nodes = ((char.get("media") or {}).get("nodes")) or []
        anime_name = media_nodes[0]["title"]["romaji"] if media_nodes else "Unknown"
        char_id = char.get("id")
        if not (name and image_url):
            return None
        return {
            "name": name,
            "anime": anime_name,
            "image_url": image_url,
            "source_name": "AniList",
            "source_url": f"https://anilist.co/character/{char_id}",
        }
    except Exception as e:
        log.warning(f"AniList fetch failed: {e}")
        return None


async def fetch_from_jikan_random():
    try:
        async with aiohttp.ClientSession(timeout=_TIMEOUT) as session:
            async with session.get(JIKAN_RANDOM_URL) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()

            char = data.get("data") or {}
            char_id = char.get("mal_id")
            name = char.get("name")
            image_url = ((char.get("images") or {}).get("jpg") or {}).get("image_url")
            if not (char_id and name and image_url):
                return None

            anime_name = "Unknown"
            try:
                async with session.get(f"https://api.jikan.moe/v4/characters/{char_id}/full") as resp2:
                    if resp2.status == 200:
                        full = await resp2.json()
                        animeo = (full.get("data") or {}).get("anime") or []
                        if animeo:
                            anime_name = animeo[0]["anime"]["title"]
            except Exception:
                pass

        return {
            "name": name,
            "anime": anime_name,
            "image_url": image_url,
            "source_name": "MyAnimeList",
            "source_url": f"https://myanimelist.net/character/{char_id}",
        }
    except Exception as e:
        log.warning(f"Jikan random fetch failed: {e}")
        return None


async def fetch_from_jikan_top():
    page = random.randint(1, 50)
    try:
        async with aiohttp.ClientSession(timeout=_TIMEOUT) as session:
            async with session.get(f"{JIKAN_TOP_URL}?page={page}") as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()

        items = data.get("data") or []
        if not items:
            return None
        char = random.choice(items)
        char_id = char.get("mal_id")
        name = char.get("name")
        image_url = ((char.get("images") or {}).get("jpg") or {}).get("image_url")
        anime_name = "Unknown"
        animeo = char.get("anime") or []
        if animeo:
            anime_name = animeo[0]["anime"]["title"]
        if not (name and image_url):
            return None
        return {
            "name": name,
            "anime": anime_name,
            "image_url": image_url,
            "source_name": "MyAnimeList",
            "source_url": f"https://myanimelist.net/character/{char_id}",
        }
    except Exception as e:
        log.warning(f"Jikan top fetch failed: {e}")
        return None


_SOURCES = [fetch_from_anilist, fetch_from_jikan_random, fetch_from_jikan_top]


async def fetch_random_character():
    """Tries each source (shuffled) until one succeeds. Returns None if all fail."""
    sources = _SOURCES[:]
    random.shuffle(sources)
    for source in sources:
        result = await source()
        if result:
            return result
    return None