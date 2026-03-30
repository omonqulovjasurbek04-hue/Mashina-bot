from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode, ChatAction
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from bot.config import (
    CAR_CATEGORIES, POPULAR_BRANDS,
    get_user_state, set_user_state
)
from bot.ai_client import get_car_info, compare_cars
from bot.utils.sender import send_long_message

router = Router()


# ═══════════════════════════════════════════
# 🎹 KLAVIATURALAR
# ═══════════════════════════════════════════

def get_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔍 Mashina qidirish"),
                KeyboardButton(text="⚖️ Taqqoslash"),
            ],
            [
                KeyboardButton(text="🏷 Brendlar"),
                KeyboardButton(text="📂 Kategoriyalar"),
            ],
            [
                KeyboardButton(text="❓ Savol berish"),
                KeyboardButton(text="📖 Yordam"),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Mashina nomini yozing..."
    )
    return keyboard


def get_brands_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    brands_list = list(POPULAR_BRANDS.items())
    for i in range(0, len(brands_list), 2):
        row = []
        for j in range(i, min(i + 2, len(brands_list))):
            brand_id, brand_name = brands_list[j]
            row.append(InlineKeyboardButton(
                text=brand_name,
                callback_data=f"brand_{brand_id}"
            ))
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="❌ Yopish", callback_data="close_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_categories_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    cats_list = list(CAR_CATEGORIES.items())
    for i in range(0, len(cats_list), 2):
        row = []
        for j in range(i, min(i + 2, len(cats_list))):
            cat_id, cat_name = cats_list[j]
            row.append(InlineKeyboardButton(
                text=cat_name,
                callback_data=f"cat_{cat_id}"
            ))
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="❌ Yopish", callback_data="close_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_brand_models_keyboard(brand: str) -> InlineKeyboardMarkup:
    """Har bir brend uchun mashhur modellar"""
    brand_models = {
        "chevrolet": ["Malibu", "Tracker", "Equinox", "Tahoe", "Camaro", "Cobalt", "Spark", "Damas"],
        "toyota": ["Camry", "Corolla", "RAV4", "Land Cruiser", "Hilux", "Prius", "Highlander", "Fortuner"],
        "hyundai": ["Sonata", "Tucson", "Santa Fe", "Accent", "Elantra", "Palisade", "Creta", "Kona"],
        "kia": ["K5", "Sportage", "Sorento", "Rio", "Cerato", "Carnival", "Seltos", "EV6"],
        "bmw": ["3 Series", "5 Series", "X3", "X5", "X7", "7 Series", "M3", "iX"],
        "mercedes": ["C-Class", "E-Class", "S-Class", "GLC", "GLE", "GLS", "A-Class", "EQS"],
        "audi": ["A4", "A6", "Q5", "Q7", "A3", "Q3", "e-tron", "RS6"],
        "volkswagen": ["Tiguan", "Passat", "Golf", "Polo", "Touareg", "Atlas", "ID.4", "Jetta"],
        "honda": ["Civic", "CR-V", "Accord", "HR-V", "Pilot", "City", "Jazz", "ZR-V"],
        "nissan": ["Qashqai", "X-Trail", "Patrol", "Sentra", "Kicks", "Navara", "Leaf", "Altima"],
        "ford": ["F-150", "Mustang", "Explorer", "Ranger", "Bronco", "Escape", "Focus", "Maverick"],
        "tesla": ["Model 3", "Model Y", "Model S", "Model X", "Cybertruck", "Semi"],
        "byd": ["Han", "Seal", "Atto 3", "Dolphin", "Song Plus", "Tang", "Qin Plus", "Seagull"],
        "geely": ["Coolray", "Atlas Pro", "Monjaro", "Emgrand", "Tugella", "Preface"],
        "chery": ["Tiggo 7 Pro", "Tiggo 8 Pro", "Arrizo 8", "Omoda C5", "Tiggo 4 Pro", "Exeed TXL"],
        "haval": ["Jolion", "H6", "F7", "Dargo", "H9", "Jolion HEV"],
    }

    models = brand_models.get(brand, [])
    brand_name = POPULAR_BRANDS.get(brand, brand.title())

    buttons = []
    for i in range(0, len(models), 2):
        row = []
        for j in range(i, min(i + 2, len(models))):
            model = models[j]
            row.append(InlineKeyboardButton(
                text=f"📌 {model}",
                callback_data=f"model_{brand}_{model}"
            ))
        buttons.append(row)

    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_brands")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_category_examples_keyboard(category: str) -> InlineKeyboardMarkup:
    """Har bir kategoriya uchun misol mashinalar"""
    cat_examples = {
        "sedan": ["Toyota Camry", "Hyundai Sonata", "Chevrolet Malibu", "Kia K5", "BMW 5 Series", "Mercedes E-Class"],
        "suv": ["Toyota RAV4", "Hyundai Tucson", "Kia Sportage", "BMW X5", "Chevrolet Tahoe", "Haval H6"],
        "hatchback": ["Volkswagen Golf", "Honda Civic HB", "Hyundai i30", "Kia Ceed", "Toyota Yaris", "Peugeot 308"],
        "truck": ["Ford F-150", "Toyota Hilux", "Chevrolet Silverado", "Nissan Navara", "Ford Ranger", "RAM 1500"],
        "electric": ["Tesla Model 3", "BYD Seal", "Hyundai Ioniq 5", "Kia EV6", "BMW iX", "Mercedes EQS"],
        "sport": ["BMW M3", "Porsche 911", "Chevrolet Camaro", "Ford Mustang", "Audi RS6", "Mercedes AMG GT"],
        "luxury": ["Mercedes S-Class", "BMW 7 Series", "Audi A8", "Lexus LS", "Genesis G90", "Rolls-Royce Ghost"],
        "minivan": ["Kia Carnival", "Toyota Sienna", "Honda Odyssey", "Chrysler Pacifica", "Hyundai Staria"],
    }

    examples = cat_examples.get(category, [])
    cat_name = CAR_CATEGORIES.get(category, category.title())

    buttons = []
    for i in range(0, len(examples), 2):
        row = []
        for j in range(i, min(i + 2, len(examples))):
            car = examples[j]
            row.append(InlineKeyboardButton(
                text=f"📌 {car}",
                callback_data=f"car_{car}"
            ))
        buttons.append(row)

    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_categories")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ═══════════════════════════════════════════
