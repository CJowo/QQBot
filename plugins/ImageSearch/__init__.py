from nonebot import on_command, CommandSession
from aiocqhttp.message import Message, MessageSegment

from . import ascii2d


__all__ = ['ascii2d', 'saucenao']

@on_command('imagesearch', aliases=('搜图', '搜图片', '图片搜索'))
async def image_search(session: CommandSession):
    image = session.get('image', prompt='图呢？')
    if image is None:
        await session.send('你发的这是什么啊')
    else:
        await session.send('在找了，等一下的啦')
        res = await session.bot.get_image(file=image)
        with open(res['file'], 'rb') as f:
            result = await ascii2d.search(f)

        await session.send(Message(MessageSegment.at(session.event.user_id)))

        # 检测允许发送图片则发送缩略图
        res = await session.bot.can_send_image()
        if res['yes']:
            await session.send(Message(MessageSegment.image(result['img'])))

        msg = Message()
        data = result.get('data', {})
        links = result.get('links', [])
        for key in data:
            msg.append(MessageSegment.text(f'{key}: {data[key]}\n'))
        msg_links = []
        for link in links:
            if link[0] != '':
                msg_links.append(link[0])
            msg_links.append(link[1])
        msg.append(MessageSegment.text('\n'.join(msg_links)))

        await session.send(msg)


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
