import random

from nonebot import on_command, CommandSession


@on_command('roll', aliases=('掷点', '骰子'))
async def roll(session: CommandSession):
    r = session.state.get('range').lower().split('d')
    if r[0] == '': r[0] = '1'
    if len(r) != 2 or not r[0].isdigit() or not r[1].isdigit():
        await session.send('参数不正确', at_sender=True)
    elif int(r[0]) > 10 or int(r[1]) > 1000 or int(r[1]) == 0:
        await session.send('参数超出范围', at_sender=True)
    else:
        res = 0
        for i in range(int(r[0])):
            res +=  random.randint(1, int(r[1]))
        await session.send(str(res), at_sender=True)


@roll.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['range'] = stripped_arg
        else:
            session.state['range'] = '1d100'
        return
    