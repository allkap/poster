import datetime
from database import ScheduleMain
from utils.errors.error_func import MyError
from functions.post.post_func import PostPostObj
from loguru import logger


class ScheduleObj:
    """Schedule will be checked every minute.
    Send post if find datetime in schedule."""

    def __init__(self):
        self.schedule = ScheduleMain.objects().first()

    async def check_main(self):
        """Main check schedule. Use from cron."""

        # list posts for sending
        list_posts_id: list = self.check_sched()

        if list_posts_id:
            for post_id in list_posts_id:
                try:
                    post = PostPostObj(post_id)
                    await post.send_post()
                except Exception as e:
                    # send error by other bot
                    await MyError(e, 'check_main').error()

    def check_sched(self) -> list:
        """Проверяем сначала есть ли дата в рассписании, если есть, то
         проверяем дату_и_время"""

        sched = self.check_date()
        if sched:
            sched_fin = self.check_datetime()
            return sched_fin

        return False

    def check_date(self):
        """Проверяем есть ли сегодняшняя дата в рассписании
        Возвращаем self если есть иначе False"""

        date_now = str(datetime.datetime.today().date())
        if date_now in self.schedule.schedule.keys():
            return self
        return False

    def check_datetime(self):
        """Проверяем есть ли datetime now
        в ключах schedule[date_now]

        :return list(posts_id) or False"""

        date_now = str(datetime.datetime.today().date())[:16]
        dt_now = str(datetime.datetime.today())[:16]

        if dt_now in self.schedule.schedule[date_now].keys():
            logger.info(f'*find dt* | {dt_now}')
            return self.schedule.schedule[date_now][dt_now]

        return False

    async def update_schedule(self, post: PostPostObj, new=False):
        """Push post_id to schedule"""
        try:
            datetime_next = gen_datetime_next(post) if not new else post.get_dt_start()

            updated_schedule = add_post_id_schedule(post.post_id, self.schedule.schedule, datetime_next)

            self.schedule.update(set__schedule=updated_schedule)
            self.schedule.save()

            if new:
                post = PostPostObj(post.post_id)
                post.update_next_dt(datetime_next)
        except Exception as e:
            await MyError(e, 'update_schedule').error()


def add_post_id_schedule(post_id: int, schedule: dict, dt_post: datetime.datetime) -> dict:
    """Функция которая добавляет пост в рассписание
    или создает новую дату и датувремя если такой нет в рассписании"""
    date = str(dt_post)[:10]
    dt_post = str(dt_post)

    try:
        if date in schedule.keys():  # Если есть рассписание на эту дату
            if dt_post in schedule[date].keys():  # Если есть такое датавремя в рассписании
                # Добавляем в список постов на эту датувремя
                schedule[date][dt_post].append(post_id) if post_id not in schedule[date][dt_post] else ''
            else:  # Если нету датывремя
                schedule[date][dt_post] = [post_id]  # Создаем словарь с дата время и ложим туда ид поста

        else:  # Если на эту дату нет ничего в рассписании
            schedule[date] = {dt_post: [post_id]}  # Создаем словарь с датой и датойвременем ложим туда ид поста

    except Exception as e:
        logger.exception(e)
    finally:
        return schedule


def del_post_id_schedule(post_id_main: int, schedule: dict) -> dict:
    new_sc = {}

    for date, dict_dt in schedule.items():
        new_dict = {}
        for dt, list_posts in dict_dt.items():
            new_list = [post_id for post_id in list_posts if post_id != post_id_main]
            new_dict[dt] = new_list
        new_sc[date] = new_dict

    return new_sc


def gen_datetime_next(post) -> str:
    """Generate datetime for next post"""
    dt_last = post.post.dt_last
    timer = post.post.timer

    next_hour = int(timer.split(':')[0])
    next_min = int(timer.split(':')[1])

    dt_new = dt_last + datetime.timedelta(hours=next_hour, minutes=next_min)
    return str(dt_new)[:16]


async def main_check():
    await ScheduleObj().check_main()


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_check())
