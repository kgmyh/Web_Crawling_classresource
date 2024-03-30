async def do_async():
    
    print(1)
    return 30

async def test():
    await do_async()
    print("test")

import asyncio

asyncio.run(test())