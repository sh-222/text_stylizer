from aiogram import Bot, Dispatcher
from handlers.message_handlers import router 
from handlers.callback_handlers import callback_router
import logging
import os
from dotenv import load_dotenv

def configure_logging():
    """Настройка логирования для приложения"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('bot.log')
        ]
    )

# Загрузка переменных окружения
load_dotenv()
configure_logging()

# Получение токена бота из переменной окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    """
    Основная функция запуска бота
    """
    # Подключаем роутеры
    dp.include_routers(router, callback_router)
    # Удаляем старые вебхуки
    await bot.delete_webhook(drop_pending_updates=True)
    #  Запускаем бота
    await dp.start_polling(bot)
    


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
