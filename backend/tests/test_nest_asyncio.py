import asyncio
import nest_asyncio

async def test_nested_async():
    print("Testing nest_asyncio...")
    nest_asyncio.apply()
    
    async def inner_async():
        await asyncio.sleep(1)
        return "Inner async works!"
    
    outer_result = await inner_async()
    print(outer_result)

if __name__ == "__main__":
    asyncio.run(test_nested_async()) 