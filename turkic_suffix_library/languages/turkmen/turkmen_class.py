from turkic_suffix_library.languages.common.turkic_class import TurkicClass
from turkic_suffix_library.languages.turkmen import constants as constants


class TurkmenClass(TurkicClass):
    def __init__(self, parameter_word: str, **kwargs):
        super().__init__(parameter_word, **kwargs)
        self.language = 'turkmen'

    def last_vowel(self):
        word = self.last_word()

        vowel_count = 0

        return_data = ''

        for letter in word:
            if letter in constants.VOWELS['front']:
                vowel_count = vowel_count + 1
                return_data = {'letter': letter, 'tone': 'front'}
            elif letter in constants.VOWELS['back']:
                vowel_count = vowel_count + 1
                return_data = {'letter': letter, 'tone': 'back'}

        if return_data == '':
            return_data = {'letter': '', 'tone': 'back'}

        return_data['vowel_count'] = vowel_count

        return return_data

    def letter_a(self):
        if self.last_vowel().get('tone') == 'front':
            return 'a'
        else:
            return 'e'

    def letter_i(self):
        if self.last_vowel().get('tone') == 'front':
            return 'y'
        else:
            return 'i'

    def count_syllable(self):
        vowel = self.last_vowel()

        return vowel['vowel_count']

    def last_letter(self):
        return self.lower(self.word[-1])

    def soften(self):
        last_letter = self.last_letter()

        self.change_last_letter(constants.SOFTEN.get(last_letter, last_letter))

        return self.word

    def last_letter_is_vowel(self):
        letter = self.last_letter()

        return letter in constants.VOWELS.get('front') or letter in constants.VOWELS.get('back')

    def missing_vowel(self):
        lower = self.lower(self.word)

        self.word = self.from_upper_or_lower(constants.MISSING_VOWEL.get(lower, self.word))

        return self.word

    def change_e(self):
        lower = self.lower(self.word)

        if lower.endswith('e'):
            self.change_last_letter('ä')

        return self.word

    def first_vowel(self):
        word = self.last_word()

        for letter in word:
            if letter in constants.VOWELS.get('front') or letter in constants.VOWELS.get('back'):
                return letter

    def change_yi(self):
        lower = self.lower(self.word)
        if self.count_syllable() == 2:
            vowel = self.first_vowel()

            if vowel in constants.VOWELS.get('rounded'):
                if lower.endswith('y'):
                    self.change_last_letter('u')
                elif lower.endswith('i'):
                    self.change_last_letter('ü')

        return self.word
