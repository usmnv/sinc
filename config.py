import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден!")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL и SUPABASE_KEY обязательны!")

MANAGER_CONTACT = os.getenv("MANAGER_CONTACT", "@china_study_manager")
MANAGER_PHONE = os.getenv("MANAGER_PHONE", "+8612345678901")
MANAGER_WHATSAPP = os.getenv("MANAGER_WHATSAPP", "+8612345678901")

PORT = int(os.environ.get('PORT', 8080))
