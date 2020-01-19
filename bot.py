import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from dvach import Dvach
from parse import *



def threads_from_board(dvach_instance, vkBot_instance):
    try:
        board = parse('треды {board}', vkBot_instance.TEXT)['board']
        return dvach_instance.get_thread_list(board)
    except:
        vkBot_instance.send_message('Что-то не так')


def single_thread(dvach_instance, vkBot_instance):


def thread_format(dvach, event, choice=False):
    try:
        if choice:
            result = parse('один тред {board} {num}', event.message['text'])
            print(result)
            thread = dvach.get_thread_list(result['board'])
            return thread[int(result['num'])-1]
        result = parse('треды {board}', event.message['text'])['board']
        thread = dvach.get_thread_list(result)
        for t in thread:
            send_message(event, f'Тред номер {t+1}')
            message = thread[t]['header'] + '\n'
            send_message(event, message)
            message = ''
        return message
    except Exception as e:
        send_message(event, 'Попробуй есчо')


token = "5b121f534ed551acff6595ad366534d14a6aa9097556c6c11beb6ab9ad5ac1b43c3189fcf875b74eee580"

bot_session = vk_api.VkApi(token=token)
vk = bot_session.get_api()
longpoll = VkBotLongPoll(bot_session, 177063309)

global board

for event in longpoll.listen():
    dvach = Dvach()
    bot = VkBot(event)
    if event.type == VkBotEventType.MESSAGE_NEW and event.message:
        text = event.message['text']
        time = datetime.strftime(datetime.now(), '%H:%M')
        print(f'{time} написал - {text}')
        print(event.message)
        if 'треды' in event.message['text'].lower():
            thread_format(dvach, event)
            send_message(event, 'Выберите тред')
        if 'один тред' in event.message['text'].lower():
            try:
                single_thread = thread_format(dvach, event, choice=True)
                message = single_thread['header'] + '\n' +  single_thread['content']
                send_message(event, message)
            except:
                send_message(event, 'Что-то не так')
        if event.message['text'].lower() == 'жопа':
            message = 'Сам ты жопа((('
            send_message(event, message)
        if event.message['text'].lower() == 'алиса':
            message = 'Такая красивая <3 <3 <3'
            send_message(event, message)
