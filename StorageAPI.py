import asyncio
import requests
import base64

class StorageAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = "https://api.moysklad.ru/api/remap/1.2"

    def get_auth_headers(self):
        credentials = base64.b64encode(f"{self.username}:{self.password}".encode("utf-8")).decode("utf-8")
        headers = {
            "Authorization": f"Basic {credentials}",
            "Accept-Encoding": "gzip"
        }
        return headers

    async def get_product_names(self):
        url = f"{self.base_url}/entity/product"
        headers = self.get_auth_headers()
        response = await self.async_request(url, headers)
        json_response = response.json()
        rows = json_response["rows"]
        names = []

        tasks = []
        for row in rows:
            sale_prices = row["meta"]
            href = sale_prices["href"]
            task = asyncio.create_task(self.get_name(href, headers))
            tasks.append(task)

        names = await asyncio.gather(*tasks)
        return names

    async def get_name(self, href, headers):
        response = await self.async_request(href, headers)
        href_response = response.json()
        name = href_response["name"]
        return name

    async def async_request(self, url, headers):
        response = await asyncio.get_event_loop().run_in_executor(
            None, lambda: requests.get(url, headers=headers)
        )
        return response
