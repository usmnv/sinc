from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode

from database import get_exchange_rate_from_db
from keyboards import back_to_main_button

router = Router()

@router.message(F.text == "💱 Обменник валют")
async def exchange_menu(message: Message):
    rate = await get_exchange_rate_from_db()
    
    text = (
        "💱 *Актуальный курс валют*\n\n"
        f"🇨🇳 1 Китайский юань (CNY) =\n\n"
        f"💵 {rate.get('cny_to_usd', 0.14)} USD\n"
        f"🇷🇺 {rate.get('cny_to_rub', 12.5)} RUB\n"
        f"🇰🇿 {rate.get('cny_to_kzt', 62.0)} KZT\n\n"
        f"🕐 Обновлено: {rate.get('updated_at', 'неизвестно')}\n\n"
        "💡 *Совет:* Лучше менять валюту в Китае в банках"
    )
    
    if rate.get("note"):
        text += f"\n\n⚠️ {rate['note']}"
    
    await message.answer(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_to_main_button()
    )