# 📌 BUYRUQLAR
# ═══════════════════════════════════════════

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    set_user_state(user_id, {"mode": "idle"})

    welcome = (
        "🚗 <b>Mashina Parametrlari Bot</b>ga xush kelibsiz!\n\n"
        "Men sizga istalgan mashina haqida <b>to'liq texnik ma'lumot</b> beraman:\n\n"
        "🔍 <b>Mashina qidirish</b> — Mashina nomini yozing\n"
        "⚖️ <b>Taqqoslash</b> — Ikki mashinani solishtiring\n"
        "🏷 <b>Brendlar</b> — Mashhur brendlar ro'yxati\n"
        "📂 <b>Kategoriyalar</b> — Mashina turlari\n"
        "❓ <b>Savol berish</b> — Mashinalar haqida savol\n\n"
        "📌 <i>Mashina nomini yozing yoki quyidagi tugmalardan foydalaning!</i> ⬇️"
    )
    await message.answer(welcome, parse_mode=ParseMode.HTML, reply_markup=get_main_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message):
    help_text = (
        "📖 <b>Yordam — Mashina Parametrlari Bot</b>\n\n"
        "<b>🔍 Mashina qidirish:</b>\n"
        "Mashina nomini yozing (masalan: <code>Toyota Camry 2024</code>)\n"
        "yoki /car buyrug'ini ishlating\n\n"
        "<b>⚖️ Taqqoslash:</b>\n"
        "Ikki mashinani \"vs\" yoki \"va\" bilan yozing:\n"
        "<code>Toyota Camry vs Hyundai Sonata</code>\n"
        "yoki /compare buyrug'ini ishlating\n\n"
        "<b>🏷 Brendlar:</b>\n"
        "Mashhur brendlar ro'yxatidan tanlang\n\n"
        "<b>📂 Kategoriyalar:</b>\n"
        "Sedan, SUV, Elektromobil va boshqalar\n\n"
        "<b>❓ Savol berish:</b>\n"
        "Mashinalar haqida istalgan savol yozing\n\n"
        "<b>📋 Buyruqlar:</b>\n"
        "/start — Botni ishga tushirish\n"
        "/help — Yordam\n"
        "/car <code>&lt;nomi&gt;</code> — Mashina haqida ma'lumot\n"
        "/compare <code>&lt;nomi vs nomi&gt;</code> — Mashina taqqoslash\n\n"
        "<b>💡 Misol:</b>\n"
        "<code>/car Chevrolet Malibu 2024</code>\n"
        "<code>/compare BMW X5 vs Mercedes GLE</code>"
    )
    await message.answer(help_text, parse_mode=ParseMode.HTML, reply_markup=get_main_keyboard())


