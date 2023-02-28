import asyncio
import aiogram
from tokens import tgbot_token # Для безопасности токен бота создается отдельной переменной в отдельном файле
from handlers import tg_story_router

# В качестве фреймворка используется библиотека Aiogram, которая позволяет связываться с телеграм-ботом через API и асинхронность.
# https://docs.aiogram.dev/en/dev-3.x/


async def main():
    tg = aiogram.Bot(token=tgbot_token) # Подключение бота
    dp = aiogram.Dispatcher() # Основной узел выполнения
    dp.include_router(tg_story_router) # Подключение роутера (иного файла с инструкциями)

    await dp.start_polling(tg) # Запуск бота

if __name__ == "__main__":
    asyncio.run(main()) 
    # Если этот файл является исполняемым, то он запускает работу бота в асихнронном потоке.