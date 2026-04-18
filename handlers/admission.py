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
    university_list_keyboard, back_to_main_button, main_menu_keyboard, remove_keyboard
)
from states import CitySearch

router = Router()

# Соответствие текстов программ ID
PROGRAM_TEXT_TO_ID = {
    "1+4 (язык + бакалавриат": 1,
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
    "1+4 (язык + бакалавриат",
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
        "📍 *Выбери город:*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=city_choice_keyboard(cities)
    )

@router.message(F.text.in_(["🔍 Поиск по названию", "Поиск по названию"]))
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

@router.message(F.text.startswith("🏙 ") | F.text.in_(get_cities_list()))
async def city_selected(message: Message, state: FSMContext):
    city = message.text.replace("🏙 ", "").strip()
    data = await state.get_data()
    program_id = data.get("program_id")
    
    if not program_id:
        await message.answer("❌ Сначала выбери программу обучения.")
        return
    
    universities = await get_universities_by_program(program_id)
    filtered = [u for u in universities if u.get("city", "").lower() == city.lower()]
    
    if not filtered:
        await message.answer(f"❌ В городе {city} нет вузов по выбранной программе.")
        return
    
    # Сохраняем выбранный город
    await state.update_data(selected_city=city)
    
    text = f"🏛 *Найдено {len(filtered)} университетов в городе {city}:*\n\n"
    for i, uni in enumerate(filtered[:15], 1):
        text += f"{i}. {uni.get('name_ru', 'Название не указано')}\n"
    
    await message.answer(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=university_list_keyboard(filtered[:20])
    )

@router.message(F.text == "◀ Назад к городам")
async def back_to_cities(message: Message, state: FSMContext):
    cities = await get_cities_list()
    await message.answer(
        "📍 *Выбери город:*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=city_choice_keyboard(cities)
    )

@router.message(F.text == "🏠 Главное меню")
async def back_to_main_menu(message: Message):
    await message.answer(
        "🏠 *Главное меню*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu_keyboard()
    )

@router.message(F.text, CitySearch.waiting_city_name)
async def handle_city_search(message: Message, state: FSMContext):
    city = message.text.strip()
    universities = await get_universities_by_city(city)
    
    if not universities:
        await message.answer(
            f"❌ Город '{city}' не найден.",
            reply_markup=back_to_main_button()
        )
    else:
        for uni in universities:
            text = f"🏛 *{uni.get('name_ru', 'Название не указано')}*\n📍 {uni.get('city', 'Не указан')}\n📚 {uni.get('duration', 'Не указана')}\n💰 {uni.get('price_per_year', 'Уточняйте')} ¥/год\n\n{uni.get('description', 'Нет описания')}"
            await message.answer(text, parse_mode=ParseMode.MARKDOWN)
        await message.answer("Нажми /start для возврата в меню")
    
    await state.clear()

@router.message(F.text.startswith("🏛 "))
async def show_university_detail(message: Message):
    uni_name = message.text.replace("🏛 ", "").split("\n")[0].strip()
    
    from database import supabase
    try:
        response = supabase.table("universities").select("*").ilike("name_ru", f"%{uni_name}%").execute()
        
        if response.data:
            uni = response.data[0]
            text = (
                f"🏛 *{uni.get('name_ru', 'Название не указано')}*\n\n"
                f"📖 *Китайское название:* {uni.get('name_cn', 'Не указано')}\n"
                f"📍 *Город:* {uni.get('city', 'Не указан')}\n"
                f"📚 *Программа:* {uni.get('duration', 'Не указана')}\n"
                f"💰 *Стоимость:* {uni.get('price_per_year', 'Уточняйте')} ¥/год\n\n"
                f"📝 *Описание:*\n{uni.get('description', 'Нет описания')}"
            )
            await message.answer(text, parse_mode=ParseMode.MARKDOWN)
        else:
            await message.answer("❌ Университет не найден")
    except Exception as e:
        await message.answer("❌ Ошибка при загрузке данных")
