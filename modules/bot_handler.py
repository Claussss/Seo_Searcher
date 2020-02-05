import requests
import json


class BotHandler:
    '''Contains a number of methods to manage a bot by using HTTP requests'''

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        with open('all_images_ids.json','r') as f:
            self._cache_imgs = json.load(f)

    #url = "https://api.telegram.org/bot<token>/"

    def get_updates(self, offset=0, timeout=30):
        '''Gets updates from the server (new messages, people) by using requests library'''
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}

        resp = requests.get(self.api_url + method, params)

        if resp.ok:
            all_updates = resp.json()['result']
            if all_updates:
                return all_updates

        return None

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_chat_action(self, chat_id, action):
        params = {'chat_id': chat_id, 'action': action}
        method = 'sendChatAction'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_photo(self, chat_id, photo_file):
        method = 'sendPhoto'

        if photo_file.name in self._cache_imgs:  # checks if the photo already exists
            photo_id = self._cache_imgs[photo_file.name]
            # if exists, the bot sends photo by using it ID in telegram
            params = {'chat_id': chat_id, 'photo': photo_id}
            resp = requests.post(self.api_url + method, params)

        else:
            files = {'photo': photo_file}
            # unless, it uploads photo and adds it to cache
            data = {'chat_id': chat_id}
            resp = (requests.post(self.api_url + method,
                                  data=data, files=files)).json()
            self._cache_imgs[photo_file.name] = resp[
                'result']['photo'][2]['file_id']

        return resp

    def send_sticker(self, chat_id, sticker_id):

        method = 'sendSticker'
        params = {'chat_id': chat_id, 'sticker': sticker_id}
        resp = requests.post(self.api_url + method, params)
        return resp
