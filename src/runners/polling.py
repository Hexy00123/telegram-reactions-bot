import asyncio

class PollingRunner:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp 

    async def __run(self): 
        await self.dp.start_polling(self.bot)
        
    def run(self): 
        asyncio.run(self.__run())