from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatAction, ParseMode

from bot.config import get_user_state, set_user_state
from bot.ai_client import get_car_info, compare_cars, ask_car_question
from bot.utils.sender import send_long_message

router = Router()


@router.message(F.text)
async def handle_message(message: Message):
    user_id = message.from_user.id
    user_text = message.text.strip()
    state = get_user_state(user_id)
    mode = state.get("mode", "idle")

    # Mashina qidirish rejimi
    if mode == "search":
        set_user_state(user_id, {"mode": "idle"})

        await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        processing_msg = await message.answer(
            f"🔍 <b>{user_text}</b> haqida ma'lumot izlanmoqda...\n"
            "⏳ Iltimos, kuting...",
            parse_mode=ParseMode.HTML
        )

        result = await get_car_info(user_text)
        await send_long_message(message, processing_msg, result)
        return

    # Taqqoslash rejimi
    if mode == "compare":
        set_user_state(user_id, {"mode": "idle"})

        await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        processing_msg = await message.answer(
            "⚖️ Mashinalar taqqoslanmoqda...\n"
            "⏳ Iltimos, kuting...",
            parse_mode=ParseMode.HTML
        )

        result = await compare_cars(user_text)
        await send_long_message(message, processing_msg, result)
        return

    # Savol-javob rejimi
    if mode == "ask":
        set_user_state(user_id, {"mode": "idle"})

        await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        processing_msg = await message.answer(
            "🤔 Javob tayyorlanmoqda...\n"
            "⏳ Iltimos, kuting...",
            parse_mode=ParseMode.HTML
        )

        result = await ask_car_question(user_text)
        await send_long_message(message, processing_msg, result)
        return

    # Oddiy holat — har qanday yozilgan matn mashina so'rovi deb qabul qilinadi
    # "vs" yoki "va" bo'lsa taqqoslash, yo'qsa qidirish
    if " vs " in user_text.lower() or " va " in user_text.lower():
        await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        processing_msg = await message.answer(
            "⚖️ Mashinalar taqqoslanmoqda...\n"
            "⏳ Iltimos, kuting...",
            parse_mode=ParseMode.HTML
        )

        result = await compare_cars(user_text)
        await send_long_message(message, processing_msg, result)
    else:
        await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        processing_msg = await message.answer(
            f"🔍 <b>{user_text}</b> haqida ma'lumot izlanmoqda...\n"
            "⏳ Iltimos, kuting...",
            parse_mode=ParseMode.HTML
        )

        result = await get_car_info(user_text)
        await send_long_message(message, processing_msg, result)
