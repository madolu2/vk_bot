import json
import requests


class Dvach(object):
    """docstring for ."""

    def __init__(self):
        pass


    def get_thread_list(self, board):
        response = requests.get(f'https://2ch.hk/{board}/threads.json').json()
        threads = {}
        for t in range(4):
            header = self.clean_all_tag_from_str(response['threads'][t]['subject'])
            content = self.clean_all_tag_from_str(response['threads'][t]['comment'])
            threads[t] = {'header': header, 'content': content}
        return threads

    def get_thread(self, thread, board=None):
        threads = get_thread_list(board)
        header = threads[thread]['threads'][0]['posts'][0]['subject']
        content = threads[thread]['threads'][0]['posts'][0]['comment']


    def get_thread_by_id(self, board, thread_id):
        response = requests.get(f'https://2ch.hk/{board}/res/{thread_id}.json').json()
        return response

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
