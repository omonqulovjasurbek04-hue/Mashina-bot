import os
import asyncio
from dotenv import load_dotenv
load_dotenv()
from mistralai.client import Mistral

async def test():
    print('Starting')
    try:
        client = Mistral(api_key=os.getenv('MISTRAL_API_KEY'))
        print('Client init')
        res = await client.chat.complete_async(
            model='mistral-small-latest',
            messages=[{'role':'user', 'content':'hi'}]
        )
        print('RES:', res.choices[0].message.content)
    except Exception as e:
        print('ERR:', e)

asyncio.run(test())
