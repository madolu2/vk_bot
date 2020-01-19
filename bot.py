import vk_api
from vk_api.utils import get_random_id
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

def send_message(vkBot_instance, message):
    if vkBot_instance.EVENT.from_chat:
        vk.messages.send(
                    user_id=vkBot_instance.FROM_ID,
                    message=message,
                    random_id=get_random_id()
        )
    else:
        vk.messages.send(
                    chat_id=vkBot_instance.EVENT.chat_id,
                    message=message,
                    random_id=get_random_id()
        )

def threads_from_board(dvach_instance, vkBot_instance):
    try:
        board = parse('треды {board}', vkBot_instance.TEXT)['board']
        threads = dvach_instance.get_thread_list(board)
        for t in threads:
            send_message(vkBot_instance, t['header'])
    except:
        send_message(vkBot_instance, 'Что-то не так')


def single_thread(dvach_instance, vkBot_instance):
    try:
        thread = parse('тред {num}', vkBot_instance.TEXT)['num']
        t = dvach_instance.get_thread(thread, board)
        header, content, id = t['header'], t['content'], t['id']
        send_message(vkBot_instance, header + '\n' + content)
        send_message(vkBot_instance, f'https://2ch.hk/{board}/res/{id}.html')
    except:
        send_message(vkBot_instance, 'Что-то не так')

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.message:
        bot = VkBot(event)
        if 'треды' in bot.TEXT.lower():
            threads_from_board(dvach, bot)
        if 'тред' in bot.TEXT.lower():
            single_thread(dvach, bot)
        if 'жопа' or 'jopa' or 'ass' in bot.TEXT.lower():
            send_message(bot, 'нет ты!!!')
        if 'алиса' in bot.TEXT.lower():
            send_message(bot, 'Такая красивая <3 <3 <3')
