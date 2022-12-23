import asyncio
import time

async def get_cancellable(timeout:float, txt:str):
    try:
        await asyncio.sleep(timeout)
        return txt
    except asyncio.CancelledError:
        return "Cancelled"

async def main5():
    task2 = asyncio.create_task(get_cancellable(2, "Task2"))
    task1 = asyncio.create_task(get_cancellable(1, "Task1"))

    print(time.strftime("%X"), "Tasks started")
    txt = await task1
    print(time.strftime("%X"), txt)
    if txt == 'Task1':
        task2.cancel()
    txt = await task2
    print(time.strftime('%X')) 

async def get_timeout(timeout:float, txt:str):
    await asyncio.sleep(timeout)
    return txt

async def main4():
    print(time.strftime("%X"))

    task1 = asyncio.create_task(get_timeout(2, "Task1"))
    task2 = asyncio.create_task(get_timeout(1, "Task2"))

    print(await task2)
    print(await task1)

    print("Tasks finished")
    print(time.strftime("%X"))

async def print_timeout(timeout:float, txt:str):
    await asyncio.sleep(timeout)
    print(txt)

async def main3():
    task1 = asyncio.create_task(print_timeout(2, "Task1"))
    task2 = asyncio.create_task(print_timeout(1, "Task2"))

    print("Tasks started")

    await task1
    await task2

    print("Tasks finished")

'''
НЕПРАВИЛЬНЫЙ КУСОК КОДА
async def main4() :                   
  print( "Tasks started" )            
  await print_timeout( 2, "Task1" )   
  await print_timeout( 1, "Task2" )   
  print( "Tasks finished" )           
'''

async def main2():
    await asyncio.sleep(2)
    print("Async 2 demo")

async def main1():
    print("Async demo")

if __name__ == "__main__":
    #asyncio.run(main2())
    #asyncio.run(main1())
    asyncio.run(main3())
    asyncio.run(main4())
    asyncio.run(main5())