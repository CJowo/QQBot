from datetime import datetime, timezone, timedelta
import json

import aiohttp
from nonebot import on_command, CommandSession

History = {}

ScoreRate = (
    (1, 1, 1.1, 1.1, 1.2),
    (1.2, 1.2, 1.5, 1.7, 2),
)

BossHp = (6000000, 8000000, 10000000, 12000000, 20000000)

@on_command('pcrguild', aliases=('line', '档线'))
async def pcrguild(session: CommandSession):
    rank = session.get('rank', prompt='请输入要查询的档线')
    if rank not in ('3', '10', '20', '50', '200', '600', '1200', '2800', '5000', '10000', '15000', '25000', '40000', '60000'):
        await session.send('档线不存在')
    else:
        line, t = await get_line(rank)
        await session.send(f'{t} {rank}档线:\n{line}')



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
    global History, ScoreRate, BossHp
    time = await get_time()
    timestamp = int(time.timestamp())
    if timestamp != History.get('timestamp'):
        History = {'timestamp': None, 'data': {}}

        url = 'https://service-kjcbcnmw-1254119946.gz.apigw.tencentcs.com//line'
        headers = {
            'Content-Type': 'application/json',
            'Origin': 'https://kyouka.kengxxiao.com',
            'Referer': 'https://kyouka.kengxxiao.com/',
            'Host': 'service-kjcbcnmw-1254119946.gz.apigw.tencentcs.com'
        }
        data = {'history': timestamp}
        async with aiohttp.ClientSession() as aiohttp_session:
            async with aiohttp_session.post(
                        url=url,
                        headers=headers,
                        data=json.dumps(data)) as resp:
                res_obj = json.loads(await resp.text())
            if res_obj.get('code') != 0:
                return f'请求出错 code:{res_obj.get("code")}', time.strftime('%Y-%m-%d %H:%M:%S')
            data = res_obj.get('data', [])
            for i in data:
                _rank = i.get('rank')
                damage = i.get('damage', 0)
                _round = 0
                boss = 0
                hp = 0
                flag = True
                while flag:
                    _round += 1
                    if _round == 1:
                        sr = ScoreRate[0]
                    else:
                        sr = ScoreRate[1]
                    for idx, (rate, bh) in enumerate(zip(sr, BossHp)):
                        if damage < bh * rate:
                            boss = idx + 1
                            hp = int(bh - damage / rate)
                            flag = False
                            break
                        else:
                            damage -= bh * rate
                    
                History['data'][str(_rank)] = f'{_round}周目{boss}王 剩余{hp}HP'
        History['timestamp'] = timestamp
    return History['data'].get(rank, '无数据'), time.strftime('%Y-%m-%d %H:%M:%S')


async def get_time():
    now = datetime.now(tz=timezone(timedelta(hours=8)))
    now -= timedelta(seconds=18000)
    return now.replace(hour=5, minute=0, second=1)
    