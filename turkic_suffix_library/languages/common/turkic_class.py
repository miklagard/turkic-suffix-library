class TurkicClass:
    def __init__(self, parameter_word: str, **kwargs):
        self.word = parameter_word
        self.stem = kwargs.get('stem', parameter_word)
        self.history = kwargs.get('history', [])
        self.language = kwargs.get('language')
        self.proper_noun = kwargs.get('proper_noun', False)
        self.apostrophes_applied = False

    def __str__(self):
        return self.word

    def to_string(self):
        return self.word

    def to_json(self):
        return {
            'result': self.word,
            'stem': self.stem,
            'history': self.history
        }

    def lower(self, parameter_word):
        word = parameter_word

        if self.language == 'turkish':
            word = word.replace('I', 'ı')

        return word.lower()

    def upper(self, parameter_word):
        if parameter_word is None:
            return ''

        word = parameter_word

        if self.language == 'turkish':
            word = word.replace('i', 'İ')

        return word.upper()

    def last_word(self):
        return self.lower(self.word).split(' ')[-1]

    def other_words_but_not_last(self):
        return ' '.join(self.lower(self.word).split(' ')[:-1])

    def concat(self, add_string):
        if self.word.isupper():
            self.word += self.upper(add_string)
        else:
            self.word += add_string

    def from_upper_or_lower(self, new_word):
        if self.word[len(self.word) - 1].isupper():
            return_data = self.lower(new_word)
        else:
            if self.word[0].isupper():
                return_data = new_word[0] + self.upper(new_word[1:])
            else:
                return_data = self.lower(new_word)

        return return_data

    def if_condition(self, person, plural, *args):
        for arg in args:
            person_param = arg[0]
            plural_param = arg[1]
            suffix = arg[2]

            if person == person_param and plural_param == plural:
                self.concat(suffix)
                return self.word

        return self.word

    def change_last_letter(self, new_last_letter):
        self.word = self.word[0:len(self.word) - 1] + new_last_letter

        return self.word


    def replace_word(self, new_word):
        self.word = self.from_upper_or_lower(new_word)


    def replace_last_letter(self):
        self.word = self.word[:-1]
