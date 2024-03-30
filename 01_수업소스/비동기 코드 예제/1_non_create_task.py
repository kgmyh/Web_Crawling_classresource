import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


# 다음 코드는 1초를 기다린 후 “hello”를 프린트한 다음 또 2초를 기다린 후 “world”를 프린트한다.
async def main():
    s = time.time()

    await say_after(1, "hello")
    await say_after(2, "world")

    print(f"finished at {time.time() - s} sec")


asyncio.run(main())
