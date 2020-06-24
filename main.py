import os
import logging

import nonebot
from nonebot.log import logger

from config import Base


if __name__ == '__main__':
    nonebot.init(Base)
    logger.setLevel(logging.WARNING)
    nonebot.load_plugins(
        os.path.join(os.path.dirname(__file__), 'plugins'),
        'plugins'
    )
    nonebot.run()
