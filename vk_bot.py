from datetime import datetime
from requests_html import HTMLSession

class VkBot:


    def __init__(self, event):
        self.EVENT = event
        self.TEXT = event.message['text']
        self.FROM_ID = event.message['from_id']
        self.CHAT_ID = event.chat_id


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
