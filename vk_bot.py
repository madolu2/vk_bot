from datetime import datetime

class VkBot:


    def __init__(self, event):
        self.EVENT = event
        self.TEXT = event.message['text']
        self.FROM_ID = event.message['from_id']
        self.CHAT_ID = event.chat_id


    def console_log(self, event):
        time = datetime.strftime(datetime.now(), '%H:%M')
        print(f'{time} написал - {self.TEXT}')
