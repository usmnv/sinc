from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, Contact
from aiogram.fsm.context import FSMContext

from database import user_exists, register_user, get_user
from keyboards import main_menu_keyboard, phone_keyboard, goal_keyboard
from states import Registration

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    
    if await user_exists(tg_id):
        user = await get_user(tg_id)
        await message.answer(
            f"👋 С возвращением, {user['name']}!\n\nВыбери действие:",
            reply_markup=main_menu_keyboard()
        )
    else:
        name = message.from_user.first_name
        if message.from_user.last_name:
            name += " " + message.from_user.last_name
        
        await state.update_data(name=name)
        
        await message.answer(
            f"🎓 *Добро пожаловать в China Study Bot, {name}!*\n\n"
            f"📱 *Пожалуйста, отправь свой номер телефона*, нажав на кнопку ниже:",
            parse_mode="Markdown",
            reply_markup=phone_keyboard()
        )
        await state.set_state(Registration.waiting_phone)

@router.message(Registration.waiting_phone, F.contact)
async def process_phone(message: Message, state: FSMContext):
    contact = message.contact
    phone = contact.phone_number
    await state.update_data(phone=phone)
    
    await message.answer(
        "🏙 *Из какого ты города?*\n\nНапиши название города:",
        parse_mode="Markdown",
        reply_markup=None
    )
    await state.set_state(Registration.waiting_city)

@router.message(Registration.waiting_phone)
async def process_phone_invalid(message: Message):
    await message.answer(
        "❓ Пожалуйста, используй кнопку для отправки номера телефона.",
        reply_markup=phone_keyboard()
    )

@router.message(Registration.waiting_city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer(
        "🎯 *Какую цель ставишь?*\n\nВыбери один из вариантов:",
        parse_mode="Markdown",
        reply_markup=goal_keyboard()
    )

@router.callback_query(F.data.startswith("goal_"))
async def process_goal(callback: CallbackQuery, state: FSMContext):
    goal_map = {
        "goal_bachelor": "Поступление в бакалавриат",
        "goal_language": "Изучение китайского языка",
        "goal_master": "Магистратура",
        "goal_preparation": "Подготовительные курсы",
        "goal_other": "Другое"
    }
    
    goal = goal_map.get(callback.data, "Не указано")
    data = await state.get_data()
    tg_id = callback.from_user.id
    
    await register_user(
        tg_id=tg_id,
        name=data["name"],
        phone=data["phone"],
        city=data["city"],
        goal=goal
    )
    
    await callback.message.delete()
    await callback.message.answer(
        f"✅ *Регистрация завершена, {data['name']}!*\n\nТеперь ты можешь пользоваться всеми функциями бота.",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )
    await state.clear()
    await callback.answer()

@router.callback_query(F.data == "back_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "🏠 *Главное меню*\n\nВыбери нужный раздел:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()

@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer(
        "🏠 *Главное меню*",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )
