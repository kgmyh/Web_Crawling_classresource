import aiohttp
import aiofiles
import asyncio

# pip install aiohttp

async def download_image(url):

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
            else:
                return None

async def main():
    url = "https://images.pexels.com/photos/305070/pexels-photo-305070.jpeg"
    image_data = await download_image(url)
    if image_data:
        async with aiofiles.open("image.jpg", "wb") as f:
            await f.write(image_data)
        print("Image saved successfully!")
    else:
        print("Error downloading image.")


asyncio.run(main())        