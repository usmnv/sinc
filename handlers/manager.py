from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command

from config import MANAGER_CONTACT, MANAGER_PHONE, MANAGER_WHATSAPP
from keyboards import back_to_main_button

router = Router()

@router.callback_query(F.data == "menu_manager")
async def manager_menu(callback: CallbackQuery):
    text = (
        "📞 *Связь с менеджером*\n\n"
        f"• Telegram: {MANAGER_CONTACT}\n"
        f"• WhatsApp: {MANAGER_WHATSAPP}\n"
        f"• Телефон: {MANAGER_PHONE}\n\n"
        "📝 Напиши /ask <вопрос> чтобы задать вопрос менеджеру"
    )
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=back_to_main_button())
    await callback.answer()

@router.message(Command("ask"))
async def ask_question(message: Message):
    question = message.text.replace("/ask", "").strip()
    if not question:
        await message.answer("❓ Напиши вопрос после команды: /ask Как поступить в Цинхуа?")
        return
    
    await message.answer(
        f"✅ *Вопрос отправлен!*\n\nТвой вопрос: _{question[:100]}_\n\nМы ответим в ближайшее время!",
        parse_mode="Markdown"
    )
