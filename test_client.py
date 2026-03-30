import asyncio
import logging
from bot.ai_client import get_car_info, compare_cars

logging.basicConfig(level=logging.ERROR)

async def run_tests():
    print("Test 1: get_car_info")
    res1 = await get_car_info("Chevrolet Malibu")
    print(res1[:200]) # Print first 200 chars

    print("\nTest 2: compare_cars")
    res2 = await compare_cars("Malibu vs Sonata")
    print(res2[:200])

if __name__ == "__main__":
    asyncio.run(run_tests())
