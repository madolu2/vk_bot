import vk_api
from vk_api import VkUpload
import requests
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_bot import VkBot


token = "5b121f534ed551acff6595ad366534d14a6aa9097556c6c11beb6ab9ad5ac1b43c3189fcf875b74eee580"
bot_session = vk_api.VkApi(token=token)
vk = bot_session.get_api()
longpoll = VkBotLongPoll(bot_session, 177063309)
session = requests.Session()
upload = VkUpload(vk)

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.message:
        bot = VkBot(event, vk, upload, session)
        bot.console_log()
        if 'треды' in bot.TEXT:
            bot.threads_from_board()
        if 'тред номер' in bot.TEXT:
            bot.single_thread()
        if 'расписание' in bot.TEXT:
            bot.send_schedule(single=True)
        if 'пара' in bot.TEXT:
            bot.send_schedule(specific=True)
        if 'документация' in bot.TEXT:
            bot.send_doc()
