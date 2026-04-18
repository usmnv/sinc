from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, Contact, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from database import user_exists, register_user, get_user
from keyboards import main_menu_keyboard, phone_keyboard, goal_keyboard, remove_keyboard
from states import Registration

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    
    if await user_exists(tg_id):
        user = await get_user(tg_id)
        # Убираем старую клавиатуру
        await message.answer("✅", reply_markup=remove_keyboard())
        await message.answer(
            f"👋 С возвращением, {user['name']}!",
            reply_markup=remove_keyboard()
        )
        await message.answer(
            "🏠 *Главное меню*\n\nВыбери нужный раздел:",
            parse_mode=ParseMode.MARKDOWN,
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
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=phone_keyboard()
        )
        await state.set_state(Registration.waiting_phone)

@router.message(Registration.waiting_phone, F.contact)
async def process_phone(message: Message, state: FSMContext):
    contact = message.contact
    phone = contact.phone_number
    await state.update_data(phone=phone)
    
    # Убираем клавиатуру с кнопкой номера!
    await message.answer("✅ Номер получен!", reply_markup=remove_keyboard())
    
    await message.answer(
        "🏙 *Из какого ты города?*\n\nНапиши название города (например: Пекин, Шанхай, Москва):",
        parse_mode=ParseMode.MARKDOWN
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
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=goal_keyboard()
    )
    await state.set_state(Registration.waiting_goal)

@router.message(Registration.waiting_goal)
async def process_goal(message: Message, state: FSMContext):
    goal_text = message.text
    goal_map = {
        "Бакалавриат": "Поступление в бакалавриат",
        "Изучение китайского языка": "Изучение китайского языка",
        "Магистратура": "Магистратура",
        "Подготовительные курсы": "Подготовительные курсы",
        "Другое": "Другое"
    }
    
    goal = goal_map.get(goal_text, goal_text)
    data = await state.get_data()
    tg_id = message.from_user.id
    
    await register_user(
        tg_id=tg_id,
        name=data["name"],
        phone=data["phone"],
        city=data["city"],
        goal=goal
    )
    
    # Убираем клавиатуру с целями
    await message.answer("✅ Регистрация завершена!", reply_markup=remove_keyboard())
    
    await message.answer(
        f"✅ *Регистрация завершена, {data['name']}!*\n\n"
        f"Теперь ты можешь пользоваться всеми функциями бота.",
        parse_mode=ParseMode.MARKDOWN
    )
    
    await message.answer(
        "🏠 *Главное меню*\n\nВыбери нужный раздел:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu_keyboard()
    )
    await state.clear()

@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer("✅", reply_markup=remove_keyboard())
    await message.answer(
        "🏠 *Главное меню*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu_keyboard()
    )
