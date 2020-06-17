from nonebot import on_command, CommandSession

@on_command('notice', aliases=('公告', '群发'))
async def notice(session: CommandSession):
    if session.event.raw_message.strip() == '#':
        await session.send('已取消')
        return

    group_list = await session.bot.get_group_list(self_id=session.event.self_id)
    for group in group_list:
        await session.bot.send_group_msg(group_id=group['group_id'], message=session.event.message)
    await session.send(f'已发送至{len(group_list)}个群聊')


@notice.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        session.pause('下一条消息将发送至所有群，取消请发送 #')
        return