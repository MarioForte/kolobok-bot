import aiogram
from tokens import tgbot_token
from handlers import tg_story_router

tg = aiogram.Bot(token=tgbot_token)
dp = aiogram.Dispatcher()
dp.include_router(tg_story_router)


if __name__ == "__main__":
    dp.start_polling(tg)