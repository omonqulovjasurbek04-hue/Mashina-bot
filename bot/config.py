import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

MAX_HISTORY = 10
RATE_LIMIT_SECONDS = 2

# Mashina so'rovi uchun ishlatiladigan model
CAR_MODEL = "mistral-large-latest"

# Mashina kategoriyalari
CAR_CATEGORIES = {
    "sedan": "🚗 Sedan",
    "suv": "🚙 SUV / Krossover",
    "hatchback": "🏎 Xetchbek",
    "truck": "🛻 Pikap / Yuk mashina",
    "electric": "⚡ Elektromobil",
    "sport": "🏁 Sport mashina",
    "luxury": "💎 Lyuks mashina",
    "minivan": "🚐 Miniven",
}

# Mashhur brendlar
POPULAR_BRANDS = {
    "chevrolet": "🇺🇸 Chevrolet",
    "toyota": "🇯🇵 Toyota",
    "hyundai": "🇰🇷 Hyundai",
    "kia": "🇰🇷 Kia",
    "bmw": "🇩🇪 BMW",
    "mercedes": "🇩🇪 Mercedes-Benz",
    "audi": "🇩🇪 Audi",
    "volkswagen": "🇩🇪 Volkswagen",
    "honda": "🇯🇵 Honda",
    "nissan": "🇯🇵 Nissan",
    "ford": "🇺🇸 Ford",
    "tesla": "🇺🇸 Tesla",
    "byd": "🇨🇳 BYD",
    "geely": "🇨🇳 Geely",
    "chery": "🇨🇳 Chery",
    "haval": "🇨🇳 Haval",
}

# Foydalanuvchi holatlari
user_states: dict[int, dict] = {}

def get_user_state(user_id: int) -> dict:
    if user_id not in user_states:
        user_states[user_id] = {"mode": "idle"}
    return user_states[user_id]

def set_user_state(user_id: int, state: dict):
    user_states[user_id] = state

# Mashina eksperti uchun system prompt
CAR_SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Sen professional avtomobil ekspertisan. "
        "Foydalanuvchi mashina nomi yoki modelini yozadi, sen uning to'liq texnik parametrlarini batafsil ko'rsatasan.\n\n"
        "Javobni quyidagi formatda ber:\n\n"
        "🚗 **[Mashina nomi]**\n\n"
        "📋 **Umumiy ma'lumot:**\n"
        "• 🏭 Ishlab chiqaruvchi: ...\n"
        "• 📅 Ishlab chiqarilgan yillar: ...\n"
        "• 🏷 Klass: ...\n"
        "• 🌍 Ishlab chiqarilgan davlat: ...\n\n"
        "⚙️ **Dvigatel:**\n"
        "• 🔧 Dvigatel turi: ...\n"
        "• 📏 Hajmi: ... L\n"
        "• ⚡ Quvvat: ... ot kuchi (... kVt)\n"
        "• 💨 Moment: ... Nm\n"
        "• ⛽ Yoqilg'i turi: ...\n\n"
        "🔄 **Transmissiya:**\n"
        "• Uzatmalar qutisi: ...\n"
        "• Yurg'izuvchi g'ildiraklar: ...\n\n"
        "📐 **O'lchamlar:**\n"
        "• Uzunligi: ... mm\n"
        "• Kengligi: ... mm\n"
        "• Balandligi: ... mm\n"
        "• Kolyor bazasi: ... mm\n"
        "• Yuk xonasi hajmi: ... L\n\n"
        "🏎 **Tezlik va dinamika:**\n"
        "• 0-100 km/s: ... soniya\n"
        "• Maksimal tezlik: ... km/s\n\n"
        "⛽ **Yoqilg'i sarfi:**\n"
        "• Shahar: ... L/100km\n"
        "• Trassa: ... L/100km\n"
        "• Aralash: ... L/100km\n"
        "• Bak hajmi: ... L\n\n"
        "⚖️ **Og'irlik:**\n"
        "• Bo'sh og'irligi: ... kg\n"
        "• To'liq og'irligi: ... kg\n\n"
        "🛡 **Xavfsizlik:**\n"
        "• Euro NCAP / NHTSA: ...\n"
        "• Yostiqchalar soni: ...\n"
        "• ABS / ESP / Boshqa tizimlar: ...\n\n"
        "💰 **Narxi:**\n"
        "• AQSh: $...\n"
        "• O'zbekiston (taxminiy): ... so'm\n\n"
        "📝 **Qo'shimcha ma'lumot:**\n"
        "• Asosiy afzalliklari: ...\n"
        "• Kamchiliklari: ...\n"
        "• Raqobatchilari: ...\n"
        "• Tavsiya: ...\n\n"
        "Agar foydalanuvchi aniq model va yilni ko'rsatsa, o'sha versiya haqida yoz. "
        "Agar faqat brend yoki model yozsa, eng so'nggi versiyasi haqida yoz. "
        "Javobni o'zbek tilida ber. Ma'lumotlar iloji boricha aniq va to'g'ri bo'lsin."
    )
}

# Mashina taqqoslash uchun prompt
CAR_COMPARE_PROMPT = {
    "role": "system",
    "content": (
        "Sen professional avtomobil ekspertisan. "
        "Foydalanuvchi ikki yoki undan ko'p mashinani taqqoslashni so'raydi.\n\n"
        "Har bir mashina uchun asosiy parametrlarni jadval ko'rinishida taqqosla:\n"
        "- Dvigatel, quvvat, moment\n"
        "- Tezlanish, maksimal tezlik\n"
        "- Yoqilg'i sarfi\n"
        "- Narxi\n"
        "- Xavfsizlik\n\n"
        "Oxirida qaysi mashina qaysi jihatdan yaxshiroq ekanligini xulosa qil.\n"
        "Javobni o'zbek tilida ber."
    )
}
