import vk_api
import requests
from parse import *
from dvach import Dvach
from vk_api.utils import get_random_id
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from datetime import datetime
from requests_html import HTMLSession


class VkBot:

    def __init__(self, event, vk, upload, session):
        self.EVENT = event
        self.TEXT = event.message['text'].lower()
        self.FROM_ID = event.message['from_id']
        self.CHAT_ID = event.chat_id
        self.VK = vk
        self.UPLOAD = upload
        self.SESSION = session
        self.dvach_instance = Dvach()

    def console_log(self):
        time = datetime.strftime(datetime.now(), '%H:%M')
        print(f'{time} написал - {self.TEXT}')

    def get_schedule(self):
        session = HTMLSession()
        url = 'http://www.asu.ru/timetable/students/18/2129439627'
        response = session.get(url)
        table = response.html.find('.schedule', first=True)
        table = table.text
        return self.format_schedule(table)

    def format_schedule(self, schedule):
        DAYS = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        CLEAR_DAYS = []
        for day in range(6):
            if day == 0:
                CLEAR_DAYS.append(schedule[0:schedule.find(DAYS[day+1])])
            elif day == 5:
                CLEAR_DAYS.append(schedule[schedule.find(DAYS[day]):-1])
            else:
                CLEAR_DAYS.append(schedule[schedule.find(DAYS[day]):schedule.find(DAYS[day+1])])
        for day in range(6):
            CLEAR_DAYS[day] = CLEAR_DAYS[day].split('\n')
            for line in CLEAR_DAYS[day]:
                if 'дата изменения' in line:
                    CLEAR_DAYS[day].pop(CLEAR_DAYS[day].index(line))
                try:
                    CLEAR_DAYS[day].pop(CLEAR_DAYS[day].index('свободные аудитории'))
                except:
                    pass
            CLEAR_DAYS[day].pop(-1)
        DAYS = {}
        for day in range(6):
            DAYS[day] = {}
            DAYS[day]['day'] = CLEAR_DAYS[day][0]
            length = (len(CLEAR_DAYS[day]) - 1) // 5
            tmp = 0
            for lesson in range(length):
                DAYS[day][lesson] = CLEAR_DAYS[day][1+tmp:6+tmp]
                tmp += 5
        return DAYS

    def message_to_day(self, message):
        DAYS = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        message =  message.lower()
        if message == 'Понедельник'.lower():
            return 0
        if message == 'Вторник'.lower():
            return 1
        if message == 'Среда'.lower():
            return 2
        if message == 'Четверг'.lower():
            return 3
        if message == 'Пятница'.lower():
            return 4
        if message == 'Суббота'.lower():
            return 5


    def send_img(self, img):
        attachments = []
        length = len(img)
        if length > 10:
            length = 10
        for i in range(length):
            image = self.SESSION.get(img[i], stream=True)
            photo = self.UPLOAD.photo_messages(photos=image.raw)[0]
            attachments.append(
                'photo{}_{}'.format(photo['owner_id'], photo['id'])
            )

        if self.EVENT.from_chat:
            self.VK.messages.send(
                        chat_id=self.EVENT.chat_id,
                        attachment=','.join(attachments),
                        random_id=get_random_id(),
                        message=''
                    )
        else:
            self.VK.messages.send(
                        user_id=self.FROM_ID,
                        attachment=','.join(attachments),
                        random_id=get_random_id(),
                        message=''
                    )


    def send_message(self, message):
        if self.EVENT.from_chat:
            self.VK.messages.send(
                        chat_id=self.EVENT.chat_id,
                        message=message,
                        random_id=get_random_id()
            )
        else:
            self.VK.messages.send(
                        user_id=self.FROM_ID,
                        message=message,
                        random_id=get_random_id()
            )


    def threads_from_board(self):
        try:
            board = parse('треды {board}', self.TEXT)['board']
            threads = self.dvach_instance.get_thread_list(board)
            for t in threads:
                header = str(t+1) + '. ' + threads[t]['header']
                self.send_message(header)
        except:
            self.send_message('Что-то не так')


    def single_thread(self):
        try:
            thread = parse('{board} тред номер {num}', self.TEXT)
            t = self.dvach_instance.get_thread(int(thread['num'])-1, thread['board'])
            header, content, id, board = t['header'], t['content'], t['id'], thread['board']
            self.send_message(header + '\n' + content)
            try:
                img_url = dvach_instance.files_in_thread(t)
                self.send_img(img_url)
            except:
                self.send_message('Не могу загрузить картинки((')
            self.send_message(f'https://2ch.hk/{board}/res/{id}.html')
        except vk_api.exceptions.ApiError as e:
            self.send_message('Тред слишком большой, соре(((((((((((((')
        except:
            self.send_message('Что-то не так')


    def send_schedule(self, single=False, specific=False):
        if single:
            try:
                schedule = self.get_schedule()
                command = parse('расписание {day}', self.TEXT)['day']
                day = self.message_to_day(command)
                schedule = schedule[day]
                message = ''
                for i in schedule:
                    if i == 'day':
                        message += f'{schedule[i]}\n'
                    else:
                        message += " | ".join(str(x) for x in schedule[i]) + '\n'
                self.send_message(message)
            except:
                self.send_message('Ты выбрал какой то неверный день')
        if specific:
            try:
                schedule = self.get_schedule()
                command = parse('пара {day} {num}', self.TEXT)
                day = self.message_to_day(command['day'])
                schedule = schedule[day][int(command['num'])-1]
                message = " | ".join(str(x) for x in schedule) + '\n'
                self.send_message(message)
            except:
                self.send_message('Неверная цифра друг')


    def send_doc(self):
        message = '''
треды (имя доски) => выведет 5 заголовков тредов с конкретной доски\nПРИМЕР треды news\n
(имя доски) тред номер (цифра) => выведет конкретный тред из функции выше. 18+ картинки не выводит\nПРИМЕР b тред номер 2\n
расписание (день недели)=> выведет расписание 283а группы пту лучшего города на земле\nПРИМЕР расписание среда\n
пара (день недели) (цифра)=> выведет конкретную пару\nПРИМЕР пара четверг 2\n'''
        self.send_message(message)
