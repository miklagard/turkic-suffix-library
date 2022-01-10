import turkic_suffix_library.languages.turkish.turkish_string as tr
import turkic_suffix_library.languages.turkish.consonants as con
from turkic_suffix_library.languages.common.turkic_class import TurkicClass


class TurkishClass(TurkicClass):
    def __init__(self, parameter_word: str, **kwargs):
        super().__init__(parameter_word, **kwargs)

        if kwargs.get('possessive', False):
            self.history.append({
                'action': 'possessive'
            })

        self.language = 'turkish'

    def make_plural(self):
        self.concat(f'l{self.letter_a()}r')

        return self.word

    def apostrophes(self, **kwargs):
        self.proper_noun = kwargs.get('proper_noun')

        if self.proper_noun and not self.apostrophes_applied:
            self.word += "'"
            self.apostrophes_applied = True

            return True
        else:
            return False

    def last_vowel(self):
        return tr.last_vowel(self.word)

    def letter_d(self):
        if self.last_letter_is_vowel() or not self.last_letter_is_hard():
            return 'd'
        else:
            return 't'

    def letter_a(self):
        if self.last_vowel().get('tone') == 'front':
            return 'a'
        else:
            return 'e'

    def minor(self):
        return con.MINOR_HARMONY.get(self.last_vowel().get('letter'), 'a')

    def letter_i(self):
        if self.last_vowel().get('tone') == 'front':
            return 'ı'
        else:
            return 'i'

    def last_letter(self):
        return tr.last_letter(self.last_word())

    def last_letter_is_vowel(self):
        return self.last_letter().get('letter') in con.VOWELS

    def last_letter_is_hard(self):
        return self.last_letter().get('letter') in con.HARD_CONSONANTS

    def if_ends_with_hard(self, concat_1, concat_2):
        if self.last_letter_is_hard():
            self.concat(concat_1)
        else:
            self.concat(concat_2)

    def if_ends_with_vowel(self, concat_text):
        if self.last_letter_is_vowel():
            self.concat(concat_text)

    def soften(self):
        self.word = tr.soften(self.word)
        return self.word

    def exception_missing(self):
        self.word = tr.exception_missing(self.word)
        return self.word

    def is_from_able(self):
        if len(self.history):
            action = self.history[-1].get('action')
            auxiliary = self.history[-1].get('kwargs', {}).get('auxiliary')

            if action == 'unify_verbs' and auxiliary == 'bil':
                return True

        return False

    def is_from_passive(self):
        if len(self.history):
            action = self.history[-1].get('action')

            if action == 'passive':
                return True

        return False

    def ng_change(self):
        word = self.last_word()

        for noun in con.NK_G_CHANGE:
            if word.endswith(noun):
                self.word = self.from_upper_or_lower(word[:-len(noun)] + con.NK_G_CHANGE.get(noun, self.word))
                return self.word

        return self.word

    def change_last_letter(self, letter):
        self.word = tr.change_last_letter(self.word, letter)
        return self.word

    def ends_with(self, letter):
        return self.last_letter().get('letter') == letter

    def if_ends_with(self, old_letter, new_letter):
        if self.ends_with(old_letter):
            self.change_last_letter(new_letter)

    def verb_in_minor_harmony_exception(self):
        word = self.last_word()

        return word in con.VERB_MINOR_HARMONY_EXCEPTIONS

    def harden_verb(self):
        lower = self.lower(self.word)

        for hard in con.VERBS_HARDEN:
            if lower.endswith(hard):
                self.word = tr.concat(
                    self.word[:-len(hard)], con.VERBS_HARDEN[hard]
                )

        return self.word

    def verbs_losing_vowels(self):
        self.word = self.from_upper_or_lower(
            con.VERBS_LOSING_VOWELS.get(self.lower(self.word), self.word)
        )
        return self.word

    def n_connector(self):
        if self.history:
            if self.history[-1].get('action') == 'possessive':
                return True

        return self.lower(self.word) in con.N_CONNECTOR

    def harmony_for_present(self):
        vowel = self.lower(self.last_vowel()['letter'])

        return con.HARMONY_FOR_PRESENT.get(vowel, vowel)

    def harmony_for_present_first(self):
        vowel = self.lower(self.last_vowel()['letter'])

        return con.HARMONY_FOR_PRESENT_FIRST.get(vowel, vowel)

    def count_syllable(self):
        vowel = self.last_vowel()

        return vowel['vowel_count']
