#!/usr/bin/env python
# coding: utf-8

import os
import random
import time
from modules.user_input import UserInput
from modules.bot_handler import BotHandler
from modules.folders import FolderTxt,FolderImg
import json




      
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
	                    
	                magnito_bot.send_chat_action(first_chat_id,'typing')    
	                    	     
	                try:
	                	user_input = UserInput(first_chat_text)

	                except json.decoder.JSONDecodeError:
	                	magnito_bot.send_message(first_chat_id, f"And what should I do with that {first_chat_text} ?") # if there is an emoji, it send that very emoji to the user back
	                	new_offset = first_update_id + 1
	                	continue


	                if user_input.has_cyrillic(): # checks if there are Cyrillic symbols
	                	magnito_bot.send_message(first_chat_id,f"The translation is '{user_input.english_text}'")				                	

	                elif user_input.has_mistakes() and (not user_input.has_date()): #True if there is no emoji or date, and there is a mistake
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

	                negative_result = False


	                if len(user_input.original_text)>=3:

		                list_of_matches = txt_folder.search_for_matches(user_input.bag_of_words)
		                if list_of_matches:
		                	magnito_bot.send_chat_action(first_chat_id,'upload_photo')
		                	for name_of_file in list_of_matches:
		                		 
		                		with open(img_folder.path_to_img(name_of_file[:-4]),'rb') as photo_f:
		                			magnito_bot.send_photo(first_chat_id,photo_f) # send a corresponding picture

		                		new_offset = first_update_id + 1

	                	else:
		                	negative_result = True
	                else:
	                	negative_result = True

	                if negative_result:
	                	magnito_bot.send_message(first_chat_id, 'Sorry, there is nothing like that. Try something else!')
	                	new_offset = first_update_id + 1

	
	        	                
        except Exception as e:
	        magnito_bot.send_message(376385737, e)
	        magnito_bot.send_message(376385737, user_input.has_emoji())
	        #raise e
	        new_offset = first_update_id + 1
	     	



if __name__ == '__main__':
    main()






