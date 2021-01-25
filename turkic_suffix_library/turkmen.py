import inspect
from turkic_suffix_library.languages.turkmen.turkmen_class import TurkmenClass


class Turkmen(TurkmenClass):
    def common_return(self, **kwargs):
        self.history.append({
            'action': inspect.stack()[1][3],
            'current': self.word,
            'kwargs': kwargs
        })

        return Turkmen(
            self.word,
            stem=self.stem,
            history=self.history
        )

    def plural(self):
        if self.word == 'ol':
            self.from_upper_or_lower('olar')
        else:
            self.concat(f'l{self.letter_a()}r')

        return self.common_return()

    def accusative(self):
        if self.lower(self.word) == 'ol':
            self.word = self.from_upper_or_lower('ony')
        else:
            self.soften()

            if self.last_letter_is_vowel():
                self.concat('ý')

            self.concat(self.minor())

        return self.common_return()
