import asyncio
from python_gelbooru import AsyncGelbooru

api_key, user_id = ("haha_not", "telling_you")
async def main():
    async with AsyncGelbooru(api_key=api_key,
                             user_id=user_id) as gel:
        yuyu = await gel.search_posts(['saigyouji yuyuko', 'rating:explicit'], limit=10, random=True)
       

        tasks = [i.async_download(f"./arts/{i.id}") for i in yuyu]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())