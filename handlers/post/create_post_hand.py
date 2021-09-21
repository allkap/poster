import datetime
from functions.post.post_func import PostPostObj
from functions.schedule.schedule_func import ScheduleObj
from functions.user.user_func import UserObj, check_status
from keyboards import keyb
from misc import bot, dp


@dp.callback_query_handler(lambda call: call.data == 'Создать_пост')
async def main_plan_menu(call):
    uid = call.from_user.id
    await bot.send_message(uid, 'Пришлите текст поста:', reply_markup=keyb.cancel())
    user = UserObj(uid)
    user.set_status('Ждем текст для поста')


@dp.message_handler(lambda msg: check_status(msg.from_user.id) == 'Ждем текст для поста')
async def create_post_hand(msg):
    uid = msg.from_user.id
    text = msg.text
    await bot.send_message(uid, 'Пришлите чаты начиная с @ через , в которых будет пост:', reply_markup=keyb.cancel())
    post_id = PostPostObj.create_post(text=text)
    user = UserObj(uid)
    user.set_status(f'Ждем чаты для поста;{post_id}')


@dp.message_handler(lambda msg: check_status(msg.from_user.id).split(';')[0] == 'Ждем чаты для поста')
async def wait_chats_post(msg):
    uid = msg.from_user.id
    chats = msg.text
    user = UserObj(uid)
    post_id = user.status().split(';')[1]
    post = PostPostObj(post_id)
    if '@' in chats:
        for chat_uname in chats.split(', '):
            chat = await bot.get_chat(chat_uname)
            chat_id = chat.id

            post.add_chat(chat_id)

        await bot.send_message(uid, 'Напишите дату время первого поста в формате: 21.03.2021 10:30')
        user.set_status(f'Ждем датувремя первого поста;{post_id}')
    else:
        await bot.send_message(uid, 'Не могу найти @ в тексте')


@dp.message_handler(lambda msg: check_status(msg.from_user.id).split(';')[0] == 'Ждем датувремя первого поста')
async def wait_dt_first_post(msg):
    uid = msg.from_user.id
    dt = msg.text

    user = UserObj(uid)
    post_id = user.status().split(';')[1]
    post = PostPostObj(post_id)

    dt_save = datetime.datetime.strptime(dt, f'%d.%m.%Y %H:%M')
    post.set_dt_start(dt_save)

    await bot.send_message(uid, 'Напишите через какое время пост будет публиковаться снова, например:'
                                '24:00 - раз в сутки\n'
                                '168:00 - раз в неделю\n\n'
                                '0 - разовый пост')

    user.set_status(f'Ждем таймер поста;{post_id}')


@dp.message_handler(lambda msg: check_status(msg.from_user.id).split(';')[0] == 'Ждем таймер поста')
async def wait_timer_first_post(msg):
    uid = msg.from_user.id
    timer = msg.text

    user = UserObj(uid)
    post_id = user.status().split(';')[1]

    post = PostPostObj(post_id)
    post.set_timer(timer)

    await bot.send_message(uid, 'Добавить медиа?', reply_markup=keyb.add_media_post(post_id))


@dp.callback_query_handler(lambda call: call.data.split(';')[0] == 'Добавить_медиа')
async def add_media_menu_hand(call):
    uid = call.from_user.id
    post_id = call.data.split(';')[1]
    user = UserObj(uid)

    await bot.send_message(uid, 'Пришлите мне фото для поста\n\n'
                                'Когда пришлете все фото и дождетесь загрузки - нажмите кнопку 👇',
                           reply_markup=keyb.finish_media(post_id))

    user.set_status(f'Ждем_медиа_пост;{post_id}')


@dp.callback_query_handler(lambda call: call.data.split(';')[0] == 'Завершить_медиа')
async def finish_media_post(call):
    uid = call.from_user.id

    post_id = call.data.split(';')[1]
    post = PostPostObj(post_id)

    await post.send_post(uid)

    await bot.send_message(uid, 'Подтвердить пост?', reply_markup=keyb.apply_post(post_id))

    user = UserObj(uid)
    user.set_status('pass')


@dp.callback_query_handler(lambda call: call.data.split(';')[0] == 'Пропустить_медиа')
async def miss_media_menu(call):
    uid = call.from_user.id
    post_id = call.data.split(';')[1]
    post = PostPostObj(post_id)

    await post.send_post(uid)

    await bot.send_message(uid, 'Подтвердить пост?', reply_markup=keyb.apply_post(post_id))


@dp.callback_query_handler(lambda call: call.data.split(';')[0] == 'Подтвердить_пост')
async def apply_plan_menu(call):
    uid = call.from_user.id
    post_id = call.data.split(';')[1]
    post = PostPostObj(post_id)

    # push post to schedule
    await ScheduleObj().update_schedule(post, True)

    await post.send_post(post)
    await bot.send_message(uid, 'Подтверждено и добавлено в рассписание.', reply_markup=keyb.admin_panel())
