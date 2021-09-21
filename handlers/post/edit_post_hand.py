import datetime

from database import PostPost
from functions.post.post_func import PostPostObj
from functions.schedule.schedule_func import ScheduleObj
from functions.user.user_func import UserObj, check_status
from keyboards import keyb
from misc import dp, bot
import asyncio
from loguru import logger


@dp.callback_query_handler(lambda call: call.data.split(';')[0] == 'Изменить_пост')
async def change_post_menu(call):
    uid = call.from_user.id

    post_id = call.data.split(';')[1]
    post = PostPostObj(post_id)

    await post.send_post(uid)
    await bot.send_message(uid, f'Панель редактирования\n\n', reply_markup=keyb.edit_post(post_id))


@dp.callback_query_handler(lambda call: call.data == 'Изменить_посты')
async def change_posts_menu(call):
    uid = call.from_user.id
    cid = call.message.chat.id

    for post in PostPost.objects():
        try:
            post_obj = PostPostObj(post.post_id)
            post_info = await post_obj.post_info(True)
            await post_obj.send_post(cid)
            await bot.send_message(uid, f'Панель редактирования\n\n{post_info}',
                                   reply_markup=keyb.edit_post(post.post_id))
        except Exception as e:
            logger.exception(e)
            await bot.send_message(uid, f'Ошибка при отображении поста'
                                        f' id-{post.post_id} в планировщике - {e}')
        await asyncio.sleep(0.3)


@dp.callback_query_handler(lambda call: call.data.split(';')[0] == 'Точно_удалить_пост')
async def change_post_menu(call):
    uid = call.from_user.id

    act = call.data.split(';')[1]
    post_id = call.data.split(';')[2]
    post = PostPostObj(post_id)

    if act == 'Да':
        post.delete()
        await bot.send_message(uid, 'Пост удалён')
    else:
        await bot.send_message(uid, f'Панель редактирования\n\n{post.post_info(True)}',
                               reply_markup=keyb.edit_post(post_id))


@dp.callback_query_handler(lambda call: call.data.split(';')[0] == 'Ch_post')
async def change_post_menu(call):
    uid = call.from_user.id

    act = call.data.split(';')[1]
    post_id = call.data.split(';')[2]

    user = UserObj(uid)
    if act == 'Текст':
        await bot.send_message(uid,
                               'Пришлите новые текст для поста:',
                               reply_markup=keyb.back_to_edit_post(post_id))
        user.set_status(f'Ждем новый текст поста;{post_id}')
    elif act == 'Таймер':
        await bot.send_message(uid,
                               'Пришлите новый таймер в формате: 24:00 или 72:00',
                               reply_markup=keyb.cancel())
        user.set_status(f'Ждем новый таймер поста;{post_id}')
    elif act == 'Удалить':
        await bot.send_message(uid, 'Точно удалить пост?', reply_markup=keyb.ex_dell_post(post_id))
    elif act == 'Дата_старта':
        await bot.send_message(uid,
                               'Напишите дату время первого поста в формате: 21.03.2021 10:30',
                               reply_markup=keyb.back_to_edit_post(post_id))
        user.set_status(f'Ждем датувремя первого поста new;{post_id}')
    elif act == 'Медиа':
        await bot.send_message(uid, 'Пришлите медиа для поста:', reply_markup=keyb.back_to_edit_post(post_id))
        user.set_status(f'Ждем_медиа_пост_new;{post_id}')
    elif act == 'Чат':
        await bot.send_message(uid, 'Выберите действие', reply_markup=keyb.ch_post_chat_act(post_id))


