from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Главное меню"""
    buttons = [
        [KeyboardButton(text="🎓 Поступление")],
        [KeyboardButton(text="💱 Обменник валют")],
        [KeyboardButton(text="🇨🇳 Гид по жизни")],
        [KeyboardButton(text="❓ Вопросы и ответы")],
        [KeyboardButton(text="📞 Связаться с менеджером")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def phone_keyboard() -> ReplyKeyboardMarkup:
    button = KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)
    return ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)

def goal_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="🎓 Бакалавриат")],
        [KeyboardButton(text="🇨🇳 Изучение китайского языка")],
        [KeyboardButton(text="📚 Магистратура")],
        [KeyboardButton(text="📖 Подготовительные курсы")],
        [KeyboardButton(text="🏫 Другое")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def programs_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="1+4 (язык + бакалавриат)")],
        [KeyboardButton(text="1+3 (язык + бакалавриат ускоренный)")],
        [KeyboardButton(text="Бакалавриат 4 года")],
        [KeyboardButton(text="Магистратура 2 года")],
        [KeyboardButton(text="1 год языкового курса")],
        [KeyboardButton(text="◀ На главную")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def city_choice_keyboard(cities: list) -> ReplyKeyboardMarkup:
    buttons = []
    for city in cities[:12]:
        buttons.append([KeyboardButton(text=city)])
    buttons.append([KeyboardButton(text="🔍 Поиск по названию")])
    buttons.append([KeyboardButton(text="◀ На главную")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def guide_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="🏦 Как открыть банковский счет")],
        [KeyboardButton(text="📱 Мобильная связь")],
        [KeyboardButton(text="🚇 Транспорт")],
        [KeyboardButton(text="📱 Приложения для жизни")],
        [KeyboardButton(text="◀ На главную")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def faq_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="❓ Как зарегистрироваться в WeChat?")],
        [KeyboardButton(text="❓ Как завести Alipay?")],
        [KeyboardButton(text="❓ Как получить студенческую визу?")],
        [KeyboardButton(text="❓ Сколько стоит жизнь в Китае?")],
        [KeyboardButton(text="◀ На главную")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def back_to_main_button() -> ReplyKeyboardMarkup:
    buttons = [[KeyboardButton(text="◀ На главную")]]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
def create_city_keyboard(cities: list) -> ReplyKeyboardMarkup:
    """Динамическая клавиатура выбора города из списка БД"""
    buttons = []
    for city in cities[:15]:
        buttons.append([KeyboardButton(text=city)])
    buttons.append([KeyboardButton(text="🔍 Поиск по названию")])
    buttons.append([KeyboardButton(text="◀ На главную")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def exchange_calculator_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для обменника валют"""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    
    builder = InlineKeyboardBuilder()
    builder.button(text="🧮 Калькулятор валют", callback_data="exchange_calculator")
    builder.button(text="📞 Связаться с менеджером", callback_data="exchange_contact_manager")
    builder.button(text="◀ На главную", callback_data="back_main")
    builder.adjust(1)
    return builder.as_markup()

def exchange_amount_keyboard(from_currency: bool = False) -> InlineKeyboardMarkup:
    """Клавиатура выбора валют для калькулятора"""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    
    builder = InlineKeyboardBuilder()
    
    if from_currency:
        builder.button(text="🇷🇺 RUB", callback_data="exchange_to_RUB")
        builder.button(text="💵 USD", callback_data="exchange_to_USD")
        builder.button(text="🇰🇿 KZT", callback_data="exchange_to_KZT")
        builder.button(text="🇹🇯 TJS", callback_data="exchange_to_TJS")
        builder.button(text="🇺🇿 UZS", callback_data="exchange_to_UZS")
    else:
        builder.button(text="🇷🇺 RUB", callback_data="exchange_from_RUB")
        builder.button(text="💵 USD", callback_data="exchange_from_USD")
        builder.button(text="🇰🇿 KZT", callback_data="exchange_from_KZT")
        builder.button(text="🇹🇯 TJS", callback_data="exchange_from_TJS")
        builder.button(text="🇺🇿 UZS", callback_data="exchange_from_UZS")
    
    builder.button(text="◀ Назад", callback_data="exchange_back")
    builder.adjust(1)
    return builder.as_markup()
