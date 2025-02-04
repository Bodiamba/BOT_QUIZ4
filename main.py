import aiogram
import asyncio
import logging
import sys

from aiogram import Bot

import game
import config_data
import handlers
import database
import fsm

from aiogram.client.session.aiohttp import AiohttpSession
session = AiohttpSession(proxy="http://proxy.server:3128")


dp = aiogram.Dispatcher() # Инициализация диспетчера
bot = aiogram.Bot(config_data.config.tg_bot.token, session=session) # Инициализация бота с соответствующим токеном
h = handlers.Handlers(bot, fsm.quiz_fsm) # Инициализация объекта для обработчиков для созданного бота с композицией FSM
h.register_handlers(dp) # Регистрация обработчиков

async def main() -> None:
    qr = game.Quiz(bot, database.db)
    for question in game.q:
        qr.add_question(question)
    h.set_quiz_class(qr)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