@router.message(Command("car"))
async def cmd_car(message: Message):
    user_id = message.from_user.id
    args = message.text.replace("/car", "").strip()

    if not args:
        set_user_state(user_id, {"mode": "search"})
        await message.answer(
            "🔍 <b>Mashina qidirish</b>\n\n"
            "Mashina nomini yozing (masalan: <code>Toyota Camry 2024</code>):",
            parse_mode=ParseMode.HTML
        )
        return

    await _search_car(message, args)


@router.message(Command("compare"))
async def cmd_compare(message: Message):
    user_id = message.from_user.id
    args = message.text.replace("/compare", "").strip()

    if not args:
        set_user_state(user_id, {"mode": "compare"})
        await message.answer(
            "⚖️ <b>Mashina taqqoslash</b>\n\n"
            "Ikki mashina nomini \"vs\" yoki \"va\" bilan yozing:\n"
            "<code>Toyota Camry vs Hyundai Sonata</code>",
            parse_mode=ParseMode.HTML
        )
        return

    await _compare_cars(message, args)


# ═══════════════════════════════════════════
# 🔘 TUGMALAR (Reply Keyboard)
# ═══════════════════════════════════════════

@router.message(lambda m: m.text == "🔍 Mashina qidirish")
async def btn_search(message: Message):
    user_id = message.from_user.id
    set_user_state(user_id, {"mode": "search"})
    await message.answer(
        "🔍 <b>Mashina qidirish</b>\n\n"
        "Qidirayotgan mashina nomini yozing:\n\n"
        "<i>Misol: Toyota Camry, BMW X5 2024, Chevrolet Malibu</i>",
        parse_mode=ParseMode.HTML
    )


@router.message(lambda m: m.text == "⚖️ Taqqoslash")
async def btn_compare(message: Message):
    user_id = message.from_user.id
    set_user_state(user_id, {"mode": "compare"})
    await message.answer(
        "⚖️ <b>Mashina taqqoslash</b>\n\n"
        "Ikki mashina nomini yozing:\n\n"
        "<i>Misol: Toyota Camry vs Hyundai Sonata</i>\n"
        "<i>Misol: BMW X5 va Mercedes GLE</i>",
        parse_mode=ParseMode.HTML
    )


@router.message(lambda m: m.text == "🏷 Brendlar")
async def btn_brands(message: Message):
    user_id = message.from_user.id
    set_user_state(user_id, {"mode": "idle"})
    await message.answer(
        "🏷 <b>Mashhur avtomobil brendlari</b>\n\n"
        "Quyidagi brendlardan birini tanlang:",
        parse_mode=ParseMode.HTML,
        reply_markup=get_brands_keyboard()
    )


@router.message(lambda m: m.text == "📂 Kategoriyalar")
async def btn_categories(message: Message):
    user_id = message.from_user.id
    set_user_state(user_id, {"mode": "idle"})
    await message.answer(
        "📂 <b>Mashina kategoriyalari</b>\n\n"
        "Qaysi turdagi mashina kerak?",
        parse_mode=ParseMode.HTML,
        reply_markup=get_categories_keyboard()
    )


@router.message(lambda m: m.text == "❓ Savol berish")
async def btn_ask(message: Message):
    user_id = message.from_user.id
    set_user_state(user_id, {"mode": "ask"})
    await message.answer(
        "❓ <b>Savol-javob rejimi</b>\n\n"
        "Mashinalar haqida istalgan savolingizni yozing:\n\n"
        "<i>Misol: Qaysi SUV eng kam yoqilg'i sarflaydi?</i>\n"
        "<i>Misol: 2024-yilda eng arzon elektromobillar?</i>",
        parse_mode=ParseMode.HTML
    )


@router.message(lambda m: m.text == "📖 Yordam")
async def btn_help(message: Message):
    await cmd_help(message)


