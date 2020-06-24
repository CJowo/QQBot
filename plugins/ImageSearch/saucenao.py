import os
import json
import random

import aiohttp

from config.ImageSearch import PROXY


async def search(file_path, api_key: str):
    """
    :param file: 待搜索的图片文件对象

    :param api_key: saucenao账号api密钥

    :return: 
    ```python
    {
        img: 'image_uri',
        similarity: '00.00',
        links: [ ( 'text', 'href' ), ... ],
        data: { 'key': str or num, ... }
    }
    ```
    """
    with open(file_path, 'rb') as file:
        multipartWriter = aiohttp.MultipartWriter('mixed')
        multipartWriter.append('2').set_content_disposition('form-data', name='output_type')
        multipartWriter.append(api_key).set_content_disposition('form-data', name='api_key')
        multipartWriter.append('1').set_content_disposition('form-data', name='numres')
        multipartWriter.append(file, {'Content-Type': 'image/*'}) \
            .set_content_disposition(
                'form-data',
                name = 'file',
                filename = str(random.random())
            )
        headers = {"Content-Type": f"multipart/form-data;boundary={multipartWriter.boundary}"}

        async with aiohttp.ClientSession() as session:
            async with session.post(url='https://saucenao.com/search.php', data=multipartWriter, headers=headers, proxy=PROXY) as resp:
                return await analyze(await resp.text())


async def analyze(text):
    res = json.loads(text)
    if res.get('header').get('status') != 0:
        return None
    results = res.get('results', [])
    if len(results) < 1:
        return None
    result = results[0]
    data = {
        key: result['data'][key] for key in result['data'] if key != 'ext_urls'
    }
    return {
        'img': result['header']['thumbnail'],
        'similarity': result['header']['similarity'],
        'links': [
            ('', i) for i in result['data'].get('ext_urls', [])
        ],
        'data': data
    }
