from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter

from database import get_exchange_rate_from_db
from keyboards import back_to_main_button, main_menu_keyboard
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

# Временное хранилище выбора пользователя
user_currency_choice = {}

@router.message(F.text == "💱 Обменник валют")
async def exchange_menu(message: Message):
    rate = await get_exchange_rate_from_db()
    
    source_text = ""
    if rate.get("source") == "база данных":
        source_text = "📊 Курс из базы данных (обновлен менеджером)"
    elif rate.get("source") == "API":
        source_text = "🌐 Курс из API (автообновление)"
    elif rate.get("source") == "кэш БД":
        source_text = "💾 Курс из кэша (API временно недоступен)"
    else:
        source_text = "⚠️ Курсы по умолчанию (требуется обновление)"
    
    text = (
        f"💱 *Курс валют на сегодня*\n\n"
        f"{source_text}\n\n"
        f"🇨🇳 1 Китайский юань (CNY) =\n\n"
        f"🇷🇺 {rate.get('cny_to_rub', 12.5)} RUB\n"
        f"💵 {rate.get('cny_to_usd', 0.14)} USD\n"
        f"🇰🇿 {rate.get('cny_to_kzt', 62.0)} KZT\n"
        f"🇹🇯 {rate.get('cny_to_tjs', 1.5)} TJS\n"
        f"🇺🇿 {rate.get('cny_to_uzs', 1700)} UZS\n\n"
        f"🕐 Обновлено: {rate.get('updated_at', 'неизвестно')}\n\n"
        "📊 *Выбери действие:*\n\n"
        "➡️ *Калькулятор* - для конвертации валют\n"
        "➡️ *Связаться с менеджером* - для обмена по лучшему курсу"
    )
    
    # Отправляем сообщение с Reply клавиатурой
    await message.answer(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=exchange_reply_keyboard()
    )

