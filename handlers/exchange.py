from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from database import get_exchange_rate_from_db
from keyboards import back_to_main_button, exchange_calculator_keyboard, exchange_amount_keyboard
from states import ExchangeState
from config import MANAGER_CONTACT, MANAGER_PHONE, MANAGER_WHATSAPP

router = Router()

# Словарь валют
CURRENCIES = {
    "RUB": "🇷🇺 Российский рубль",
    "USD": "💵 Доллар США",
    "KZT": "🇰🇿 Казахстанский тенге",
    "TJS": "🇹🇯 Таджикский сомони",
    "UZS": "🇺🇿 Узбекский сум"
}

@router.message(F.text == "💱 Обменник валют")
async def exchange_menu(message: Message):
    rate = await get_exchange_rate_from_db()
    
    # Показываем источник курса
    source_text = ""
    if rate.get("source") == "база данных":
        source_text = "📊 *Курс из базы данных* (обновлен менеджером)"
    elif rate.get("source") == "API":
        source_text = "🌐 *Курс из API* (автообновление)"
    elif rate.get("source") == "кэш БД":
        source_text = "💾 *Курс из кэша* (API временно недоступен)"
    else:
        source_text = "⚠️ *Курсы по умолчанию* (требуется обновление)"
    
    text = (
        "💱 *Курс валют на сегодня*\n\n"
        f"{source_text}\n\n"
        f"🇨🇳 1 Китайский юань (CNY) =\n\n"
        f"🇷🇺 {rate.get('cny_to_rub', 12.5)} RUB\n"
        f"💵 {rate.get('cny_to_usd', 0.14)} USD\n"
        f"🇰🇿 {rate.get('cny_to_kzt', 62.0)} KZT\n"
        f"🇹🇯 {rate.get('cny_to_tjs', 1.5)} TJS\n"
        f"🇺🇿 {rate.get('cny_to_uzs', 1700)} UZS\n\n"
        f"🕐 Обновлено: {rate.get('updated_at', 'неизвестно')}\n\n"
        "📊 *Выбери действие:*"
    )
    
    await message.answer(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=exchange_calculator_keyboard()
    )

@router.callback_query(F.data == "exchange_calculator")
async def start_calculator(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🧮 *Калькулятор валют*\n\n"
        "Выбери валюту, из которой хочешь конвертировать:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=exchange_amount_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("exchange_from_"))
async def select_from_currency(callback: CallbackQuery, state: FSMContext):
    from_currency = callback.data.split("_")[2]
    await state.update_data(from_currency=from_currency)
    
    text = (
        "🧮 *Калькулятор валют*\n\n"
        f"Выбрано: {CURRENCIES.get(from_currency, from_currency)}\n\n"
        "Теперь выбери валюту, в которую хочешь конвертировать:"
    )
    
    await callback.message.edit_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=exchange_amount_keyboard(from_currency=True)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("exchange_to_"))
async def select_to_currency(callback: CallbackQuery, state: FSMContext):
    to_currency = callback.data.split("_")[2]
    data = await state.get_data()
    from_currency = data.get("from_currency")
    
    if not from_currency:
        await callback.message.edit_text(
            "❌ Ошибка. Начни сначала: /start",
            reply_markup=back_to_main_button()
        )
        await callback.answer()
        return
    
    await state.update_data(to_currency=to_currency)
    
    await callback.message.edit_text(
        "🧮 *Калькулятор валют*\n\n"
        f"Конвертация: {CURRENCIES.get(from_currency, from_currency)} → {CURRENCIES.get(to_currency, to_currency)}\n\n"
        "💰 *Введи сумму* (только число):",
        parse_mode=ParseMode.MARKDOWN
    )
    await state.set_state(ExchangeState.waiting_amount)
    await callback.answer()

