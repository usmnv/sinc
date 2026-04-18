import os
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)

# Подключение к Supabase
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    logging.info("✅ Supabase подключен успешно!")
except Exception as e:
    logging.error(f"❌ Ошибка подключения к Supabase: {e}")
    raise

# ========== ПОЛЬЗОВАТЕЛИ ==========
async def user_exists(tg_id: int) -> bool:
    try:
        response = supabase.table("users").select("id").eq("tg_id", tg_id).execute()
        return len(response.data) > 0
    except Exception as e:
        logging.error(f"Ошибка user_exists: {e}")
        return False

async def register_user(tg_id: int, name: str, phone: str, city: str, goal: str):
    try:
        # Проверяем, есть ли уже пользователь
        if await user_exists(tg_id):
            logging.info(f"Пользователь {tg_id} уже существует")
            return
        
        supabase.table("users").insert({
            "tg_id": tg_id,
            "name": name,
            "phone": phone,
            "city": city,
            "goal": goal
        }).execute()
        logging.info(f"✅ Пользователь {tg_id} зарегистрирован")
    except Exception as e:
        logging.error(f"Ошибка register_user: {e}")

async def get_user(tg_id: int) -> Optional[Dict]:
    try:
        response = supabase.table("users").select("*").eq("tg_id", tg_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        logging.error(f"Ошибка get_user: {e}")
        return None

# ========== ПРОГРАММЫ ОБУЧЕНИЯ ==========
async def get_all_programs() -> List[Dict]:
    try:
        response = supabase.table("programs").select("*").order("id").execute()
        logging.info(f"📚 Загружено {len(response.data)} программ")
        return response.data
    except Exception as e:
        logging.error(f"Ошибка get_all_programs: {e}")
        # Возвращаем тестовые данные, если Supabase пуст
        return [
            {"id": 1, "code": "1_4", "name": "1+4 (язык + бакалавриат)", "description": ""},
            {"id": 2, "code": "1_3", "name": "1+3 (язык + бакалавриат ускоренный)", "description": ""},
            {"id": 3, "code": "bach_4", "name": "Бакалавриат 4 года", "description": ""},
            {"id": 4, "code": "mag", "name": "Магистратура 2 года", "description": ""},
            {"id": 5, "code": "lang_1", "name": "1 год языкового курса", "description": ""}
        ]

# ========== УНИВЕРСИТЕТЫ ==========
async def get_universities_by_program(program_id: int) -> List[Dict]:
    try:
        response = supabase.table("universities").select("*").eq("program_id", program_id).execute()
        logging.info(f"🏛 Найдено {len(response.data)} вузов для программы {program_id}")
        return response.data
    except Exception as e:
        logging.error(f"Ошибка get_universities_by_program: {e}")
        # Возвращаем тестовые данные
        return [
            {"id": 1, "name_ru": "Пекинский университет", "name_cn": "北京大学", "city": "Пекин", "program_id": program_id, "description": "Ведущий университет Китая", "price_per_year": 28000, "duration": "4 года"},
            {"id": 2, "name_ru": "Университет Цинхуа", "name_cn": "清华大学", "city": "Пекин", "program_id": program_id, "description": "Технический вуз №1", "price_per_year": 29000, "duration": "4 года"},
            {"id": 3, "name_ru": "Шанхайский университет Цзяо Тун", "name_cn": "上海交通大学", "city": "Шанхай", "program_id": program_id, "description": "Старейший университет Шанхая", "price_per_year": 27000, "duration": "4 года"},
        ]

async def get_universities_by_city(city: str) -> List[Dict]:
    try:
        response = supabase.table("universities").select("*").ilike("city", f"%{city}%").execute()
        return response.data
    except Exception as e:
        logging.error(f"Ошибка get_universities_by_city: {e}")
        return []

async def get_cities_list() -> List[str]:
    try:
        response = supabase.table("universities").select("city").execute()
        cities = list(set([item["city"] for item in response.data]))
        if not cities:
            return ["Пекин", "Шанхай", "Гуанчжоу", "Шэньчжэнь", "Ханчжоу"]
        return sorted(cities)
    except Exception as e:
        logging.error(f"Ошибка get_cities_list: {e}")
        return ["Пекин", "Шанхай", "Гуанчжоу", "Шэньчжэнь", "Ханчжоу"]

# ========== FAQ ==========
async def get_all_faq() -> List[Dict]:
    try:
        response = supabase.table("faq").select("*").execute()
        if not response.data:
            # Тестовые FAQ
            return [
                {"id": 1, "question": "Как зарегистрироваться в WeChat?", "answer": "Скачай WeChat → введи номер → подтверди → привяжи карту"},
                {"id": 2, "question": "Как завести Alipay?", "answer": "Скачай Alipay → выбери International → добавь карту"},
                {"id": 3, "question": "Как получить студенческую визу?", "answer": "Получи JW202 → запишись в посольство → собери документы"},
            ]
        return response.data
    except Exception as e:
        logging.error(f"Ошибка get_all_faq: {e}")
        return []

# ========== ГИД ==========
async def get_guide_articles() -> List[Dict]:
    try:
        response = supabase.table("guide_articles").select("*").order("order_num").execute()
        if not response.data:
            return [
                {"id": 1, "title": "Как открыть банковский счет", "content": "В Китае можно открыть счет в ICBC, Bank of China. Нужен паспорт и виза."},
                {"id": 2, "title": "Мобильная связь", "content": "Операторы: China Mobile, China Unicom. Тарифы от 50 ¥/мес."},
                {"id": 3, "title": "Транспорт", "content": "Метро, автобусы, Didi. Оплата через Alipay."},
            ]
        return response.data
    except Exception as e:
        logging.error(f"Ошибка get_guide_articles: {e}")
        return []
