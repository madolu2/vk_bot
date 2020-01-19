import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from vk_bot import VkBot
from dvach import Dvach
from datetime import datetime
from parse import *

def send_message(event, message, from_user = True):
    if from_user:
        vk.messages.send(
                    user_id=event.message['from_id'],
                    message=message,
                    random_id=get_random_id()
		)
    else:
        vk.messages.send(
                    chat_id=event.chat_id,
                    message=message,
                    random_id=get_random_id()
		)

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
            mailing(event, f'Тред номер {t+1}')
            message = thread[t]['header'] + '\n'
            mailing(event, message)
            message = ''
        return message
    except Exception as e:
        mailing(event, 'Попробуй есчо')


def mailing(event, message):
    if event.from_chat:
        send_message(event, message, False)
    if event.from_user:
        send_message(event, message)


token = "5b121f534ed551acff6595ad366534d14a6aa9097556c6c11beb6ab9ad5ac1b43c3189fcf875b74eee580"

bot_session = vk_api.VkApi(token=token)
vk = bot_session.get_api()
longpoll = VkBotLongPoll(bot_session, 177063309)

for event in longpoll.listen():
    dvach = Dvach()
    if event.type == VkBotEventType.MESSAGE_NEW and event.message:
        text = event.message['text']
        time = datetime.strftime(datetime.now(), '%H:%M')
        print(f'{time} написал - {text}')
        print(event.message)
        if 'треды' in event.message['text'].lower():
            thread_format(dvach, event)
            mailing(event, 'Выберите тред')
        if 'один тред' in event.message['text'].lower():
            try:
                single_thread = thread_format(dvach, event, choice=True)
                message = single_thread['header'] + '\n' +  single_thread['content']
                mailing(event, message)
            except:
                mailing(event, 'Что-то не так')
        if event.message['text'].lower() == 'жопа':
            message = 'Сам ты жопа((('
            mailing(event, message)
        if event.message['text'].lower() == 'алиса':
            message = 'Такая красивая <3 <3 <3'
            mailing(event, message)
