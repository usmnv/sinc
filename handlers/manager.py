from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from config import MANAGER_CONTACT, MANAGER_PHONE, MANAGER_WHATSAPP
from keyboards import back_to_main_button

router = Router()

@router.message(F.text == "📞 Связаться с менеджером")
async def manager_menu(message: Message):
    text = (
        "📞 *Связь с менеджером*\n\n"
        f"• Telegram: {MANAGER_CONTACT}\n"
        f"• WhatsApp: {MANAGER_WHATSAPP}\n"
        f"• Телефон: {MANAGER_PHONE}\n\n"
        "📝 Напиши /ask <вопрос> чтобы задать вопрос менеджеру"
    )
    await message.answer(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_to_main_button()
    )

@router.message(Command("ask"))
async def ask_question(message: Message):
    question = message.text.replace("/ask", "").strip()
    if not question:
        await message.answer(
            "❓ *Напиши вопрос после команды:*\n\n"
            "Пример: `/ask Как поступить в Цинхуа?`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    await message.answer(
        f"✅ *Вопрос отправлен!*\n\n"
        f"Твой вопрос: _{question[:100]}_\n\n"
        f"Мы ответим в ближайшее время!",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_to_main_button()
    )
