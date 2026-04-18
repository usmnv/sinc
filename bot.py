import asyncio
import logging
import os
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode

from config import BOT_TOKEN, PORT
from handlers import start, admission, exchange, guide, faq, manager

logging.basicConfig(level=logging.INFO)

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')
    
    def log_message(self, format, *args):
        pass

def run_health_server():
    server = HTTPServer(('0.0.0.0', PORT), HealthHandler)
    server.serve_forever()

async def main():
    # Создаем бота
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Подключаем роутеры
    dp.include_router(start.router)
    dp.include_router(admission.router)
    dp.include_router(exchange.router)
    dp.include_router(guide.router)
    dp.include_router(faq.router)
    dp.include_router(manager.router)
    
    # Запускаем healthcheck сервер
    health_thread = Thread(target=run_health_server, daemon=True)
    health_thread.start()
    
    logging.info("Бот запущен!")
    
    while True:
        try:
            await dp.start_polling(bot)
        except Exception as e:
            logging.error(f"Ошибка в polling: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
