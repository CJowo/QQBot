import os

import nonebot

import config


if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins(
        os.path.join(os.path.dirname(__file__), 'plugins'),
        'plugins'
    )
    nonebot.run(host='127.0.0.1', port=5000)
