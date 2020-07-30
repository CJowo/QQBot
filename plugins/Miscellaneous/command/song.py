import json

from nonebot import on_command, CommandSession, permission
import aiohttp
from aiocqhttp.message import Message, MessageSegment

@on_command('song', aliases=('点歌'))
async def song(session: CommandSession):
    keywords = session.current_arg_text.strip()

    if keywords == '':
        return await session.send('缺少关键字', at_sender=True)

    url = 'http://music.163.com/api/search/pc'
    headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,zh;q=0.8,zh-CN;q=0.7,zh-HK;q=0.6,zh-TW;q=0.5,ja;q=0.4',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Host': 'music.163.com',
        'Upgrade-Insecure-Requests': '1',

    }
    data={
        's':keywords,
        'type':1,
        'limit':1
    }
    
    await session.send('请稍后', at_sender=True)

    async with aiohttp.ClientSession() as aiohttp_session:
        async with aiohttp_session.post(
                    url=url,
                    data=data,
                    headers=headers,
                    allow_redirects=False) as resp:
        
            res_obj = json.loads(await resp.text())
            if 'result' not in res_obj:
                return await session.send('功能异常，请联系管理员处理', at_sender=True)
        
            result = res_obj.get('result')
            if 'songs' not in result:
                return await session.send('功能异常，请联系管理员处理', at_sender=True)
    
            songs = result.get('songs')
            if len(songs) < 1:
                return await session.send('未找到歌曲', at_sender=True)

            msg = Message(MessageSegment.music(type_='163', id_=songs[0].get('id')))
            await session.send(msg)

