from nonebot import on_command, CommandSession, permission

@on_command('help', aliases=('帮助'))
async def notice(session: CommandSession):
    await session.send('帮助详见: https://github.com/CJowo/QQBot/blob/master/doc/help.md')
