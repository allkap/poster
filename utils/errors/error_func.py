import datetime
from config import SYSTEM_CHAT
from misc import bot
from loguru import logger


class MyError:

    def __init__(self, e, info=False, update=False):
        dt = datetime.datetime.now()
        self.info_df = f'❌ [{dt} ButlerBikes]'
        self.e = e
        self.info = info
        self.update = update

    async def error(self):
        await bot.send_message(SYSTEM_CHAT, f'{self.info_df} - {self.update}\n\n'
                                            f'{self.e}\n\n'
                                            f'{self.info}')
        logger.exception(self.e)

    async def print(self):
        await bot.send_message(SYSTEM_CHAT, f'{self.info_df} - {self.update}\n\n'
                                            f'{self.e}\n\n'
                                            f'{self.info}')
        print(self.e)
