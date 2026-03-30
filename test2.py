import os
import asyncio
from mistralai.client import Mistral
from dotenv import load_dotenv
load_dotenv()

async def test_large():
    try:
        c = Mistral(api_key=os.getenv('MISTRAL_API_KEY'))
        print('Testing mistral-large-latest...')
        res = await asyncio.wait_for(
            c.chat.complete_async(model='mistral-large-latest', messages=[{'role':'user', 'content':'hi'}]),
            timeout=10.0
        )
        print("Success large:", res.choices[0].message.content[:20])
    except Exception as e:
        print("Error large:", repr(e))

async def test_small():
    try:
        c = Mistral(api_key=os.getenv('MISTRAL_API_KEY'))
        print('Testing mistral-small-latest...')
        res = await asyncio.wait_for(
            c.chat.complete_async(model='mistral-small-latest', messages=[{'role':'user', 'content':'hi'}]),
            timeout=10.0
        )
        print("Success small:", res.choices[0].message.content[:20])
    except Exception as e:
        print("Error small:", repr(e))

async def main():
    await test_small()
    await test_large()

asyncio.run(main())
