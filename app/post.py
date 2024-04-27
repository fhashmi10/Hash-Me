import aiohttp
import requests
    
post_urla='http://127.0.0.1:5000/predict'

class Post():
    
    async def post_async(post_url, json_data):
        async with aiohttp.ClientSession() as session:
            async with session.post(post_urla, json=json_data) as resp:
                result = await resp.json(content_type='text/html')
                print(result.text)

    def post_sync(post_url, json_data):
        result = requests.post(post_urla, json=json_data)
        return result.text