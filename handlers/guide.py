from aiogram import Router, F
from aiogram.types import CallbackQuery

from database import get_guide_articles
from keyboards import guide_keyboard, back_to_main_button

router = Router()

@router.callback_query(F.data == "menu_guide")
async def guide_menu(callback: CallbackQuery):
    articles = await get_guide_articles()
    await callback.message.edit_text(
        "🇨🇳 *Гид по жизни в Китае*\n\nВыбери тему:",
        parse_mode="Markdown",
        reply_markup=guide_keyboard(articles)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("guide_"))
async def show_guide_article(callback: CallbackQuery):
    article_id = int(callback.data.split("_")[1])
    
    from database import supabase
    response = supabase.table("guide_articles").select("*").eq("id", article_id).execute()
    
    if response.data:
        article = response.data[0]
        text = f"📖 *{article['title']}*\n\n{article['content']}"
        await callback.message.answer(text, parse_mode="Markdown", reply_markup=back_to_main_button())
    else:
        await callback.answer("Статья не найдена")
    await callback.answer()
