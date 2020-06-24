from nonebot import on_command, CommandSession, permission


@on_command('notice', aliases=('公告', '群发'), permission=permission.SUPERUSER)
async def notice(session: CommandSession):
    if session.event.raw_message.strip() == '#':
        await session.send('已取消')
        return

    group_list = await session.bot.get_group_list(self_id=session.event.self_id)
    fail = []
    for group in group_list:
        try:
            await session.bot.send_group_msg(group_id=group['group_id'], message=session.event.message)
        except:
            fail.append(f'{group["group_name"]}({group["group_id"]})')
    await session.send(f'已发送至{len(group_list)-len(fail)}个群聊\n失败{len(fail)}个:')


@notice.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        session.pause('下一条消息将发送至所有群，取消请发送 #')
        return