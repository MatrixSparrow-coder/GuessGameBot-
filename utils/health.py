from aiohttp import web
from config import PORT


async def _health(request):
    return web.Response(text="OK")


async def start_health_server():
    app_ = web.Application()
    app_.router.add_get("/", _health)
    app_.router.add_get("/health", _health)
    runner = web.AppRunner(app_)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    return runner
