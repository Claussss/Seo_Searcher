from spellchecker import SpellChecker
from emoji import UNICODE_EMOJI
import re


class UserInput():
    '''Represents message sent by the user.'''

    def __init__(self, user_input):
        self._spell_checker = SpellChecker()
        self._text = user_input
        self.bag_of_words = set(self._text.lower().split()) # default bag of words of the text with english translation

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, new_text):
        self._text = new_text
        self.bag_of_words = set(self._text.lower().split())


    def has_mistakes(self):
        '''Returns True if there are mistakes'''
        return bool(self._spell_checker.unknown(self._text.split()))  # checking origin user input for mistakes (not translated)

    def has_cyrillic(self):
        '''Returns True if there are Cyrillic symbols'''
        return bool(re.search('[а-яА-Я]', self._text))

    def has_date(self):
        '''Returns True if there are dates'''
        return bool(re.search(r'\d{4}-\d{2}', self._text))

    def has_emoji(self):
        '''Returns True if there is an emoji'''
        for char in self._text:
            if char in UNICODE_EMOJI:
                return True

        return False

    def correct_mistakes_in_text(self):
        '''Corrects mistakes in the text by using SpellChecker module.
           Returns message to user with spelling corrections'''
        all_words = self.bag_of_words
        wrong_words = self._spell_checker.unknown(all_words)
        corrected_words = []
        message_to_user = "Spelling correction:\n"

        for wrong_word in wrong_words:
            corrected_word = self._spell_checker.correction(wrong_word)
            message_to_user += f"{wrong_word} -> {corrected_word}\n"
            corrected_words.append(corrected_word)

        self.bag_of_words = all_words.difference(wrong_words).union(corrected_words)

        return message_to_user



