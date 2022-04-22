from aiohttp import ClientSession


class Requests(object):
    def __init__(self, headers=None):
        self.headers = headers if headers else {}

    async def request(self, method, url, params=None, json=None, data=None, headers=None, verify_ssl=False, **kwargs):
        if headers:
            self.headers.update(headers)

        async with ClientSession() as session:
            async with session.request(method, url, json=json, data=data, verify_ssl=verify_ssl, params=params,
                                       headers=self.headers, **kwargs) as response:
                return await response.json()

    async def get(self, url, params=None, headers=None, verify_ssl=False, **kwargs):
        return await self.request('GET', url, params=params, headers=headers, verify_ssl=verify_ssl, **kwargs)

    async def post(self, url, json=None, data=None, headers=None, verify_ssl=False, **kwargs):
        return await self.request('POST', url, json=json, data=data, headers=headers, verify_ssl=verify_ssl, **kwargs)

    async def put(self, url, json=None, data=None, headers=None, verify_ssl=False, **kwargs):
        return await self.request('PUT', url, json=json, data=data, headers=headers, verify_ssl=verify_ssl, **kwargs)

    async def delete(self, url, headers=None, verify_ssl=False, **kwargs):
        return await self.request('DELETE', url, headers=headers, verify_ssl=verify_ssl, **kwargs)

    async def patch(self, url, json=None, data=None, headers=None, verify_ssl=False, **kwargs):
        return await self.request('PATCH', url, json=json, data=data, headers=headers, verify_ssl=verify_ssl, **kwargs)
