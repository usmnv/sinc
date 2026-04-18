from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode

from keyboards import faq_keyboard, back_to_main_button, main_menu_keyboard

router = Router()

# Словарь с ответами на вопросы
FAQ_ANSWERS = {
    "❓ Как зарегистрироваться в WeChat?": "❓ *Как зарегистрироваться в WeChat*\n\n"
        "1. Скачай приложение WeChat из App Store/Google Play\n"
        "2. Нажми 'Регистрация'\n"
        "3. Введи номер телефона\n"
        "4. Подтверди код из SMS\n"
        "5. Придумай пароль\n\n"
        "⚠️ *Важно:* Если требуется приглашение от пользователя в Китае - обратись к менеджеру!",
    
    "❓ Как завести Alipay?": "❓ *Как завести Alipay*\n\n"
        "1. Скачай приложение Alipay\n"
        "2. Выбери 'International version'\n"
        "3. Нажми 'Sign Up'\n"
        "4. Введи номер телефона\n"
        "5. Добавь банковскую карту (Visa/Mastercard)\n"
        "6. Пройди верификацию по паспорту\n\n"
        "💡 *Совет:* Alipay работает с иностранными картами!",
    
    "❓ Как получить студенческую визу?": "❓ *Как получить студенческую визу (X1/X2)*\n\n"
        "1. Получи приглашение от университета (форма JW202)\n"
        "2. Запишись на подачу документов в посольство Китая\n"
        "3. Собери пакет документов:\n"
        "   - Загранпаспорт (срок действия > 6 месяцев)\n"
        "   - Фото 3.5x4.5 см\n"
        "   - Приглашение JW202\n"
        "   - Медицинская справка\n"
        "   - Финансовые гарантии\n"
        "4. Оплати визовый сбор\n"
        "5. Жди решения (обычно 5-10 дней)\n\n"
        "📞 *Нужна помощь?* Свяжись с менеджером!",
    
    "❓ Сколько стоит жизнь в Китае?": "❓ *Стоимость жизни в Китае*\n\n"
        "💰 *Расходы в месяц:*\n\n"
        "🏙 *Пекин / Шанхай:* 4000-7000 ¥\n"
        "🌆 *Другие города:* 2500-4500 ¥\n\n"
        "Из чего складывается:\n"
        "• Общежитие: 1000-2000 ¥\n"
        "• Еда: 1000-2000 ¥\n"
        "• Транспорт: 200-300 ¥\n"
        "• Связь: 50-100 ¥\n"
        "• Прочее: 500-1000 ¥\n\n"
        "💡 *Совет:* Готовь еду сам — это экономит до 50% бюджета!"
}

@router.message(F.text == "❓ Вопросы и ответы")
async def faq_menu(message: Message):
    await message.answer(
        "❓ *Часто задаваемые вопросы*\n\nВыбери вопрос:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=faq_keyboard()
    )

@router.message(F.text.in_(FAQ_ANSWERS.keys()))
async def show_faq_answer(message: Message):
    answer = FAQ_ANSWERS.get(message.text, "Ответ не найден")
    await message.answer(
        answer,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_to_main_button()
    )