# ═══════════════════════════════════════════
# 🔘 INLINE TUGMALAR (Callback)
# ═══════════════════════════════════════════

@router.callback_query(lambda c: c.data and c.data.startswith("brand_"))
async def cb_brand_selected(callback: CallbackQuery):
    brand = callback.data.replace("brand_", "")
    brand_name = POPULAR_BRANDS.get(brand, brand.title())

    await callback.message.edit_text(
        f"🏷 <b>{brand_name}</b> modellari:\n\n"
        "Quyidagi modellardan birini tanlang:",
        parse_mode=ParseMode.HTML,
        reply_markup=get_brand_models_keyboard(brand)
    )
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("cat_"))
async def cb_category_selected(callback: CallbackQuery):
    category = callback.data.replace("cat_", "")
    cat_name = CAR_CATEGORIES.get(category, category.title())

    await callback.message.edit_text(
        f"📂 <b>{cat_name}</b> mashinalar:\n\n"
        "Quyidagi mashinalardan birini tanlang:",
        parse_mode=ParseMode.HTML,
        reply_markup=get_category_examples_keyboard(category)
    )
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("model_"))
async def cb_model_selected(callback: CallbackQuery):
    parts = callback.data.replace("model_", "").split("_", 1)
    brand = parts[0]
    model = parts[1] if len(parts) > 1 else ""
    brand_name = POPULAR_BRANDS.get(brand, brand.title())
    full_name = f"{brand_name.split(' ', 1)[-1]} {model}"

    await callback.message.edit_text(
        f"🔍 <b>{full_name}</b> haqida ma'lumot izlanmoqda...",
        parse_mode=ParseMode.HTML
    )
    await callback.answer()

    await callback.message.bot.send_chat_action(callback.message.chat.id, ChatAction.TYPING)
    result = await get_car_info(full_name)
    await send_long_message(callback.message, callback.message, result)


@router.callback_query(lambda c: c.data and c.data.startswith("car_"))
async def cb_car_selected(callback: CallbackQuery):
    car_name = callback.data.replace("car_", "")

    await callback.message.edit_text(
        f"🔍 <b>{car_name}</b> haqida ma'lumot izlanmoqda...",
        parse_mode=ParseMode.HTML
    )
    await callback.answer()

    await callback.message.bot.send_chat_action(callback.message.chat.id, ChatAction.TYPING)
    result = await get_car_info(car_name)
    await send_long_message(callback.message, callback.message, result)


@router.callback_query(lambda c: c.data == "back_brands")
async def cb_back_brands(callback: CallbackQuery):
    await callback.message.edit_text(
        "🏷 <b>Mashhur avtomobil brendlari</b>\n\n"
        "Quyidagi brendlardan birini tanlang:",
        parse_mode=ParseMode.HTML,
        reply_markup=get_brands_keyboard()
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "back_categories")
async def cb_back_categories(callback: CallbackQuery):
    await callback.message.edit_text(
        "📂 <b>Mashina kategoriyalari</b>\n\n"
        "Qaysi turdagi mashina kerak?",
        parse_mode=ParseMode.HTML,
        reply_markup=get_categories_keyboard()
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "close_menu")
async def cb_close_menu(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer("✅ Menyu yopildi")


# ═══════════════════════════════════════════
# 🔧 YORDAMCHI FUNKSIYALAR
# ═══════════════════════════════════════════

async def _search_car(message: Message, car_name: str):
    """Mashina haqida ma'lumot qidirish"""
    user_id = message.from_user.id
    set_user_state(user_id, {"mode": "idle"})

    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    processing_msg = await message.answer(
        f"🔍 <b>{car_name}</b> haqida ma'lumot izlanmoqda...\n"
        "⏳ Iltimos, kuting...",
        parse_mode=ParseMode.HTML
    )

    result = await get_car_info(car_name)
    await send_long_message(message, processing_msg, result)


async def _compare_cars(message: Message, cars_text: str):
    """Mashinalarni taqqoslash"""
    user_id = message.from_user.id
    set_user_state(user_id, {"mode": "idle"})

    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    processing_msg = await message.answer(
        f"⚖️ Mashinalar taqqoslanmoqda...\n"
        "⏳ Iltimos, kuting...",
        parse_mode=ParseMode.HTML
    )

    result = await compare_cars(cars_text)
    await send_long_message(message, processing_msg, result)
