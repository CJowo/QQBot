import asyncio
import os
import random

import aiohttp
from lxml import etree

import config


async def search(file, method='color'):
    """
    :param file: 待搜索的图片文件对象

    :param method:
    
    `'color'` - 颜色搜索

    `'bovw'` - 特征搜索

    `'all'` - 全部

    :return: { img: 'image_uri', links: [ ( 'text', 'href' ), ... ] }
    """
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
                    proxy=config.PROXY) as resp:
            location = resp.headers.get('location')

        path = os.path.basename(location)
        results = {}
        for m in (method, ) if method != 'all' else ('color', 'bovw'):
            async with session.get(url=f'https://ascii2d.net/search/{m}/{path}') as resp:
                return await analyze(await resp.text())


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
    return {
        'img': img,
        'links': links
    }
