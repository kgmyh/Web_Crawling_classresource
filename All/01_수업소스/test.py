import asyncio 

async def sleep(sec):
    await asyncio.sleep(sec)

async def main():
    await sleep(3)

asyncio.run(main())