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
        '''Returns True if there are mistakes'''
        return bool(self.spell_checker.unknown(self.original_text.split())) # checking origin user input for mistakes (not translated)

    def has_cyrillic(self):
        '''Returns True if there are Cyrillic symbols'''
        return bool(re.search('[а-яА-Я]', self.original_text))

    def has_date(self):
        '''Returns True if there are dates'''
        return bool(re.search(r'\d{4}-\d{2}', self.original_text))
