import asyncio
import time

def blocking_io(sleep_time):
    print(f"start blocking_io at {time.strftime('%X')}")
    time.sleep(sleep_time)
    print(f"blocking_io complete at {time.strftime('%X')}")
async def blocking_io_with_async(sleep_time):
    print(f"start blocking_io with async at {time.strftime('%X')}")
    await asyncio.sleep(sleep_time)
    print(f"blocking_io with async complete at {time.strftime('%X')}")

async def main():
    # thread_task = asyncio.create_task(asyncio.to_thread(blocking_io, 30))   # THREAD TASK
    thread_task = asyncio.create_task(blocking_io_with_async(30))  # NON THREAD TASK


    print(f"started main at {time.strftime('%X')}")

    # Await the to_thread call directly
    await asyncio.sleep(1)
    print(f"after 1 second  : {time.strftime('%X')}")
    await asyncio.sleep(3)
    print(f"after 3 second  : {time.strftime('%X')}")
    print("below to thread await")
    await thread_task  # Pass `sleep_time=2`
                   # Async sleep

    print(f"finished main at {time.strftime('%X')}")

# Run the async main function
asyncio.run(main())