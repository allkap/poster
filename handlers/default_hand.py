import asyncio

from aiogram.types import Message

from config import ADM_IDS
from functions.post.post_func import PostPostObj
from functions.user.user_func import UserObj
from keyboards import keyb
from misc import bot, dp


@dp.message_handler(commands=['start'])
async def start_hand(msg: Message):
    uid = msg.from_user.id
    await msg.answer('Если ты админ - напиши боту /admin')
    UserObj.create_user(uid, msg.from_user.full_name)


@dp.message_handler(commands=['admin'])
async def start_hand(msg: Message):
    uid = msg.from_user.id
    if uid in ADM_IDS:
        await msg.answer('Панель админа:', reply_markup=keyb.admin_panel())
        UserObj.create_user(uid, msg.from_user.full_name)
        UserObj(uid).set_status('pass')


@dp.message_handler(content_types=['photo'])
async def photos_hand(msg: Message):
    uid = msg.from_user.id
    photo = msg.photo[-1].file_id

    user = UserObj(uid)
    status = user.status()

    if len(status.split(';')) > 1:
        post_id = status.split(';')[1]
        post = PostPostObj(post_id)

        act = status.split(';')[2]
        if act == 'Ждем_медиа_пост':
            post.set_media(photo)
            await msg.answer('Сохранено!')
