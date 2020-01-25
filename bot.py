import vk_api
import requests
from vk_api.utils import get_random_id
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from dvach import Dvach
from vk_bot import VkBot
from parse import *


token = "5b121f534ed551acff6595ad366534d14a6aa9097556c6c11beb6ab9ad5ac1b43c3189fcf875b74eee580"
bot_session = vk_api.VkApi(token=token)
vk = bot_session.get_api()
longpoll = VkBotLongPoll(bot_session, 177063309)
session = requests.Session()
upload = VkUpload(vk)
dvach = Dvach()

def send_img(vkBot_instance, img):
    attachments = []
    length = len(img)
    if length > 10:
        length = 10
    for i in range(length):
        image = session.get(img[i], stream=True)
        photo = upload.photo_messages(photos=image.raw)[0]
        attachments.append(
            'photo{}_{}'.format(photo['owner_id'], photo['id'])
        )

    if vkBot_instance.EVENT.from_chat:
        vk.messages.send(
                    chat_id=vkBot_instance.EVENT.chat_id,
                    attachment=','.join(attachments),
                    random_id=get_random_id(),
                    message=''
                )
    else:
        vk.messages.send(
                    user_id=vkBot_instance.FROM_ID,
                    attachment=','.join(attachments),
                    random_id=get_random_id(),
                    message=''
                )

def send_message(vkBot_instance, message):
    if vkBot_instance.EVENT.from_chat:
        vk.messages.send(
                    chat_id=vkBot_instance.EVENT.chat_id,
                    message=message,
                    random_id=get_random_id()
        )
    else:
        vk.messages.send(
                    user_id=vkBot_instance.FROM_ID,
                    message=message,
                    random_id=get_random_id()
        )

def threads_from_board(dvach_instance, vkBot_instance):
    try:
        board = parse('треды {board}', vkBot_instance.TEXT)['board']
        print(board)
        threads = dvach_instance.get_thread_list(board)
        for t in threads:
            header = str(t+1) + '. ' + threads[t]['header']
            send_message(vkBot_instance, header)
    except:
        send_message(vkBot_instance, 'Что-то не так')


def single_thread(dvach_instance, vkBot_instance):
    try:
        thread = parse('{board} тред номер {num}', vkBot_instance.TEXT)
        t = dvach_instance.get_thread(int(thread['num'])-1, thread['board'])
        header, content, id, board = t['header'], t['content'], t['id'], thread['board']
        send_message(vkBot_instance, header + '\n' + content)
        try:
            img_url = dvach_instance.files_in_thread(t)
            print(img_url)
            send_img(vkBot_instance, img_url)
        except:
            send_message(vkBot_instance, 'Не могу загрузить картинки((')
        send_message(vkBot_instance, f'https://2ch.hk/{board}/res/{id}.html')
    except vk_api.exceptions.ApiError as e:
        send_message(vkBot_instance, 'Тред слишком большой, соре(((((((((((((')
    except:
        send_message(vkBot_instance, 'Что-то не так')

def send_schedule(vkBot_instance, single=False, specific=False):
    if single:
        try:
            schedule = vkBot_instance.get_schedule()
            command = parse('расписание {day}',vkBot_instance.TEXT)['day']
            day = vkBot_instance.message_to_day(command)
            print(day)
            schedule = schedule[day]
            message = ''
            for i in schedule:
                if i == 'day':
                    message += f'{schedule[i]}\n'
                else:
                    message += " | ".join(str(x) for x in schedule[i]) + '\n'
            send_message(vkBot_instance, message)
        except:
            send_message(vkBot_instance, 'Ты выбрал какой то неверный день')
    if specific:
        try:
            schedule = vkBot_instance.get_schedule()
            command = parse('пара {day} {num}',vkBot_instance.TEXT)
            day = vkBot_instance.message_to_day(command['day'])
            schedule = schedule[day][int(command['num'])-1]
            message = " | ".join(str(x) for x in schedule) + '\n'
            send_message(vkBot_instance, message)
        except:
            send_message(vkBot_instance, 'Неверная цифра друг')

def send_doc(vkBot_instance):
    message = '''треды (имя доски) => выведет 5 заголовков тредов с конкретной доски\nПРИМЕР треды news\n
(имя доски) тред номер (цифра) => выведет конкретный тред из функции выше. 18+ картинки не выводит\nПРИМЕР b тред номер 2\n
жопа => САМ ЖОПА\n
расписание (день недели)=> выведет расписание 283а группы пту лучшего города на земле\nПРИМЕР расписание среда\n
пара (день недели) (цифра)=> выведет конкретную пару\nПРИМЕР пара четверг 2\n'''
    send_message(vkBot_instance, message)

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.message:
        bot = VkBot(event)
        bot.console_log()
        if 'треды' in bot.TEXT.lower():
            threads_from_board(dvach, bot)
        if 'тред номер' in bot.TEXT.lower():
            single_thread(dvach, bot)
        if 'жопа' in bot.TEXT.lower():
            send_message(bot, 'нет ты!!!')
        if 'алиса' in bot.TEXT.lower():
            send_message(bot, 'Такая красивая <3 <3 <3')
        if 'расписание' in bot.TEXT.lower():
            send_schedule(bot, single=True)
        if 'пара' in bot.TEXT.lower():
            send_schedule(bot, specific=True)
        if 'документация' in bot.TEXT.lower():
            send_doc(bot)
