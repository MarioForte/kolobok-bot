import asyncio
import aiogram
from tokens import tgbot_token
from handlers import tg_story_router


async def main():
    tg = aiogram.Bot(token=tgbot_token)
    dp = aiogram.Dispatcher()
    dp.include_router(tg_story_router)

    await dp.start_polling(tg)

if __name__ == "__main__":
    asyncio.run(main())