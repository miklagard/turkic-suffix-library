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
        lower = self.lower(self.word)
        if lower == 'ol':
            self.word = self.from_upper_or_lower('olar')
        elif lower == 'men':
            self.word = self.from_upper_or_lower('biz')
        elif lower == 'sen':
            self.word = self.from_upper_or_lower('siz')
        elif lower == 'sen':
            self.word = self.from_upper_or_lower('siz')
        else:
            self.change_yi()

            self.concat(f'l{self.letter_a()}r')

        return self.common_return()

    def accusative(self):
        """
            -i hali
        """

        if self.lower(self.word) == 'ol':
            self.word = self.from_upper_or_lower('ony')
        else:
            self.missing_vowel()
            self.soften()
            self.change_e()

            if self.last_letter_is_vowel():
                self.concat('n')

            self.concat(self.letter_i())

        return self.common_return()

    def dative(self):
        """
            -e hali
        """
        lower = self.lower(self.word)

        if lower == 'ol':
            self.word = self.from_upper_or_lower('oňa')
        elif lower == 'sen':
            self.word = self.from_upper_or_lower('saňa')
        elif lower == 'men':
            self.word = self.from_upper_or_lower('maňa')
        else:
            self.missing_vowel()
            self.soften()
            self.change_e()

            if self.last_letter_is_vowel():
                self.concat('n')

            self.concat(self.letter_a())

        return self.common_return()
