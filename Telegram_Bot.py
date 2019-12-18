#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
import datetime
import os


# In[2]:


class BotHandler:
    def __init__(self, token):
            self.token = token
            self.api_url = "https://api.telegram.org/bot{}/".format(token)

    #url = "https://api.telegram.org/bot<token>/"

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp
    
    def send_photo(self, chat_id,photo_url):
        method = 'sendPhoto'
        files = {'photo': open(f'img/{photo_url}.jpg', 'rb')}
        data = {'chat_id' : chat_id}
        resp = requests.post(self.api_url + method,files=files,data=data)
        return resp




    def get_first_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[0]
        else:
            last_update = None

        return last_update


# In[3]:


token = '938870264:AAHAL4RlulLbjEcgM1awC9eDoyHUtLa4jsQ' #Token of your bot
magnito_bot = BotHandler(token) #Your bot's name


# In[28]:


def main():
    new_offset = 0
    print('hi, now launching...')

    while True:
        all_updates=magnito_bot.get_updates(new_offset)

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
                    magnito_bot.send_message(first_chat_id, f"Hey, {first_chat_name}, what's up?\n\nI am SEO Searcher, and I can search for different lessons from SOE by using keywords from the topics.\nI have all the lessons from the beginning to November 2019 in my database.\nHere are a few tips how to use me:\n1) Enter the keywords you can remember from a topic. As a separator use SPACE.\n(Warning, in one message you can write only keywords from THE SAME topic, otherwise I will send you nothing)\n2) The more keywords, the more specific the search.\n\nFor instance, you can write 'exposed to' or just 'exposed'.\nYou can mention a few key words from ONE topic, such as 'disappointed  devoted to discriminated' or 'much many'.\n\nNow send me something!")
                    new_offset = first_update_id + 1
                    continue
                    
                user_input = set((first_chat_text.lower()).split(' ')) # split and convert user input to set 
                txt_list = os.listdir('txt') # list of txt files in derectory
                found_flag = True
                for txt_f in txt_list: # grabbing all txt files in the directory
                    f = open("txt/"+txt_f,"r")
                    text = set(f.read().split()) # getting a bag of words from the txt's
                    if user_input.issubset(text): # check if the user input is a subset of the bag of words
                        magnito_bot.send_photo(first_chat_id,txt_f[:-4]) # sending a corresponding picture
                        new_offset = first_update_id + 1
                        found_flag = False
                    f.close()
                if found_flag:
                    magnito_bot.send_message(first_chat_id, 'Sorry, there is nothing like that. Try something else!')
                    new_offset = first_update_id + 1



if __name__ == '__main__':
    main()


# In[ ]:




