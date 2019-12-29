#!/usr/bin/env python
# coding: utf-8

import os
import random
import time
#from modules.user_input import UserInput
#from modules.bot_handler import BotHandler
#from modules.folders import FolderTxt,FolderImg


from googletrans import Translator
from spellchecker import SpellChecker
import re 



class UserInput():
    '''Represents message sent by the user.'''
    def __init__(self,user_input):
        self._translator = Translator().translate(user_input.lower())
        self.spell_checker = SpellChecker()
        self.lang = self._translator.src # language 
        self.english_text = self._translator.text # translated text into English
        self.original_text = self._translator.origin
        self._bag_of_words = set(self.english_text.lower().split()) # default bag of words of the text with english translation

    @property
    def bag_of_words(self):
        return self._bag_of_words

    @bag_of_words.setter
    def bag_of_words(self,new_bag):
        if isinstance(new_bag,set):
        	self._bag_of_words = new_bag

        else:
        	raise TypeError("The argument has to be a set()")
        
        
    def has_english_context(self):
        '''Returns True if the text language is English'''
        return self.lang == 'en'
    
    def has_mistakes(self):
        '''Returns True is there are mistakes'''
        return bool(self.spell_checker.unknown(self.original_text.split())) # checking origin user input for mistakes (not translated)

    def has_cyrillic(self):
        '''Returns True is there are Cyrillic symbols'''
        return bool(re.search('[а-яА-Я]', self.original_text))



import os

class BaseFolder:
	def __init__(self,directory,extension):
		self.directory = directory
		self.extension = extension
		self.list_of_files = os.listdir(directory)


class FolderTxt(BaseFolder):

	def search_for_matches(self,user_bag_of_words):
		approptiate_file_names = []
		for txt_f in self.list_of_files: # grabbing all txt files in the directory
		    f = open(self.directory+txt_f,"r")
		    text = set(f.read().split()) # getting a bag of words from the txt files
		    if user_bag_of_words.issubset(text): # check if the user input is a subset of the bag of words
		    	approptiate_file_names.append(txt_f)
		    	f.close()
		return approptiate_file_names


class FolderImg(BaseFolder):

	def open_img(self,file_name):

		full_file_name = file_name+"."+self.extension
		if full_file_name in self.list_of_files:
			return open(self.directory+full_file_name,'rb')

		raise KeyError("There is no file like that")
		


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

      
token = os.environ.get('TELEGRAM_TOKEN') #Token of the bot
magnito_bot = BotHandler(token) #object of the Bot class


def main():
    stickers = [
    'CAADAgADmAADGB0GD38JjVV51eNUFgQ',
    'CAADAgADqQADGB0GD3PlulRsd1MkFgQ',
    'CAADAgADvAADGB0GD6SysPS40rdzFgQ',
    'CAADAgADjwADGB0GD0ckrhn7ST9JFgQ',
    'CAADAgADnwADGB0GDyWgsIdx524-FgQ'] # ids of stikers

    new_offset = 0
    
    print('Now launching...')

    while True:
        try:
	        all_updates = None
	        all_updates=magnito_bot.get_updates(new_offset)

	        if 'result' not in all_updates:
	        	time.sleep(2)
	        	continue

	        all_updates = all_updates['result']
	        if len(all_updates) > 0:
	            for current_update in all_updates:
	                print(current_update)
	                first_update_id = current_update['update_id']
	                if 'text' not in current_update['message']:
	                    first_chat_text='New member'
	                else:
	                    first_chat_text = current_update['message']['text']
	                first_chat_id = current_update['message']['chat']['id']
	                if 'first_name' in current_update['message']:
	                    first_chat_name = current_update['message']['chat']['first_name']
	                elif 'new_chat_member' in current_update['message']:
	                    first_chat_name = current_update['message']['new_chat_member']['username']
	                elif 'from' in current_update['message']:
	                    first_chat_name = current_update['message']['from']['first_name']
	                else:
	                    first_chat_name = "unknown"

	                if first_chat_text == '/start':
	                	
	                	magnito_bot.send_message(first_chat_id, f"""
Hey, {first_chat_name}, what's up?

I am SEO Searcher, and I can search for different lessons from SOE by using keywords from the topics.
Also, I have built-in google translator, so you can write keywords in Russian or Ukrainian.
I have all the lessons from the beginning to November 2019.

Here are a few tips how to use me:

----1) Enter the KEYWORDS you can remember from a topic. As a separator use SPACE.

WARNING: in one message you can write only keywords from THE SAME topic, otherwise I will send you nothing

----2) The MORE keywords, the more specific the search.

For instance, you can write 'exposed to' or just 'exposed', 'помнить', 'пам'ятати'.
You can mention a few key words from ONE topic, such as 'disappointed  devoted to discriminated', 'much many' or 'рисковать отрицать'.

-------BONUS-------
Furthermore, if you send me a date by using this template 
'YEAR-MONTH', I will send you all the lessons of that month.
For example, '2019-11' or '2018-01'.

Now send me something!
""")

	                    
	                	magnito_bot.send_sticker(first_chat_id,random.choice(stickers))
	                	new_offset = first_update_id + 1
	                	continue
	                    
	                    
	                    	     
	                user_input = UserInput(first_chat_text)

	                if user_input.has_cyrillic(): # checks if there are Cyrillic symbols
	                	magnito_bot.send_message(first_chat_id,f"The translation is '{user_input.english_text}'")				                	

	                elif user_input.has_mistakes(): #if the user input language is English and there are mistakes
	                	all_words = set(user_input.original_text.split()) # set of all words in user input
	                	wrong_words = user_input.spell_checker.unknown(all_words)
	                	corrected_words = []
	                	message_to_user = "Spelling correction:\n"

	                	for word in wrong_words:
	                		corrected_word = user_input.spell_checker.correction(word)
	                		message_to_user+=f"{word} -> {corrected_word}\n"
	                		corrected_words.append(corrected_word)

	                	magnito_bot.send_message(first_chat_id,message_to_user)
	                	user_input.bag_of_words = all_words.difference(wrong_words).union(corrected_words)

	                txt_folder = FolderTxt("txt/","txt")
	                img_folder = FolderImg("img/","jpg")

	                if len(user_input.original_text)>=3:

		                list_of_matches = txt_folder.search_for_matches(user_input.bag_of_words)
		                if list_of_matches:
		                	for name_of_file in list_of_matches:
		                		magnito_bot.send_photo(first_chat_id,img_folder.open_img(name_of_file[:-4])) # sending a corresponding picture

		                		new_offset = first_update_id + 1

		                else:
		                	magnito_bot.send_message(first_chat_id, 'Sorry, there is nothing like that. Try something else!')
		                	new_offset = first_update_id + 1

	
	        	                
        except Exception as e:
	        magnito_bot.send_message(376385737, e)
	        raise e
	        new_offset = first_update_id + 1       	



if __name__ == '__main__':
    main()





