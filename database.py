from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY
from typing import List, Dict, Optional

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ========== ПОЛЬЗОВАТЕЛИ ==========
async def user_exists(tg_id: int) -> bool:
    try:
        response = supabase.table("users").select("id").eq("tg_id", tg_id).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Ошибка user_exists: {e}")
        return False

async def register_user(tg_id: int, name: str, phone: str, city: str, goal: str):
    try:
        supabase.table("users").insert({
            "tg_id": tg_id,
            "name": name,
            "phone": phone,
            "city": city,
            "goal": goal
        }).execute()
    except Exception as e:
        print(f"Ошибка register_user: {e}")

async def get_user(tg_id: int) -> Optional[Dict]:
    try:
        response = supabase.table("users").select("*").eq("tg_id", tg_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Ошибка get_user: {e}")
        return None

# ========== ПРОГРАММЫ ==========
async def get_all_programs() -> List[Dict]:
    try:
        response = supabase.table("programs").select("*").order("id").execute()
        return response.data
    except Exception as e:
        print(f"Ошибка get_all_programs: {e}")
        return []

# ========== УНИВЕРСИТЕТЫ ==========
async def get_universities_by_program(program_id: int) -> List[Dict]:
    try:
        response = supabase.table("universities").select("*").eq("program_id", program_id).execute()
        return response.data
    except Exception as e:
        print(f"Ошибка get_universities_by_program: {e}")
        return []

async def get_universities_by_city(city: str) -> List[Dict]:
    try:
        response = supabase.table("universities").select("*").ilike("city", f"%{city}%").execute()
        return response.data
    except Exception as e:
        print(f"Ошибка get_universities_by_city: {e}")
        return []

async def get_cities_list() -> List[str]:
    try:
        response = supabase.table("universities").select("city").execute()
        cities = list(set([item["city"] for item in response.data]))
        return sorted(cities)
    except Exception as e:
        print(f"Ошибка get_cities_list: {e}")
        return []

# ========== FAQ ==========
async def get_all_faq() -> List[Dict]:
    try:
        response = supabase.table("faq").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Ошибка get_all_faq: {e}")
        return []

# ========== ГИД ==========
async def get_guide_articles() -> List[Dict]:
    try:
        response = supabase.table("guide_articles").select("*").order("order_num").execute()
        return response.data
    except Exception as e:
        print(f"Ошибка get_guide_articles: {e}")
        return []
