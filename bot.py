import handlers, functions
from misc import dp
import aiogram


if __name__ == '__main__':
    aiogram.executor.start_polling(dp)
