from envparse import env


env.read_envfile()

BOT_TOKEN = env.str('BOT_TOKEN')

ADM_IDS = env.str('ADM_IDS')

DATABASE_NAME = env.str('DATABASE_NAME')
DATABASE_HOST = env.str('DATABASE_HOST')
DATABASE_PORT = env.str('DATABASE_PORT')
DATABASE_LOGIN = env.str('DATABASE_LOGIN')
DATABASE_PASSWORD = env.str('DATABASE_PASSWORD')

SYSTEM_CHAT = env.str('SYSTEM_CHAT')
