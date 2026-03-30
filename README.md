# 🚗 Mashina Parametrlari Bot

Bu interaktiv Telegram bot foydalanuvchilarga istalgan avtomobil haqida to'liq texnik ma'lumotlarni berishga, turli mashinalarni taqqoslashga va mashinalarga oid savollarga javob topishga yordam beradi. Bot **Mistral AI** (Xususan, Mistral Large modeli) ga asoslangan bo'lib, sun'iy intellekt orqali doimo eng so'nggi va aniq ma'lumotlarni taqdim etadi.

## 🌟 Imkoniyatlar

*   **🔍 Mashina qidirish:** Mashina nomi (masalan: `Toyota Camry 2024` yoki `BMW X5`) kiritilsa, bot u haqida to'liq parametrlarni (dvigatel, transmissiya, o'lchamlar, narx, yoqilg'i sarfi, tezlashuv va hk.) chiqarib beradi.
*   **⚖️ Mashinalarni taqqoslash:** Ikki yoki bir nechta mashina "vs" yoki "va" orqali so'ralsa (`Mercedes E-Class va BMW 5-Series`), bot ularni yonma-yon jadval/ro'yxat ko'rinishida taqqoslab, xulosa yozadi.
*   **🏷 Brendlar va Modellar:** Maxsus interaktiv klaviaturalar (Inline Buttons) orqali dunyoning eng mashhur brendlari va ularning modellari bo'ylab qulay navigatsiya qilish mumkin.
*   **📂 Kategoriyalar:** Sedan, SUV, Krossover, Sport, va Elektromobillar kabi kategoriyalar bo'yicha mashinalar ro'yxatini ko'rish oson.
*   **❓ Avto Ekspert Q&A rejimi:** Foydalanuvchi to'g'ridan-to'g'ri istalgan mashinalar bilan bog'liq ixtiyoriy savolni (masalan, `Eng iqtisodchi krossoverlar qaysi?`) berishi mumkin. AI mutaxassis sifatida javob beradi.

## 🛠 Texnologiyalar

*   **Python:** Asosiy dasturlash tili.
*   **aiogram v3:** Telegram bot yaratish uchun zamonaviy va asinxron freymvork.
*   **Mistral AI API:** Sun'iy intellekt xizmati sifatida ishlatilmoqda (`mistral-large-latest` modeli, kengaytirilgan tizim prompitlari bilan).
*   **python-dotenv:** Atrof-muhit o'zgaruvchilarini `.env` faylidan o'qish uchun.
*   **Asinxron dasturlash (asyncio):** API so'rovlarni va bot buyruqlarini parallel, tezkor ishlashi uchun.

## 📂 Loyiha tuzilishi

```text
Mahina-bot/
├── .env                  # Bot tokenlari va API kalitlari (yaratish kerak)
├── .gitignore            # Git kuzatmaydigan fayllar (masalan, .env, __pycache__)
├── main.py               # Botni ishga tushiruvchi asosiy (entry-point) fayl
├── requirements.txt      # Kutubxonalar ro'yxati (aiogram, mistralai va hk.)
└── bot/                  # Bot logikasi papkasi
    ├── config.py         # Sozlamalar, AI promptlar va kategoriyalar
    ├── ai_client.py      # Mistral AI bilan bog'lanish va so'rov yuborish
    ├── handlers/         # Bot buyruqlari va xabarlar handlerlari
    │   ├── commands.py   # /start, /help, klaviaturalar, inline buyruqlar
    │   └── chat.py       # Foydalanuvchidan oddiy / search xabarlarni tutish
    ├── middlewares/      # Qo'shimcha tekshiruv va cheklovlar
    │   └── __init__.py   # Antispam v.h. (RateLimitMiddleware, ErrorHandlerMiddleware)
    └── utils/            # Foydali yordamchi funksiyalar
        ├── formatter.py  # AI matnini Telegram formatiga (HTML) o'tkazish
        ├── sender.py     # Yozuv 4000 belgidan oshsa, bo'lib jo'natish
        └── validator.py  # URL v.b qo'shimcha tekshiruvlar (kerak bo'lsa)
```

## 🚀 O'rnatish va ishga tushirish (Lokal)

Botni o'z kompyuteringizda yoki serveringizda ishga tushirish uchun quyidagi qadamlarni bajaring:

**1. Repozitoriyni yuklab oling yoki klon qiling**
*(Agar Git orqali ishlayotgan bo'lsangiz)*
```bash
git clone https://github.com/SizningGithub/Mahina-bot.git
cd Mahina-bot
```

**2. Virtual muhit (Virtual Environment) yarating (Tavsiya qilinadi)**
```bash
python -m venv .venv
# Windows uchun:
.venv\Scripts\activate
# macOS/Linux uchun:
source .venv/bin/activate
```

**3. Kutubxonalarni o'rnating**
```bash
pip install -r requirements.txt
```

**4. .env faylini yarating**
Loyiha asosiy papkasida `Mahina-bot/.env` degan fayl yarating va unga o'zingizning API kalitlaringizni kiriting:
```ini
BOT_TOKEN=Sizning_Telegram_BotFather_Tokeningiz
MISTRAL_API_KEY=Sizning_Mistral_API_Kalitingiz
```

**5. Botni ishga tushiring**
```bash
python main.py
```

## 📖 Foydalanish (Bot bilan ishlash)

Bot ishga tushgandan kegin `Start` tugmasini bosing yoki `/start` yozing. Sizga maxsus menyu (Reply Keyboard) taqdim etiladi.

### Asosiy buyruqlar va tugmalar:

- **🔍 Mashina qidirish:** Mashina nomini kiritib qidirishni faollashtiradi (faqat shu nomni o'zini ham to'g'ridan to'g'ri yozish mumkin: `Chevrolet Lacetti`).
- **⚖️ Taqqoslash:** Ikki xil mashinani taqqoslaydi.
- **🏷 Brendlar:** Mashhur brendlardan birini ekranga inline menyuda chiqaradi va aniq modelni bosib tanlash mumkin bo'ladi.
- **📂 Kategoriyalar:** Krossover yoki Sedan kerak bo'lsa, kategoriyani chiqaradi va misol ko'rsatadi.
- **❓ Savol berish:** "Savol berish" tugmasini bosgandan yozilgan keyingi har qanday matn mashina bo'yicha maslahat so'rovi sifatida qabul qilinadi.

## 🤝 Hissa qo'shish (Contributing)

Agar botga yangi xususiyatlar yoki xatoliklarni to'g'irlashni xohlasangiz:
1. `Fork` qiling
2. Yangi `branch` yarating (`git checkout -b feature/YangiImkoniyat`)
3. O'zgarishlarni kiriting va kommit qiling (`git commit -m "Yangi imkoniyat qo'shildi"`)
4. O'z xushingiz bilan `push` qiling (`git push origin feature/YangiImkoniyat`)
5. **Pull Request** oching!
