import time
import json

import aiohttp
from nonebot import on_command, CommandSession

Cache = {}

Url = 'https://service-kjcbcnmw-1254119946.gz.apigw.tencentcs.com//'

Headers = {
    'Content-Type': 'application/json',
    'Custom-Source': 'CJ-Bot',
    'Host': 'service-kjcbcnmw-1254119946.gz.apigw.tencentcs.com',
    'Origin': 'https://kyouka.kengxxiao.com',
    'Referer': 'https://kyouka.kengxxiao.com/'

}

@on_command('pcrguild', aliases=('line', '档线'))
async def pcrguild(session: CommandSession):
    rank = session.get('rank', prompt='请输入要查询的档线')
    if rank not in ('3', '10', '20', '50', '200', '600', '1200', '2800', '5000', '10000', '15000', '25000', '40000', '60000'):
        await session.send('档线不存在')
    else:
        line, t = await get_line(rank)
        if t != 0:
            await session.send(f'{t} {rank}档线:\n{line}')
        else:
            session.send(line)



@pcrguild.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['rank'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('请输入要查询的档线')

    session.state[session.current_key] = stripped_arg


async def get_line(rank):
    global Cache
    if time.time() - Cache.get('timestamp', 0) > 86400:
        Cache = {'timestamp': None, 'data': {}}
        history_list = await get_history_list()
        if history_list.get('code') != 0:
            return f'请求出错 code:{line_data.get("code")}', 0
        history = history_list.get('history', [])
        if len(history) == 0:
            return '获取历史数据失败', 0
        line_data = await get_line_data(history[-1])
        if line_data.get('code') != 0:
            return f'请求出错 code:{line_data.get("code")}', 0
        data = line_data.get('data', [])
        for i in data:
            _rank = i.get('rank')
            damage = i.get('damage', 0)
            _round, boss, hp = await damage_to_bossinfo(damage)
            Cache['data'][str(_rank)] = f'{_round}周目{boss}王 剩余{hp}HP'
        ts = line_data.get('ts', 0)
        Cache['timestamp'] = ts
    return Cache['data'].get(rank, '无数据'), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(Cache.get('timestamp', 0)))


async def damage_to_bossinfo(damage):
    scoreRate = (
        (1, 1, 1.1, 1.1, 1.2),
        (1.2, 1.2, 1.5, 1.7, 2),
    )
    bossHp = (6000000, 8000000, 10000000, 12000000, 20000000)
    _round = 0
    boss = 0
    hp = 0
    flag = True
    while flag:
        _round += 1
        if _round == 1:
            sr = scoreRate[0]
        else:
            sr = scoreRate[1]
        for idx, (rate, bh) in enumerate(zip(sr, bossHp)):
            if damage < bh * rate:
                boss = idx + 1
                hp = int(bh - damage / rate)
                flag = False
                break
            else:
                damage -= bh * rate
    return _round, boss, hp


async def get_history_list():
    async with aiohttp.ClientSession() as aiohttp_session:
        async with aiohttp_session.get(
                    url=Url+'default',
                    headers=Headers) as resp:
            return json.loads(await resp.text())


async def get_line_data(timestamp):
    async with aiohttp.ClientSession() as aiohttp_session:
        async with aiohttp_session.post(
                    url=Url+'line',
                    headers=Headers,
                    data=json.dumps({'history': timestamp})) as resp:
            return json.loads(await resp.text())