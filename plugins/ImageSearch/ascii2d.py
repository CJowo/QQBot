import asyncio
import os
import random

import aiohttp
from lxml import etree

from config.ImageSearch import PROXY


async def search(file_path, method='color'):
    """
    :param file: 待搜索的图片文件路径

    :param method:
    
    `'color'` - 颜色搜索

    `'bovw'` - 特征搜索

    `'all'` - 全部

    :return:
    ```python
    { ascii2d_color: { img: 'image_uri', links: [ ( 'text', 'href' ), ... ] }, ascii2d_bovw: { ... } }
    ```
    """
    with open(file_path, 'rb') as file:
        multipartWriter = aiohttp.MultipartWriter('mixed')
        multipartWriter.append(file, {'Content-Type': 'image/*'}) \
            .set_content_disposition(
                'form-data',
                name='file',
                filename=str(random.random())
            )
        headers = {"Content-Type": f"multipart/form-data;boundary={multipartWriter.boundary}"}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                        url='https://ascii2d.net/search/file',
                        data=multipartWriter,
                        headers=headers,
                        allow_redirects=False,
                        proxy=PROXY()) as resp:
                location = resp.headers.get('location')
            if location is None: return None

            path = os.path.basename(location)
            results = {'ascii2d_color': None, 'ascii2d_bovw': None}
            for m in (method, ) if method != 'all' else ('color', 'bovw'):
                async with session.get(url=f'https://ascii2d.net/search/{m}/{path}', proxy=PROXY()) as resp:
                    results['ascii2d_'+m] = await analyze(await resp.text())
            return results


async def analyze(text):
    html = etree.HTML(text)
    results = html.xpath('/html/body/div/div/div[1]/div[@class="row item-box"]')
    if len(results) < 2:
        return None
    img = 'https://ascii2d.net' + results[1].xpath('./div[1]/img/@src')[0]
    a = results[1].xpath('./div[2]//a')
    links = [
        (i.xpath('./text()')[0], i.xpath('./@href')[0]) for i in a
    ]
    if len(links) == 0: return None
    return {
        'img': img,
        'links': links
    }
