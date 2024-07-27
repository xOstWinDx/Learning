import asyncio


async def func1():
    counter = 0
    while True:
        counter += 1
        print(f"func1: {counter}")
        await asyncio.sleep(1)
        return counter


async def func2():
    counter = 0
    while True:
        counter += 1
        print(f"func2: {counter}")
        await asyncio.sleep(2)
        return counter


async def main():

    async with asyncio.TaskGroup() as tg:
        f1 = tg.create_task(func1())
        f2 = tg.create_task(func2())

    print(f1.result(), f2.result())

asyncio.run(main())
