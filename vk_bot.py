import bs4
import requests
from datetime import datetime
from vk_api.utils import get_random_id

class VkBot:

    def __init__(self, event):
        self.EVENT = event
        self.CHAT_ID = event.chat_id
        self.TEXT = event.message['text']
        self.FROM_ID = event.message['from_id']

    def send_message(self, message):
        if self.EVENT.from_chat:
            vk.messages.send(
                        user_id=self.FROM_ID,
                        message=message,
                        random_id=get_random_id()
    		)
        else:
            vk.messages.send(
                        chat_id=self.EVENT.chat_id,
                        message=message,
                        random_id=get_random_id()
    		)

    def console_log(self, event):
        time = datetime.strftime(datetime.now(), '%H:%M')
        print(f'{time} написал - {self.TEXT}')
