from loguru import logger
from functions.schedule.schedule_func import ScheduleObj, del_post_id_schedule

from database import PostPost, ScheduleMain
import datetime

from misc import bot


class PostPostObj:

    def __init__(self, post_id):
        self.post_id = int(post_id)
        self.post = PostPost.objects(post_id=self.post_id).first()

    @classmethod
    def create_post(cls, text: str):
        post = PostPost(text=text).save()
        return post.post_id

    def set_timer(self, timer):
        """After how much hours post will be send to chat

        # 168:00
        # 24:00
        """
        self.post.update(set__timer=timer)
        self.post.save()

    def set_text(self, text):
        """Message with this text will be send to chat"""
        self.post.update(set__text=text)
        self.post.save()

    def set_media(self, media):
        """Set media file id"""
        self.post.update(set__media=str(media))
        self.post.save()

    def add_chat(self, chat_id):
        """Add chat to list chats"""
        if chat_id not in self.post.chats:
            self.post.update(push__chats=int(chat_id))
            self.post.save()

    def dell_chat(self, chat_id):
        """Delete chat from list chats"""
        if chat_id in self.post.chats:
            self.post.update(pull__chats=int(chat_id))
            self.post.save()

    def set_dt_start(self, dt: datetime.datetime):
        """When post will be send firstly to the chat"""
        self.post.update(set__dt_start=dt)
        self.post.save()

    def get_dt_start(self):
        return str(self.post.dt_start)[:16]

    async def send_post(self, chat=False):
        """
        send post to chat
        :param chat: send to special chat
        :return:
        """

        text = self.post.text
        media = self.post.media

        if chat:
            await send_message_post_by_bot(chat, text, media=media)
        else:
            for chat_id in list(set(self.post.chats)):
                await send_message_post_by_bot(chat_id, text, media=media)
            self.update_last_dt()

    def update_last_dt(self, dtime=False):
        """Set datetime last post"""

        if not dtime:
            dt = str(datetime.datetime.today())[:16]
        else:
            dt = str(dtime)[:16]

        self.post.update(set__dt_last=dt)
        self.post.save()

    def update_next_dt(self, dtime=False):
        """Set datetime next post"""

        if not dtime:
            dt = str(datetime.datetime.today())[:16]
        else:
            dt = str(dtime)[:16]

        self.post.update(set__dt_next=dt)
        self.post.save()

    def delete(self):
        """Delete post_id from schedule and delete post object."""

        sched = ScheduleObj().schedule.schedule

        # schedule without post
        new_sched = del_post_id_schedule(self.post_id, sched)

        sc = ScheduleMain.objects().first()
        sc.update(set__schedule=new_sched)
        sc.save()

        PostPost.objects(post_id=self.post_id).first().delete()

    async def post_info(self, short=False):
        """

        :param short: use it when need to send short text
        :return:
        """

        chats = []

        for chat_id in self.post.chats:
            try:
                chat = await bot.get_chat(int(chat_id))
                chats.append('@' + chat.username)
            except Exception as e:
                logger.error(e)
                chats.append(f'*Чат не найден - {chat_id}')

        row_chats = '\n'.join([chat for chat in chats])

        text = f'id-{str(self.post_id)}\n\n' \
               f'Текст: {self.post.text if not short else str(self.post.text)[:int(len(self.post.text) / 2)]} ....\n\n' \
               f'Чаты: {row_chats}\n\n' \
               f'След. пост: {self.post.dt_next}\n' \
               f'Таймер: {self.post.timer}\n'
        return text


async def send_message_post_by_bot(cid, text, media=None, reply_markup=None):
    if media:
        try:
            m = await bot.send_photo(cid, media, text, reply_markup=reply_markup, parse_mode='Markdown')
            logger.info('*send message*\n'
                        f'chat: {cid}\n'
                        f'media: {True}\n'
                        f'text: {text}')
            return m
        except Exception as e:
            logger.exception(e)
    else:
        try:
            m = await bot.send_message(cid, text, reply_markup=reply_markup, parse_mode='Markdown')
            logger.info('*send message*\n'
                        f'chat: {cid}\n'
                        f'media: {False}\n'
                        f'text: {text}')
            return m
        except Exception as e:
            logger.exception(e)

    return
