from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import datetime


def admin_panel():
    keyb = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Создать пост', callback_data='Создать_пост')
    but2 = InlineKeyboardButton('Изменить посты', callback_data='Изменить_посты')
    but6 = InlineKeyboardButton('Рассписание', callback_data='Рассписание')
    keyb.row(but1)
    keyb.row(but2)
    keyb.row(but6)
    return keyb


def cancel():
    keyb = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('❌ Отмена', callback_data=f'Отмена')
    keyb.row(but1)
    return keyb


def add_media_post(post_id):
    keyb = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Добавить медиа', callback_data=f'Добавить_медиа;{post_id}')
    but2 = InlineKeyboardButton('Пропустить', callback_data=f'Пропустить_медиа;{post_id}')
    keyb.row(but1)
    keyb.row(but2)
    return keyb


def finish_media(post_id):
    keyb = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Завершить', callback_data=f'Завершить_медиа;{post_id}')
    keyb.row(but1)
    return keyb


def apply_post(post_id):
    keyb = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Подтвердить', callback_data=f'Подтвердить_пост;{post_id}')
    but2 = InlineKeyboardButton('Изменить', callback_data=f'Изменить_пост;{post_id}')
    keyb.row(but1)
    keyb.row(but2)
    return keyb


def edit_post(post_id):
    keyb = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Текст', callback_data=f'Ch_post;Текст;{post_id}')
    but11 = InlineKeyboardButton('Медиа', callback_data=f'Ch_post;Медиа;{post_id}')
    but2 = InlineKeyboardButton('Дата старта', callback_data=f'Ch_post;Дата_старта;{post_id}')
    but22 = InlineKeyboardButton('Чат', callback_data=f'Ch_post;Чат;{post_id}')
    but3 = InlineKeyboardButton('Таймер', callback_data=f'Ch_post;Таймер;{post_id}')
    but5 = InlineKeyboardButton('Удалить', callback_data=f'Ch_post;Удалить;{post_id}')
    but6 = InlineKeyboardButton('Назад 🔙', callback_data=f'Изменить_посты')
    keyb.row(but1)
    keyb.row(but11)
    keyb.row(but2)
    keyb.row(but22)
    keyb.row(but3)
    keyb.row(but5)
    keyb.row(but6)
    return keyb


def ch_post_chat_act(post_id):
    keyb = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Добавить', callback_data=f'EDIT;Добавить_чат;+;{post_id}')
    but2 = InlineKeyboardButton('Удалить', callback_data=f'EDIT;Удалить_чат;+;{post_id}')
    but6 = InlineKeyboardButton('Назад 🔙', callback_data=f'Изменить_пост;{post_id}')
    keyb.row(but1)
    keyb.row(but2)
    keyb.row(but6)
    return keyb


def back_to_edit_post(post_id):
    keyb = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Назад 🔙', callback_data=f'Изменить_пост;{post_id}')
    keyb.row(but1)
    return keyb


def ex_dell_post(post_id):
    keyb = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Да', callback_data=f'Точно_удалить_пост;Да;{post_id}')
    but2 = InlineKeyboardButton('Нет', callback_data=f'Точно_удалить_пост;Нет;{post_id}')
    but6 = InlineKeyboardButton('Назад 🔙', callback_data=f'Изменить_пост;{post_id}')
    keyb.row(but1)
    keyb.row(but2)
    keyb.row(but6)
    return keyb


def act_trigger(trig_id):
    keyb = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton('Добавить триггер', callback_data=f'Добавить_триг;{trig_id}')
    but2 = InlineKeyboardButton('Удалить триггер', callback_data=f'Удалить_триг;{trig_id}')
    but3 = InlineKeyboardButton('Добавить чат', callback_data=f'Добавить_чат;{trig_id}')
    but4 = InlineKeyboardButton('Удалить чат', callback_data=f'Удалить_чат;{trig_id}')
    keyb.row(but1)
    keyb.row(but2)
    keyb.row(but3)
    keyb.row(but4)
    return keyb


def gen_schedule_but(date: datetime.date, schedule):
    dict_days_week = {0: 'ПН', 1: 'ВТ', 2: 'СР', 3: 'ЧТ', 4: 'ПТ', 5: 'СБ', 6: 'ВС'}
    em = '🟢' if str(date) in schedule.schedule.schedule.keys() else '⚪️'
    but1 = InlineKeyboardButton(
        f'{dict_days_week[date.weekday()]}: {date.day}-0{date.month} | {em}',
        callback_data=f'Schedule_day;{str(date)}')
    return but1


def week_schedule(schedule):
    keyb = InlineKeyboardMarkup()

    date_tod = datetime.date.today()
    week_days = []

    for day in range(7):
        week_days.append(date_tod + datetime.timedelta(days=day))

    for date in week_days:
        but = gen_schedule_but(date, schedule)
        keyb.row(but)
    return keyb


def day_schedule(date, schedule):
    from database import PostPost

    keyb = InlineKeyboardMarkup()

    if date in schedule.schedule.schedule.keys():
        dict_posts = schedule.schedule.schedule[date]
        for date_time, items in dict_posts.items():

            for item in items:
                post = PostPost.objects(post_id=int(item)).first()
                but1 = InlineKeyboardButton(f'id-{post.post_id}: {str(post.text)[:15]}',
                                            callback_data=f'Post_menu;{post.post_id}')
                keyb.row(but1)
        but1 = InlineKeyboardButton('Создать пост 🆕', callback_data='Создать_пост')
        keyb.row(but1)
    else:
        but1 = InlineKeyboardButton('Создать пост', callback_data='Создать_пост')
        but2 = InlineKeyboardButton('Назад', callback_data=f'Рассписание')
        keyb.row(but1)
        keyb.row(but2)

    return keyb
