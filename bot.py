import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from dvach import Dvach
from vk_bot import VkBot
from parse import *


token = "5b121f534ed551acff6595ad366534d14a6aa9097556c6c11beb6ab9ad5ac1b43c3189fcf875b74eee580"
bot_session = vk_api.VkApi(token=token)
vk = bot_session.get_api()
longpoll = VkBotLongPoll(bot_session, 177063309)
dvach = Dvach()
global board

def threads_from_board(dvach_instance, vkBot_instance):
    try:
        board = parse('треды {board}', vkBot_instance.TEXT)['board']
        threads = dvach_instance.get_thread_list(board)
        for t in threads:
            vkBot_instance.send_message(t['header'])
    except:
        vkBot_instance.send_message('Что-то не так')


def single_thread(dvach_instance, vkBot_instance):
    try:
        thread = parse('тред {num}', vkBot_instance.TEXT)['num']
        t = dvach_instance.get_thread(thread, board)
        vkBot_instance.send_message(t['header']+'\n'+t['content'])
        vkBot_instance.send_message(f'https://2ch.hk/{board}/res/{t['id']}.html')
    except:
        vkBot_instance.send_message('Что-то не так')

for event in longpoll.listen():
    bot = VkBot(event)
    if event.type == VkBotEventType.MESSAGE_NEW and event.message:
        if 'треды' in bot.TEXT.lower():
            threads_from_board(dvach, bot)
        if 'тред' in bot.TEXT.lower():
            single_thread(dvach, bot)
        if 'жопа' or 'jopa' or 'ass' in bot.TEXT.lower():
            bot.send_message('нет ты!!!')
        if 'алиса' in bot.TEXT.lower():
            bot.send_message('Такая красивая <3 <3 <3')
