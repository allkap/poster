from functions.post.post_func import PostPostObj
from functions.schedule.schedule_func import ScheduleObj
from keyboards import keyb
from misc import bot, dp


@dp.callback_query_handler(lambda call: call.data == 'Рассписание')
async def schedule_menu_hand(call):
    uid = call.from_user.id
    schedule = ScheduleObj()
    await bot.send_message(uid, 'Рассписание:', reply_markup=keyb.week_schedule(schedule))


@dp.callback_query_handler(lambda call: call.data.split(';')[0] == 'Schedule_day')
async def schedule_day_menu_hand(call):
    uid = call.from_user.id
    date = call.data.split(';')[1]
    schedule = ScheduleObj()
    await bot.send_message(uid, 'Рассписание:', reply_markup=keyb.day_schedule(date, schedule))


@dp.callback_query_handler(lambda call: call.data.split(';')[0] == 'Post_menu')
async def post_menu_hand(call):
    uid = call.from_user.id
    post_id = call.data.split(';')[1]
    try:
        post_obj = PostPostObj(post_id)
        await post_obj.send_post(uid)
        await bot.send_message(uid, f'Панель редактирования\n\n'
                                    f'{post_obj.post_info()}', reply_markup=keyb.edit_post(post_id))

    except Exception as e:
        await bot.send_message(uid, f'Ошибка при отображении поста'
                                    f' id-{post_id} в планировщике - {e}')