def exchange_reply_keyboard() -> ReplyKeyboardMarkup:
    """Reply клавиатура для обменника"""
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    buttons = [
        [KeyboardButton(text="🧮 Запустить калькулятор")],
        [KeyboardButton(text="📞 Связаться с менеджером")],
        [KeyboardButton(text="◀ На главную")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def currency_from_keyboard() -> ReplyKeyboardMarkup:
    """Reply клавиатура выбора валюты ИЗ которой конвертируем"""
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    buttons = [
        [KeyboardButton(text="🇷🇺 RUB"), KeyboardButton(text="💵 USD")],
        [KeyboardButton(text="🇰🇿 KZT"), KeyboardButton(text="🇹🇯 TJS")],
        [KeyboardButton(text="🇺🇿 UZS")],
        [KeyboardButton(text="◀ Назад к курсам")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def currency_to_keyboard() -> ReplyKeyboardMarkup:
    """Reply клавиатура выбора валюты В которую конвертируем"""
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    buttons = [
        [KeyboardButton(text="🇷🇺 RUB"), KeyboardButton(text="💵 USD")],
        [KeyboardButton(text="🇰🇿 KZT"), KeyboardButton(text="🇹🇯 TJS")],
        [KeyboardButton(text="🇺🇿 UZS")],
        [KeyboardButton(text="◀ Назад к курсам")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@router.message(F.text == "🧮 Запустить калькулятор")
async def start_calculator(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_currency_choice[user_id] = {}
    
    await message.answer(
        "🧮 *Калькулятор валют*\n\n"
        "Выбери валюту, *из которой* хочешь конвертировать:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=currency_from_keyboard()
    )
    await state.set_state(ExchangeState.waiting_from_currency)

@router.message(ExchangeState.waiting_from_currency)
async def select_from_currency(message: Message, state: FSMContext):
    text = message.text.strip()
    user_id = message.from_user.id
    
    # Маппинг эмодзи в коды валют
    currency_map = {
        "🇷🇺 RUB": "RUB",
        "💵 USD": "USD", 
        "🇰🇿 KZT": "KZT",
        "🇹🇯 TJS": "TJS",
        "🇺🇿 UZS": "UZS"
    }
    
    if text not in currency_map:
        await message.answer(
            "❌ Пожалуйста, выбери валюту из списка кнопок.",
            reply_markup=currency_from_keyboard()
        )
        return
    
    from_currency = currency_map[text]
    
    if user_id not in user_currency_choice:
        user_currency_choice[user_id] = {}
    user_currency_choice[user_id]["from"] = from_currency
    
    await message.answer(
        f"✅ Выбрано: {text}\n\n"
        "Теперь выбери валюту, *в которую* хочешь конвертировать:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=currency_to_keyboard()
    )
    await state.set_state(ExchangeState.waiting_to_currency)

@router.message(ExchangeState.waiting_to_currency)
async def select_to_currency(message: Message, state: FSMContext):
    text = message.text.strip()
    user_id = message.from_user.id
    
    currency_map = {
        "🇷🇺 RUB": "RUB",
        "💵 USD": "USD",
        "🇰🇿 KZT": "KZT",
        "🇹🇯 TJS": "TJS",
        "🇺🇿 UZS": "UZS"
    }
    
    if text not in currency_map:
        await message.answer(
            "❌ Пожалуйста, выбери валюту из списка кнопок.",
            reply_markup=currency_to_keyboard()
        )
        return
    
    to_currency = currency_map[text]
    from_currency = user_currency_choice.get(user_id, {}).get("from")
    
    if not from_currency:
        await message.answer(
            "❌ Ошибка. Начни сначала: /start",
            reply_markup=main_menu_keyboard()
        )
        await state.clear()
        return
    
    user_currency_choice[user_id]["to"] = to_currency
    
    await message.answer(
        f"🧮 *Калькулятор валют*\n\n"
        f"Конвертация: {from_currency} → {to_currency}\n\n"
        "💰 *Введи сумму* (только число):\n\n"
        "Например: 100, 5000, 10000",
        parse_mode=ParseMode.MARKDOWN
    )
    await state.set_state(ExchangeState.waiting_amount)

@router.message(StateFilter(ExchangeState.waiting_amount))
async def calculate_exchange(message: Message, state: FSMContext):
    user_id = message.from_user.id
    
    # Парсим сумму
    try:
        amount_text = message.text.strip().replace(",", ".").replace(" ", "")
        amount = float(amount_text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer(
            "❌ *Пожалуйста, введи корректное число*\n\n"
            "Примеры: 100, 5000, 10000.50",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    from_currency = user_currency_choice.get(user_id, {}).get("from")
    to_currency = user_currency_choice.get(user_id, {}).get("to")
    
    if not from_currency or not to_currency:
        await message.answer(
            "❌ Ошибка. Начни сначала: /start",
            reply_markup=main_menu_keyboard()
        )
        await state.clear()
        return
    
    rate = await get_exchange_rate_from_db()
    
    # Получаем курсы
    from_rate = rate.get(f"cny_to_{from_currency.lower()}", 1)
    to_rate = rate.get(f"cny_to_{to_currency.lower()}", 1)
    
    # Конвертируем: сумма -> CNY -> целевая валюта
    cny_amount = amount / from_rate
    result = cny_amount * to_rate
    
    # Форматируем результат
    if to_currency in ["UZS", "KZT"]:
        result_text = f"{result:,.0f}".replace(",", " ")
    else:
        result_text = f"{result:.2f}"
    
    if from_currency in ["UZS", "KZT"]:
        amount_text_formatted = f"{amount:,.0f}".replace(",", " ")
    else:
        amount_text_formatted = f"{amount:.2f}"
    
    text = (
        "🧮 *Результат конвертации*\n\n"
        f"💰 {amount_text_formatted} {from_currency} = *{result_text} {to_currency}*\n\n"
        f"📊 Курс: 1 CNY = {from_rate} {from_currency}\n"
        f"📊 Курс: 1 CNY = {to_rate} {to_currency}\n\n"
        "➖➖➖➖➖➖➖➖➖➖\n\n"
        "🔄 *Хочешь сделать новый расчет?*\n"
        "Нажми /start или выбери '🧮 Запустить калькулятор' снова"
    )
    
    # Очищаем состояние
    await state.clear()
    if user_id in user_currency_choice:
        del user_currency_choice[user_id]
    
    # Отправляем результат
    await message.answer(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=exchange_reply_keyboard()
    )

@router.message(F.text == "📞 Связаться с менеджером")
async def contact_manager_for_exchange(message: Message):
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
    
    await message.answer(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=exchange_reply_keyboard()
    )

@router.message(F.text == "◀ Назад к курсам")
async def back_to_exchange_menu(message: Message):
    rate = await get_exchange_rate_from_db()
    
    source_text = ""
    if rate.get("source") == "база данных":
        source_text = "📊 Курс из базы данных (обновлен менеджером)"
    elif rate.get("source") == "API":
        source_text = "🌐 Курс из API (автообновление)"
    elif rate.get("source") == "кэш БД":
        source_text = "💾 Курс из кэша (API временно недоступен)"
    else:
        source_text = "⚠️ Курсы по умолчанию (требуется обновление)"
    
    text = (
        f"💱 *Курс валют на сегодня*\n\n"
        f"{source_text}\n\n"
        f"🇨🇳 1 Китайский юань (CNY) =\n\n"
        f"🇷🇺 {rate.get('cny_to_rub', 12.5)} RUB\n"
        f"💵 {rate.get('cny_to_usd', 0.14)} USD\n"
        f"🇰🇿 {rate.get('cny_to_kzt', 62.0)} KZT\n"
        f"🇹🇯 {rate.get('cny_to_tjs', 1.5)} TJS\n"
        f"🇺🇿 {rate.get('cny_to_uzs', 1700)} UZS\n\n"
        f"🕐 Обновлено: {rate.get('updated_at', 'неизвестно')}\n\n"
        "📊 *Выбери действие:*\n\n"
        "➡️ *Калькулятор* - для конвертации валют\n"
        "➡️ *Связаться с менеджером* - для обмена по лучшему курсу"
    )
    
    await message.answer(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=exchange_reply_keyboard()
    )
