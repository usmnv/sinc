from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Главное меню - ReplyKeyboard кнопки внизу"""
    buttons = [
        [KeyboardButton(text="🎓 Поступление")],
        [KeyboardButton(text="💱 Обменник валют")],
        [KeyboardButton(text="🇨🇳 Гид по жизни")],
        [KeyboardButton(text="❓ Вопросы и ответы")],
        [KeyboardButton(text="📞 Связаться с менеджером")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def phone_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для отправки номера телефона"""
    button = KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)
    return ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)

def goal_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура выбора цели"""
    buttons = [
        [KeyboardButton(text="🎓 Бакалавриат")],
        [KeyboardButton(text="🇨🇳 Изучение китайского языка")],
        [KeyboardButton(text="📚 Магистратура")],
        [KeyboardButton(text="📖 Подготовительные курсы")],
        [KeyboardButton(text="🏫 Другое")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def programs_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура выбора программы обучения"""
    buttons = [
        [KeyboardButton(text="1+4 (язык + бакалавриат")],
        [KeyboardButton(text="1+3 (язык + бакалавриат ускоренный)")],
        [KeyboardButton(text="Бакалавриат 4 года")],
        [KeyboardButton(text="Магистратура 2 года")],
        [KeyboardButton(text="1 год языкового курса")],
        [KeyboardButton(text="◀ На главную")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def city_choice_keyboard(cities: list) -> ReplyKeyboardMarkup:
    """Клавиатура выбора города"""
    buttons = []
    for city in cities[:8]:
        buttons.append([KeyboardButton(text=city)])
    buttons.append([KeyboardButton(text="🔍 Поиск по названию")])
    buttons.append([KeyboardButton(text="◀ На главную")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def university_list_keyboard(universities: list) -> ReplyKeyboardMarkup:
    """Клавиатура выбора университета"""
    buttons = []
    for uni in universities[:10]:
        buttons.append([KeyboardButton(text=f"{uni.get('name_ru', 'Университет')[:30]}")])
    buttons.append([KeyboardButton(text="◀ Назад к городам")])
    buttons.append([KeyboardButton(text="🏠 Главное меню")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def back_to_main_button() -> ReplyKeyboardMarkup:
    """Кнопка возврата в главное меню"""
    buttons = [[KeyboardButton(text="◀ На главную")]]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def remove_keyboard() -> ReplyKeyboardRemove:
    """Убирает клавиатуру"""
    return ReplyKeyboardRemove()