@dp.callback_query_handler(lambda call: call.data.split(';')[0] == 'EDIT')
async def apply_plan_menu(call):
    uid = call.from_user.id

    act = call.data.split(';')[1]
    act_callback = call.data.split(';')[2]
    post_id = call.data.split(';')[3]

    post = PostPostObj(post_id)
    user = UserObj(uid)

    if act == 'act_dell_post':
        act_dell = True if act_callback == 'True' else False
        post.set_act_delete(act_dell)
    elif act == 'Добавить_чат':
        await bot.send_message(uid, 'Пришлите ссылку на чат для добавления, начиная с @',
                               reply_markup=keyb.back_to_edit_post(post_id))
        user.set_status(f'Ждем ссылку на новый чат для поста;{post_id}')
    else:
        await bot.send_message(uid, 'Пришлите ссылку на чат для удаления, начиная с @',
                               reply_markup=keyb.back_to_edit_post(post_id))
        user.set_status(f'Ждем ссылку на чат для удаления блока;{post_id}')
    # await bot.send_message(uid, 'Сохранено!', reply_markup=keyb.admin_keyb())


@dp.message_handler(lambda msg: check_status(msg.from_user.id).split(';')[0] == 'Ждем ссылку на новый чат для поста')
async def new_chat_post_hand(msg):
    uid = msg.from_user.id
    chats = msg.text

    user = UserObj(uid)
    post_id = user.status().split(';')[1]
    post = PostPostObj(post_id)

    if '@' in chats:
        for chat_uname in chats.split(', '):
            chat = await bot.get_chat(chat_uname)
            post.add_chat(chat.id)
        await bot.send_message(uid, 'Сохранено!', reply_markup=keyb.edit_post(post_id))
        UserObj(uid).set_status('pass')
    else:
        await msg.answer(uid, 'Не нашли такой чат в нашей базе @ChatikRobot')


@dp.message_handler(lambda msg: check_status(msg.from_user.id).split(';')[0] == 'Ждем датувремя первого поста new')
async def wait_dt_new_post(msg):
    uid = msg.from_user.id
    dt = msg.text

    user = UserObj(uid)
    post_id = user.status().split(';')[1]
    post = PostPostObj(post_id)

    dt_save = datetime.datetime.strptime(dt, f'%d.%m.%Y %H:%M')
    post.set_dt_start(dt_save)
    post = PostPostObj(post_id)

    await post.send_post(uid)

    await ScheduleObj().update_schedule(post, True)

    await bot.send_message(uid, 'Сохранено!')
    user.set_status('pass')


@dp.message_handler(lambda msg: check_status(msg.from_user.id).split(';')[0] == 'Ждем новый текст поста')
async def wait_new_text_post(msg):
    uid = msg.from_user.id

    user = UserObj(uid)
    post_id = user.status().split(';')[1]
    post = PostPostObj(post_id)
    post.set_text(msg.text)
    post = PostPostObj(post_id)

    await post.send_post(uid)
    user.set_status('pass')

    post_info = await post.post_info(True)
    await bot.send_message(uid, f'Панель редактирования\n\n'
                                f'{post_info}', reply_markup=keyb.edit_post(post_id))


@dp.message_handler(lambda msg: check_status(msg.from_user.id).split(';')[0] == 'Ждем новый таймер поста')
async def wait_new_text_post(msg):
    uid = msg.from_user.id

    user = UserObj(uid)
    post_id = user.status().split(';')[1]
    post = PostPostObj(post_id)
    post.set_timer(msg.text)
    post = PostPostObj(post_id)

    await post.send_post(uid)
    user.set_status('pass')

    post_info = await post.post_info(True)
    await bot.send_message(uid, f'Панель редактирования\n\n'
                                f'{post_info}', reply_markup=keyb.edit_post(post_id))


@dp.message_handler(lambda msg: check_status(msg.from_user.id).split(';')[0] == 'Ждем новый таймер поста')
async def wait_new_text_post(msg):
    uid = msg.from_user.id

    user = UserObj(uid)
    post_id = user.status().split(';')[1]
    post = PostPostObj(post_id)
    post.set_timer(msg.text)
    post = PostPostObj(post_id)

    await post.send_post(uid)
    user.set_status('pass')

    post_info = await post.post_info(True)
    await bot.send_message(uid, f'Панель редактирования\n\n'
                                f'{post_info}', reply_markup=keyb.edit_post(post_id))
