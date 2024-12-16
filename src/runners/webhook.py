import os
from aiohttp import web
from aiogram import types
from dotenv import load_dotenv

class WebhookRunner:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp    
        
        self.webhook_uri = os.getenv("WEBHOOK_URI") + f'/{os.getenv("TOKEN")}'
        self.token = os.getenv("TOKEN")
            
    async def set_webhook(self):
        webhook_uri = self.webhook_uri
        await self.bot.set_webhook(webhook_uri)

    async def on_startup(self, _):
        await self.set_webhook()

    async def on_shutdown(self, _):
        await self.bot.set_webhook("")

    async def handle_webhook(self, request):
        url = str(request.url)
        index = url.rfind("/")
        token = url[index + 1 :]

        if token != self.token:
            return web.Response(status=403)

        data = await request.json()
        update = types.Update(**data)
        await self.dp.feed_update(bot=self.bot, update=update)

        return web.Response()

    def run(self):
        app = web.Application()
        app.on_startup.append(self.on_startup)

        app.router.add_post(f'/{self.token}', self.handle_webhook)

        web.run_app(app, host="0.0.0.0", port=int(os.getenv("WEBHOOK_PORT", 8080)))
