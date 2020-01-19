import json
import requests


class Dvach(object):
    """docstring for ."""

    def __init__(self):
        pass

    def get_thread_list(self, board):
        url = f'https://2ch.hk/{board}/threads.json'
        response = requests.get(url).json()
        threads = {}
        for t in range(4):
            header = self.clean_all_tag_from_str(response['threads'][t]['subject'])
            content = self.clean_all_tag_from_str(response['threads'][t]['comment'])
            id = self.clean_all_tag_from_str(response['threads'][t]['num'])
            threads[t] = {'header': header, 'content': content, 'id': id}
        return threads

    def get_thread(self, thread, board='news'):
        threads = self.get_thread_list(board)
        return threads[thread]

    @staticmethod
    def clean_all_tag_from_str(string_line):
        string_line = string_line.replace('<br>', '\n')
        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True
        result = result.replace('&#47;', '/')
        return result
