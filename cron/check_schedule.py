### use this file by cron everyminute

import asyncio
import sys

sys.path.insert(0, '/home/plan-poster')

from functions.schedule.schedule_func import ScheduleObj


async def main_check():
    await ScheduleObj().check_main()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_check())
