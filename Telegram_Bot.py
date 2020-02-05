import os
import random
import time
from modules.user_input import UserInput
from modules.bot_handler import BotHandler
from modules.folders import FolderTxt, FolderImg
import json

from datetime import datetime


token = os.environ.get('TELEGRAM_TOKEN')  # Token of the bot
magnito_bot = BotHandler(token)  # object of the Bot class


def main():

    stickers = [
        'CAADAgADmAADGB0GD38JjVV51eNUFgQ',
        'CAADAgADqQADGB0GD3PlulRsd1MkFgQ',
        'CAADAgADvAADGB0GD6SysPS40rdzFgQ',
        'CAADAgADjwADGB0GD0ckrhn7ST9JFgQ',
        'CAADAgADnwADGB0GDyWgsIdx524-FgQ']  # ids of stikers

    new_offset = 0

    img_folder = FolderImg("img/", "jpg")
    txt_folder = FolderTxt("txt/", "txt")

    print('Now launching...')

    while True:
        try:
            all_updates = magnito_bot.get_updates(new_offset)

            if all_updates != None:

                for current_update in all_updates:

                    print(current_update)

                    first_update_id = current_update['update_id']
                    first_chat_id = current_update['message']['chat']['id']
                    first_chat_name = current_update['message']['from']['first_name']
                    first_chat_text = current_update['message']['text']


                    if first_chat_text == '/start':

                        with open('greetings.txt', 'r', encoding="utf8") as file:
                            greeting_message = file.read()

                        magnito_bot.send_message(first_chat_id,greeting_message.format(first_chat_name)) # inserting the user name
                        magnito_bot.send_sticker(
                            first_chat_id, random.choice(stickers))

                        new_offset = first_update_id + 1
                        continue


                    magnito_bot.send_chat_action(first_chat_id, 'typing')

                    try:
                        user_input = UserInput(first_chat_text)

                    except json.decoder.JSONDecodeError:
                        # if there is an emoji, it send that very emoji to the
                        # user back
                        magnito_bot.send_message(
                            first_chat_id, first_chat_text * 2)
                        new_offset = first_update_id + 1
                        continue

                    if user_input.has_cyrillic():  # checks if there are Cyrillic symbols
                        magnito_bot.send_message(first_chat_id, f"The translation is '{user_input.english_text}'")

                    # True if there is no emoji or date, and there is a mistake
                    elif user_input.has_mistakes() and (not user_input.has_date()):
                        # set of all words in user input
                        all_words = set(user_input.original_text.split())
                        wrong_words = user_input.spell_checker.unknown(
                            all_words)
                        corrected_words = []
                        message_to_user = "Spelling correction:\n"

                        for word in wrong_words:
                            corrected_word = user_input.spell_checker.correction(
                                word)
                            message_to_user += f"{word} -> {corrected_word}\n"
                            corrected_words.append(corrected_word)

                        magnito_bot.send_message(
                            first_chat_id, message_to_user)
                        user_input.bag_of_words = all_words.difference(
                            wrong_words).union(corrected_words)

                    negative_result = False

                    if len(user_input.original_text) >= 3: # skips input if user text len < 3

                        list_of_matches = txt_folder.search_for_matches(
                            user_input.bag_of_words)
                        if list_of_matches:
                            magnito_bot.send_chat_action(
                                first_chat_id, 'upload_photo')
                            for name_of_file in list_of_matches:

                                with open(img_folder.path_to_img(name_of_file), 'rb') as photo_f:
                                    # send a corresponding picture
                                    magnito_bot.send_photo(first_chat_id, photo_f)

                                new_offset = first_update_id + 1



                        else:
                            negative_result = True
                    else:
                        negative_result = True

                    if negative_result:
                        magnito_bot.send_message(
                            first_chat_id, 'Sorry, there is nothing like that. Try something else!')
                        new_offset = first_update_id + 1

        except Exception as e:
            magnito_bot.send_message(376385737, e)
            # raise e
            new_offset = first_update_id + 1


if __name__ == '__main__':
    main()
