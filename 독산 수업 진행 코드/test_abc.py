import asyncio
import time
# 코루틴
async def sleep2(seconds):
    #asyncio.sleep()-코루틴 -> 코루틴 호출시 await를 붙여준다.
    await asyncio.sleep(seconds)
    print('hello|', seconds)
    return seconds
    
async def main():
    # asyncio.gather() 코루틴들을 모아서 동시성으로 실행하기 위해 
    #                 event loop 에 등록해서 실행한다.
    await asyncio.gather(sleep2(1), sleep2(2), sleep2(3))

    
print("asaaaa")
print("bbbbb")
print(__name__)
if __name__ == "__main__":
    start = time.time()
    # main() 코루틴 호출
    asyncio.run(main())
    end = time.time()
    print("걸린시간:", end-start, "초")
