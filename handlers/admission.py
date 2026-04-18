from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from database import (
    get_all_programs, get_universities_by_program,
    get_universities_by_city, get_cities_list
)
from keyboards import (
    programs_keyboard, city_choice_keyboard,
    university_list_keyboard, back_to_main_button
)
from states import CitySearch

router = Router()

PROGRAM_CODE_TO_ID = {"1_4": 1, "1_3": 2, "bach_4": 3, "mag": 4, "lang_1": 5}

@router.callback_query(F.data == "menu_admission")
async def admission_menu(callback: CallbackQuery):
    programs = await get_all_programs()
    await callback.message.edit_text(
        "🎓 *Выбери программу обучения:*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=programs_keyboard(programs)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("prog_"))
async def program_selected(callback: CallbackQuery, state: FSMContext):
    program_code = callback.data.split("_")[1]
    program_id = PROGRAM_CODE_TO_ID.get(program_code)
    
    if not program_id:
        await callback.answer("Ошибка: программа не найдена")
        return
    
    await state.update_data(program_code=program_code, program_id=program_id)
    cities = await get_cities_list()
    await callback.message.edit_text(
        "📍 *Выбери город:*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=city_choice_keyboard(cities)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("city_"))
async def city_selected(callback: CallbackQuery, state: FSMContext):
    city = callback.data.split("_", 1)[1]
    data = await state.get_data()
    program_code = data.get("program_code")
    program_id = data.get("program_id")
    
    universities = await get_universities_by_program(program_id)
    filtered = [u for u in universities if u["city"].lower() == city.lower()]
    
    if not filtered:
        await callback.message.answer(f"❌ В городе {city} нет вузов по выбранной программе.")
        return
    
    text = f"🏛 *Найдено {len(filtered)} университетов:*\n\n"
    for i, uni in enumerate(filtered[:10], 1):
        text += f"{i}. {uni['name_ru']}\n"
    if len(filtered) > 10:
        text += f"\n...и еще {len(filtered) - 10} вузов"
    
    await callback.message.edit_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=university_list_keyboard(filtered[:20], program_code)
    )
    await callback.answer()

@router.callback_query(F.data == "city_search")
async def search_city_prompt(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🔍 *Введи название города:*", parse_mode=ParseMode.MARKDOWN)
    await state.set_state(CitySearch.waiting_city_name)
    await callback.answer()

@router.message(CitySearch.waiting_city_name)
async def handle_city_search(message: Message, state: FSMContext):
    city = message.text.strip()
    universities = await get_universities_by_city(city)
    
    if not universities:
        await message.answer(f"❌ Город '{city}' не найден.", reply_markup=back_to_main_button())
    else:
        for uni in universities:
            text = f"🏛 *{uni['name_ru']}*\n📍 {uni['city']}\n📚 {uni['duration']}\n💰 {uni['price_per_year']} ¥/год\n\n{uni['description']}"
            await message.answer(text, parse_mode=ParseMode.MARKDOWN)
        await message.answer("Нажми /start для возврата в меню")
    await state.clear()

@router.callback_query(F.data.startswith("uni_"))
async def show_university_detail(callback: CallbackQuery):
    uni_id = int(callback.data.split("_")[1])
    
    from database import supabase
    response = supabase.table("universities").select("*").eq("id", uni_id).execute()
    
    if response.data:
        uni = response.data[0]
        text = f"🏛 *{uni['name_ru']}*\n📖 *Китайское название:* {uni['name_cn']}\n📍 *Город:* {uni['city']}\n📚 *Программа:* {uni['duration']}\n💰 *Стоимость:* {uni['price_per_year']} ¥/год\n\n📝 *Описание:*\n{uni['description']}"
        await callback.message.answer(text, parse_mode=ParseMode.MARKDOWN)
    else:
        await callback.answer("Университет не найден")
    await callback.answer()