@router.message(StateFilter(ExchangeState.waiting_amount))
async def calculate_exchange(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(",", ".").strip())
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer(
            "❌ *Пожалуйста, введи корректное число* (например: 100, 5000, 10000)",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    data = await state.get_data()
    from_currency = data.get("from_currency")
    to_currency = data.get("to_currency")
    
    if not from_currency or not to_currency:
        await message.answer(
            "❌ Ошибка. Начни сначала: /start",
            reply_markup=back_to_main_button()
        )
        await state.clear()
        return
    
    rate = await get_exchange_rate_from_db()
    
    # Сначала конвертируем в CNY
    cny_amount = amount / rate.get(f"cny_to_{from_currency.lower()}", 1)
    # Потом из CNY в целевую валюту
    result = cny_amount * rate.get(f"cny_to_{to_currency.lower()}", 1)
    
    # Форматируем результат
    if to_currency in ["UZS", "KZT"]:
        result_text = f"{result:,.0f}".replace(",", " ")
    else:
        result_text = f"{result:.2f}"
    
    if from_currency in ["UZS", "KZT"]:
        amount_text = f"{amount:,.0f}".replace(",", " ")
    else:
        amount_text = f"{amount:.2f}"
    
    text = (
        "🧮 *Результат конвертации*\n\n"
        f"💰 {amount_text} {from_currency} = *{result_text} {to_currency}*\n\n"
        f"📊 Курс: 1 CNY = {rate.get(f'cny_to_{from_currency.lower()}', 1)} {from_currency}\n"
        f"📊 Курс: 1 CNY = {rate.get(f'cny_to_{to_currency.lower()}', 1)} {to_currency}\n\n"
        "➖➖➖➖➖➖➖➖➖➖\n\n"
        "🔄 Хочешь сделать новый расчет? Нажми /start"
    )
    
    await message.answer(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_to_main_button()
    )
    await state.clear()

@router.callback_query(F.data == "exchange_contact_manager")
async def contact_manager_for_exchange(callback: CallbackQuery):
    text = (
        "💱 *Обмен валют*\n\n"
        "Для точного расчета и лучшего курса рекомендуем обратиться к менеджеру:\n\n"
        f"📞 *Telegram:* {MANAGER_CONTACT}\n"
        f"📞 *WhatsApp:* {MANAGER_WHATSAPP}\n"
        f"📞 *Телефон:* {MANAGER_PHONE}\n\n"
        "Менеджер поможет:\n"
        "• Узнать актуальный курс\n"
        "• Провести обмен по лучшему курсу\n"
        "• Ответить на вопросы"
    )
    
    await callback.message.edit_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_to_main_button()
    )
    await callback.answer()

@router.callback_query(F.data == "exchange_back")
async def back_to_exchange_menu(callback: CallbackQuery):
    rate = await get_exchange_rate_from_db()
    
    source_text = ""
    if rate.get("source") == "база данных":
        source_text = "📊 *Курс из базы данных* (обновлен менеджером)"
    elif rate.get("source") == "API":
        source_text = "🌐 *Курс из API* (автообновление)"
    elif rate.get("source") == "кэш БД":
        source_text = "💾 *Курс из кэша* (API временно недоступен)"
    else:
        source_text = "⚠️ *Курсы по умолчанию* (требуется обновление)"
    
    text = (
        "💱 *Курс валют на сегодня*\n\n"
        f"{source_text}\n\n"
        f"🇨🇳 1 Китайский юань (CNY) =\n\n"
        f"🇷🇺 {rate.get('cny_to_rub', 12.5)} RUB\n"
        f"💵 {rate.get('cny_to_usd', 0.14)} USD\n"
        f"🇰🇿 {rate.get('cny_to_kzt', 62.0)} KZT\n"
        f"🇹🇯 {rate.get('cny_to_tjs', 1.5)} TJS\n"
        f"🇺🇿 {rate.get('cny_to_uzs', 1700)} UZS\n\n"
        f"🕐 Обновлено: {rate.get('updated_at', 'неизвестно')}\n\n"
        "📊 *Выбери действие:*"
    )
    
    await callback.message.edit_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=exchange_calculator_keyboard()
    )
    await callback.answer()
