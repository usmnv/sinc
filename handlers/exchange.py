from aiogram import Router, F
from aiogram.types import CallbackQuery
import aiohttp
from datetime import datetime

from keyboards import back_to_main_button

router = Router()

@router.callback_query(F.data == "menu_exchange")
async def exchange_menu(callback: CallbackQuery):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.exchangerate-api.com/v4/latest/CNY") as resp:
                data = await resp.json()
                usd = data["rates"].get("USD", 0.138)
                rub = data["rates"].get("RUB", 12.5)
                kzt = data["rates"].get("KZT", 62.0)
                
                text = (
                    "💱 *Актуальный курс валют*\n\n"
                    f"🇨🇳 1 Китайский юань (CNY) =\n\n"
                    f"💵 {round(usd, 4)} USD\n"
                    f"🇷🇺 {round(rub, 2)} RUB\n"
                    f"🇰🇿 {round(kzt, 2)} KZT\n\n"
                    f"🕐 Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
                    "💡 *Совет:* Лучше менять валюту в Китае в банках"
                )
    except:
        text = "💱 *Курс валют*\n\n1 CNY ≈ 0.14 USD | 12.5 RUB | 62 KZT\n\n⚠️ Данные примерные"
    
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=back_to_main_button())
    await callback.answer()
