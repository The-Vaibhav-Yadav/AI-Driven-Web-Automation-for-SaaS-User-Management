import json
import asyncio
from scraper import run_automation

async def use_result():
    result = await run_automation()

    return result

if __name__ == '__main__':
    asyncio.run(use_result())

