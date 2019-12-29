import requests

class BotHandler:
    '''Contains a number of methods to manage a bot by using HTTP requests'''
    def __init__(self, token):
            self.token = token
            self.api_url = "https://api.telegram.org/bot{}/".format(token)
            self._cache_imgs = {}

    #url = "https://api.telegram.org/bot<token>/"

    def get_updates(self, offset=0, timeout=30):
        '''Gets updates from the server (new messages, people) by using requests library'''
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        return resp.json()

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp
    
    
    def send_photo(self, chat_id,photo_file):
        method = 'sendPhoto'

        if photo_file.name in self._cache_imgs: # checks if the photo already exists
            photo_id = self._cache_imgs[photo_file.name]
            params = {'chat_id' : chat_id,'photo': photo_id}# if exists, the bot sends photo by using it ID in telegram
            resp = requests.post(self.api_url + method,params)

        else:
            files = {'photo': photo_file}
            data = {'chat_id' : chat_id} # unless, it uploads photo and adds it to cache
            resp = (requests.post(self.api_url + method,data = data, files = files)).json()
            self._cache_imgs[photo_file.name] = resp['result']['photo'][2]['file_id']

        return resp
   

    def send_sticker(self, chat_id,sticker_id):
        method = 'sendSticker'
        params = {'chat_id' : chat_id,'sticker':sticker_id}
        resp = requests.post(self.api_url + method,params)
        return resp


    def get_first_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[0]
        else:
            last_update = None

        return last_update
