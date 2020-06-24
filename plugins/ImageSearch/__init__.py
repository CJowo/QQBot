import hashlib
import json

from nonebot import on_command, CommandSession, logger
from aiocqhttp.message import Message, MessageSegment
from aiohttp.client_exceptions import ClientConnectionError

from plugins.Admin.database import r
from . import ascii2d
from . import saucenao
from config.ImageSearch import *


__all__ = ['ascii2d', 'saucenao']

@on_command('imagesearch', aliases=('搜图', '搜图片', '图片搜索'))
async def image_search(session: CommandSession):
    image = session.get('image', prompt='图呢？')
    if image is None:
        await session.send('你发的这是什么啊')
        return

    await session.send('在找了，等一下的啦')
    file_path = await session.bot.get_image(file=image)
    results = {'saucenao': None, 'color': None, 'bovw': None}
    with open(file_path['file'], 'rb') as f: 
        md5 = hashlib.md5(f.read()).hexdigest()
    if SAUCENAO:
        try:
            cache = None
            if CACHE_TIME > 0:
                cache = r.get('ImageSearch-SauceNao-' + md5)
            if cache is not None:
                res = json.loads(cache)
            else:
                res = await saucenao.search(file_path['file'], SAUCENAO_KEY)
            if CACHE_TIME > 0:
                r.set('ImageSearch-SauceNao-' + md5, json.dumps(res), CACHE_TIME)
            results['saucenao'] = res
        except ClientConnectionError as err:
            logger.error(err)
            await error('SauceNao请求失败，请过段时间再试')
            return
    if ASCII2D:
        try:
            cache = None
            if CACHE_TIME > 0:
                cache = r.get('ImageSearch-Ascii2D-' + md5)
            if cache is not None:
                res = json.loads(cache)
            else:
                res = await ascii2d.search(file_path['file'], 'all')
            if CACHE_TIME > 0:
                r.set('ImageSearch-Ascii2D-' + md5, json.dumps(res), CACHE_TIME)
            results.update(res)
        except ClientConnectionError as err:
            logger.error(err)
            await error('Ascii2D请求失败，请过段时间再试')
            return

    for key in results:
        if results[key] is not None:
            break
    else:
        await err('无结果或请求达到限额，请过段时间或明日再试')
        return
    
    if SMART:
        results = await smart(results)

    for key in results:
        if results[key] is None: continue
        msg = Message(MessageSegment.text(f'来自{key}的结果:\n'))
        if SHOW_IMAGE:
            can_send_image = await session.bot.can_send_image()
            if can_send_image['yes']:
                msg.append((MessageSegment.image(results[key]['img'])))
                msg.append((MessageSegment.text('\n')))

        data = results[key].get('data', {})
        links = results[key].get('links', [])
        for key in data:
            msg.append(MessageSegment.text(f'{key}: {data[key]}\n'))
        msg_links = []
        for link in links:
            if link[0] != '':
                msg_links.append(link[0])
            msg_links.append(link[1])
        msg.append(MessageSegment.text('\n'.join(msg_links)))

        await session.send(msg)
    await session.send(Message(MessageSegment.at(session.event.user_id)))


@image_search.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        for i in session.event.message:
            if i['type'] == 'image':
                session.state['image'] = i['data']['file']
        return

    for i in session.event.message:
        if i['type'] == 'image':
            session.state['image'] = i['data']['file']
            break
    else:
        session.state['image'] = None


async def smart(results):
    pass
    return results

async def error(text):
    msg = Message()
    msg.append(MessageSegment.at(session.event.user_id))
    msg.append(MessageSegment.text(text))
    await session.send(msg)