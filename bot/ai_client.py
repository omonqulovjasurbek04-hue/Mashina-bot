import logging

from mistralai.client import Mistral

from bot.config import (
    MISTRAL_API_KEY, CAR_MODEL,
    CAR_SYSTEM_PROMPT, CAR_COMPARE_PROMPT
)

logger = logging.getLogger(__name__)

mistral_client = Mistral(api_key=MISTRAL_API_KEY)


async def get_car_info(car_name: str) -> str:
    """Mashina haqida to'liq ma'lumot olish"""
    try:
        response = await mistral_client.chat.complete_async(
            model=CAR_MODEL,
            messages=[
                CAR_SYSTEM_PROMPT,
                {
                    "role": "user",
                    "content": f"Menga {car_name} mashina haqida to'liq ma'lumot ber."
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"Mashina ma'lumot olishda xato (car={car_name}): {e}", exc_info=True)
        return "❌ Xato yuz berdi. Iltimos, mashina nomini to'g'ri yozing va qayta urinib ko'ring."


async def compare_cars(car_names: str) -> str:
    """Ikki yoki undan ko'p mashinani taqqoslash"""
    try:
        response = await mistral_client.chat.complete_async(
            model=CAR_MODEL,
            messages=[
                CAR_COMPARE_PROMPT,
                {
                    "role": "user",
                    "content": f"Quyidagi mashinalarni taqqoslab ber: {car_names}"
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"Taqqoslashda xato (cars={car_names}): {e}", exc_info=True)
        return "❌ Taqqoslashda xato yuz berdi. Iltimos, mashina nomlarini to'g'ri yozing."


async def ask_car_question(question: str) -> str:
    """Mashina haqida umumiy savol berish"""
    try:
        response = await mistral_client.chat.complete_async(
            model=CAR_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sen avtomobil bo'yicha ekspertsan. "
                        "Foydalanuvchining mashinalar haqidagi savollariga javob ber. "
                        "Javobni o'zbek tilida, tushunarli va batafsil ber."
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"Savol-javobda xato: {e}", exc_info=True)
        return "❌ Xato yuz berdi. Iltimos, savolingizni qayta yozing."


async def close_client():
    try:
        await mistral_client.close_async()
        logger.info("Mistral client yopildi")
    except Exception as e:
        logger.warning(f"Mistral client yopishda xato: {e}")
