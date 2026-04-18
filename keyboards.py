from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Главное меню"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🎓 Поступление", callback_data="menu_admission")
    builder.button(text="💱 Обменник валют", callback_data="menu_exchange")
    builder.button(text="🇨🇳 Гид по жизни", callback_data="menu_guide")
    builder.button(text="❓ Вопросы и ответы", callback_data="menu_faq")
    builder.button(text="📞 Связаться с менеджером", callback_data="menu_manager")
    builder.adjust(1)
    return builder.as_markup()

def back_to_main_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="◀ На главную", callback_data="back_main")
    return builder.as_markup()

def remove_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[]], resize_keyboard=True)

def phone_keyboard() -> ReplyKeyboardMarkup:
    button = KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)
    return ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)

def goal_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🎓 Бакалавриат", callback_data="goal_bachelor")
    builder.button(text="🇨🇳 Изучение китайского языка", callback_data="goal_language")
    builder.button(text="📚 Магистратура", callback_data="goal_master")
    builder.button(text="📖 Подготовительные курсы", callback_data="goal_preparation")
    builder.button(text="🏫 Другое", callback_data="goal_other")
    builder.adjust(1)
    return builder.as_markup()

def programs_keyboard(programs: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for prog in programs:
        builder.button(text=prog.get("name", "Неизвестно"), callback_data=f"prog_{prog.get('code', '')}")
    builder.button(text="◀ На главную", callback_data="back_main")
    builder.adjust(1)
    return builder.as_markup()

def city_choice_keyboard(cities: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for city in cities[:12]:
        builder.button(text=f"🏙 {city}", callback_data=f"city_{city}")
    builder.button(text="🔍 Поиск по названию", callback_data="city_search")
    builder.button(text="◀ На главную", callback_data="back_main")
    builder.adjust(2)
    return builder.as_markup()

def university_list_keyboard(universities: list, program_code: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for uni in universities[:20]:
        name = uni.get("name_ru", "Университет")[:35]
        builder.button(text=f"📚 {name}", callback_data=f"uni_{uni.get('id')}")
    builder.button(text="◀ Назад к городам", callback_data=f"prog_{program_code}")
    builder.button(text="🏠 Главное меню", callback_data="back_main")
    builder.adjust(1)
    return builder.as_markup()

def faq_keyboard(faq_list: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for faq in faq_list[:15]:
        question = faq.get("question", "Вопрос")[:45]
        builder.button(text=f"❓ {question}", callback_data=f"faq_{faq.get('id')}")
    builder.button(text="◀ На главную", callback_data="back_main")
    builder.adjust(1)
    return builder.as_markup()

def guide_keyboard(articles: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for article in articles[:10]:
        title = article.get("title", "Статья")[:40]
        builder.button(text=f"📖 {title}", callback_data=f"guide_{article.get('id')}")
    builder.button(text="◀ На главную", callback_data="back_main")
    builder.adjust(1)
    return builder.as_markup()
