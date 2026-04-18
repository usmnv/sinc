from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from database import (
    get_all_programs, get_universities_by_program,
    get_universities_by_city, get_cities_list
)
from keyboards import (
    programs_keyboard, city_choice_keyboard,
    back_to_main_button, main_menu_keyboard, remove_keyboard
)
from states import CitySearch

router = Router()

# Соответствие текстов программ ID
PROGRAM_TEXT_TO_ID = {
    "1+4 (язык + бакалавриат)": 1,
    "1+3 (язык + бакалавриат ускоренный)": 2,
    "Бакалавриат 4 года": 3,
    "Магистратура 2 года": 4,
    "1 год языкового курса": 5,
}

@router.message(F.text == "🎓 Поступление")
async def admission_menu(message: Message, state: FSMContext):
    await state.update_data(program_code=None, program_id=None)
    await message.answer(
        "🎓 *Выбери программу обучения:*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=programs_keyboard()
    )

@router.message(F.text.in_([
    "1+4 (язык + бакалавриат)",
    "1+3 (язык + бакалавриат ускоренный)",
    "Бакалавриат 4 года",
    "Магистратура 2 года",
    "1 год языкового курса"
]))
async def program_selected(message: Message, state: FSMContext):
    program_text = message.text
    program_id = PROGRAM_TEXT_TO_ID.get(program_text)
    
    if not program_id:
        await message.answer("❌ Программа не найдена")
        return
    
    # Сохраняем выбранную программу
    await state.update_data(program_code=str(program_id), program_id=program_id)
    
    cities = await get_cities_list()
    
    if not cities:
        await message.answer("❌ Список городов пуст. Добавьте университеты в Supabase.")
        return
    
    await message.answer(
        f"📍 *Выбери город для программы:*\n{program_text}",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=city_choice_keyboard(cities)
    )

@router.message(F.text == "🔍 Поиск по названию")
async def search_city_prompt(message: Message, state: FSMContext):
    await message.answer(
        "🔍 *Введи название города:*\n\nНапример: Пекин, Шанхай, Гуанчжоу",
        parse_mode=ParseMode.MARKDOWN
    )
    await state.set_state(CitySearch.waiting_city_name)

@router.message(F.text == "◀ На главную")
async def back_to_main(message: Message):
    await message.answer(
        "🏠 *Главное меню*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu_keyboard()
    )

@router.message(F.text)  # Обрабатываем выбор города (Пекин, Шанхай и т.д.)
async def city_selected(message: Message, state: FSMContext):
    city = message.text.strip()
    
    # Проверяем, что это не команда и не кнопка навигации
    if city in ["🎓 Поступление", "💱 Обменник валют", "🇨🇳 Гид по жизни", "❓ Вопросы и ответы", "📞 Связаться с менеджером"]:
        return
    
    data = await state.get_data()
    program_id = data.get("program_id")
    program_text = data.get("program_text")
    
    if not program_id:
        await message.answer("❌ Сначала выбери программу обучения.")
        return
    
    # Получаем университеты по программе
    universities = await get_universities_by_program(program_id)
    
    # Фильтруем по городу
    filtered = [u for u in universities if u.get("city", "").lower() == city.lower()]
    
    if not filtered:
        await message.answer(
            f"❌ В городе {city} нет вузов по выбранной программе.\n\n"
            f"Попробуй выбрать другой город.",
            reply_markup=back_to_main_button()
        )
        return
    
    # Показываем каждый университет отдельно
    await message.answer(
        f"🏛 *Найдено {len(filtered)} университетов в городе {city}:*\n",
        parse_mode=ParseMode.MARKDOWN
    )
    
    for uni in filtered:
        text = (
            f"🏛 *{uni.get('name_ru', 'Название не указано')}*\n"
            f"📖 *Китайское название:* {uni.get('name_cn', 'Не указано')}\n"
            f"📍 *Город:* {uni.get('city', 'Не указан')}\n"
            f"📚 *Программа:* {uni.get('duration', 'Не указана')}\n"
            f"💰 *Стоимость:* {uni.get('price_per_year', 'Уточняйте')} ¥/год\n\n"
            f"📝 *Описание:*\n{uni.get('description', 'Нет описания')}"
        )
        await message.answer(text, parse_mode=ParseMode.MARKDOWN)
    
    await message.answer(
        "🔍 *Хочешь выбрать другой город?*\nНажми /start для возврата в меню",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_to_main_button()
    )
    
    await state.clear()

@router.message(CitySearch.waiting_city_name)
async def handle_city_search(message: Message, state: FSMContext):
    city = message.text.strip()
    
    data = await state.get_data()
    program_id = data.get("program_id")
    
    if not program_id:
        await message.answer("❌ Сначала выбери программу обучения.")
        await state.clear()
        return
    
    universities = await get_universities_by_city(city)
    
    if not universities:
        await message.answer(
            f"❌ Город '{city}' не найден.\n\nПопробуй другой город.",
            reply_markup=back_to_main_button()
        )
    else:
        await message.answer(
            f"🔍 Найдено {len(universities)} вузов в городе {city}:",
            parse_mode=ParseMode.MARKDOWN
        )
        for uni in universities:
            text = (
                f"🏛 *{uni.get('name_ru', 'Название не указано')}*\n"
                f"📍 *Город:* {uni.get('city', 'Не указан')}\n"
                f"📚 *Программа:* {uni.get('duration', 'Не указана')}\n"
                f"💰 *Стоимость:* {uni.get('price_per_year', 'Уточняйте')} ¥/год\n\n"
                f"📝 *Описание:*\n{uni.get('description', 'Нет описания')}"
            )
            await message.answer(text, parse_mode=ParseMode.MARKDOWN)
        await message.answer(
            "Нажми /start для возврата в главное меню",
            reply_markup=back_to_main_button()
        )
    
    await state.clear()
