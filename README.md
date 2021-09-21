# poster


Bot for sending plan post to groups


start:

python3 bot.py

send to bot: /admin

create post



setup cron:

*/1 * * * * sudo python3.8 /your-path/poster/cron/check_schedule.py >> /your-path/poster/cron/log_schedule.log
