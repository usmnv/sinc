from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode

from keyboards import guide_keyboard, back_to_main_button, main_menu_keyboard

router = Router()

# Словарь со статьями гида
GUIDE_ARTICLES = {
    "🏦 Как открыть банковский счет": "🏦 *Как открыть банковский счет в Китае*\n\n"
        "1. Выбери банк: ICBC, Bank of China, China Construction Bank\n"
        "2. Возьми с собой паспорт и визу\n"
        "3. Заполни анкету в отделении банка\n"
        "4. Получи банковскую карту (обычно через 30-60 минут)\n\n"
        "💡 *Совет:* Многие банки имеют англоговорящих сотрудников в крупных городах.",
    
    "📱 Мобильная связь": "📱 *Мобильная связь в Китае*\n\n"
        "Основные операторы:\n"
        "• China Mobile - лучший охват\n"
        "• China Unicom - хорош для иностранцев\n"
        "• China Telecom - дешевые тарифы\n\n"
        "💰 *Цены:* Тарифы от 50 ¥/мес (30-50 ГБ трафика)\n\n"
        "📱 SIM-карту можно купить в салонах связи с паспортом.",
    
    "🚇 Транспорт": "🚇 *Транспорт в Китае*\n\n"
        "• Метро - самый удобный способ (2-10 ¥ за поездку)\n"
        "• Автобусы - дешево, но сложно без китайского (1-3 ¥)\n"
        "• Didi (китайский Uber) - удобно, оплата через Alipay\n"
        "• Велосипеды - Hello Bike, Meituan Bike (1.5 ¥ за 30 мин)\n\n"
        "💡 *Совет:* Используй Alipay или WeChat для оплаты проезда!",
    
    "📱 Приложения для жизни": "📱 *Полезные приложения для жизни в Китае*\n\n"
        "• WeChat - общение и оплата всего\n"
        "• Alipay - оплата и переводы\n"
        "• Didi - такси\n"
        "• Meituan - доставка еды\n"
        "• Taobao - онлайн-покупки\n"
        "• Baidu Maps - навигация на китайском\n\n"
        "💡 *Совет:* WeChat и Alipay обязательны для комфортной жизни!"
}

@router.message(F.text == "🇨🇳 Гид по жизни")
async def guide_menu(message: Message):
    await message.answer(
        "🇨🇳 *Гид по жизни в Китае*\n\nВыбери тему:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=guide_keyboard()
    )

@router.message(F.text.in_(GUIDE_ARTICLES.keys()))
async def show_guide_article(message: Message):
    article_text = GUIDE_ARTICLES.get(message.text, "Статья не найдена")
    await message.answer(
        article_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_to_main_button()
    )

@router.message(F.text == "◀ На главную")
async def back_to_main(message: Message):
    await message.answer(
        "🏠 *Главное меню*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu_keyboard()
    )
