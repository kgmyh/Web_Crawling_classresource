import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():

    s = time.time()

    # task 생성 대신 gather로 모아서 실행.
    # gather에 코루틴을 넣으면 내부적으로 Task로 만들어 실행한다.
    result_list = await asyncio.gather(say_after(1, "hello"), say_after(2, "word"))

    print(f"finished at {time.time() - s} sec")


asyncio.run(main())
