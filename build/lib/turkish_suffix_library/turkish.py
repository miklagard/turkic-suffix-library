import inspect

from turkish_suffix_library.turkish_class import TurkishClass

from turkish_suffix_library.consonants import MINOR_HARMONY, MINOR_HARMONY_FOR_FUTURE, PASSIVE_EXCEPTION


class Turkish(TurkishClass):
    def common_return(self, **kwargs):
        self.history.append({
            'action': inspect.stack()[1][3],
            'current': self.word,
            'kwargs': kwargs
        })

        return Turkish(
            self.word,
            stem=self.stem,
            history=self.history
        )

    def plural(self, **kwargs):
        self.concat(f'l{self.letter_a()}r')

        return self.common_return(**{})
    
    def apostrophes(self, **kwargs):
        if kwargs.get('proper_noun'):
            self.concat("'")
            return True
        else:
            return False

    def accusative(self, **kwargs):
        """
            -i hali
            (not finished yet)
        """

        if not self.apostrophes(**kwargs):
            self.word = self.exception_missing(kwargs.get('proper_noun'))

        if self.last_letter_is_vowel():
            if self.n_connector():
                self.concat('n')
            else:
                self.concat('y')

        self.ng_change()
        self.soften()

        self.concat(self.minor())

        return self.common_return(**kwargs)

    def dative(self, **kwargs):
        """
            -e hali
        """

        # firstly exceptions for ben (I) and you (sen)

        lower_word = self.lower()

        proper_noun = self.apostrophes(**kwargs)

        if lower_word == 'ben' and not proper_noun:
            self.word = self.from_upper_or_lower('bana')
        elif lower_word == 'sen' and not proper_noun:
            self.word = self.from_upper_or_lower('sana')
        else:
            self.ng_change()
            self.word = self.exception_missing(proper_noun)

            if self.last_letter_is_vowel():
                if self.n_connector():
                    self.concat('n')
                else:
                    self.concat('y')

            self.soften()

            self.concat(self.letter_a())

        return self.common_return(**kwargs)

    def ablative(self, **kwargs):
        """
            -den hali
        """
        self.apostrophes(**kwargs)
        ae = self.letter_a()

        if self.n_connector():
            self.concat('n')

        self.if_ends_with_hard('t', 'd')

        self.concat(f'{ae}n')

        return self.common_return(**kwargs)

    def locative(self, **kwargs):
        """
            -de hali
        """
        self.apostrophes(**kwargs)

        if self.n_connector():
            self.concat('n')

        self.if_ends_with_hard('t', 'd')

        self.concat(self.letter_a())

        return self.common_return(**kwargs)

    def genitive(self, **kwargs):
        """
            Iyelik aitlik eki
            Ayakkabinin
            Elif'in
        """

        last_letter_is_vowel = self.last_letter_is_vowel()
        proper_noun = self.apostrophes(**kwargs)
        minor = self.minor()

        if proper_noun:
            if last_letter_is_vowel:
                self.concat('n')
        else:
            self.ng_change()

            if last_letter_is_vowel:
                self.concat('n')
            else:
                self.soften()

                self.exception_missing(proper_noun)

        self.concat(f'{minor}n')

        return self.common_return(**kwargs)

    def equalative(self, **kwargs):
        """
            Ismin esitlik hali: -ce, -ca etc.
        """

        self.if_ends_with_hard('ç', 'c')
        self.concat(self.letter_a())

        return self.common_return(**kwargs)

    def instrumental(self, **kwargs):
        """
            Ismin vasıta hali: -le, -la, -yle, -yla
        """
        is_vowel = self.last_letter_is_vowel()

        self.apostrophes(**kwargs)

        ae = self.letter_a()

        if is_vowel:
            self.concat('y')

        self.concat(f'l{ae}')

        return self.common_return(**kwargs)

    def possessive(self, **kwargs):
        """
            Iyelik tamlanan eki
            Ayakkabısı
        """
        person = str(kwargs.get('person', 3))

        is_plural = kwargs.get('plural', False)

        proper_noun = self.apostrophes(**kwargs)

        if not (person == '3' and is_plural):
            if not proper_noun:
                self.soften()

                self.exception_missing(proper_noun)

        minor = self.minor()

        if not is_plural:
            if person == '1':
                self.ng_change()

                if not self.last_letter_is_vowel():
                    self.concat(minor)

                self.concat('m')

            elif person == '2':
                self.ng_change()

                if not self.last_letter_is_vowel():
                    self.concat(minor)

                self.concat('n')

            elif person == '3':
                self.ng_change()

                if self.last_letter_is_vowel():
                    self.concat('s')

                self.concat(minor)
        else:
            if person == '1':
                self.ng_change()

                if not self.last_letter_is_vowel():
                    self.concat(minor)

                self.concat(f'm{minor}z')

            elif person == '2':
                self.ng_change()

                if not self.last_letter_is_vowel():
                    self.concat(minor)

                self.concat(f'n{minor}z')
            else:
                if self.lower() == 'ism':
                    self.from_upper_or_lower('isim')

                self.word = self.plural().to_string()
                self.concat(minor)

        return self.common_return(**kwargs)

    def infinitive(self, **kwargs):
        """
            Mastar eki
        """

        ae = self.letter_a()

        from_able = self.is_from_able()

        if kwargs.get('negative', False) and not from_able:
            self.concat(f'm{ae}')

        self.concat(f'm{ae}k')

        return self.common_return(**kwargs)
    
    def present_continuous(self, **kwargs):
        """
            Şimdiki zaman
            Example: arıyorum
            Note: For alternative usage of present continuous tense, check the function
                    present_continuous_alternative
        """
        from_able = self.is_from_able()
        negative = kwargs.get('negative', False)

        if not negative:
            self.harden_verb()

            if self.last_letter_is_vowel():
                self.change_last_letter(self.minor())
            else:
                self.concat(self.minor())
        else:
            if not from_able:
                self.concat('m')
            else:
                self.word = self.word[:-1]

            self.concat(self.minor())

        self.concat('yor')

        if kwargs.get('question', False):
            if not kwargs.get('plural', False):
                if kwargs.get('person', 3) == 1:
                    self.concat(' muyum')
                elif kwargs.get('person', 3) == 2:
                    self.concat(' musun')
                elif kwargs.get('person', 3) == 3:
                    self.concat(' mu')
            else:
                if kwargs.get('person', 3) == 1:
                    self.concat(' muyuz')
                elif kwargs.get('person', 3) == 2:
                    self.concat(' musunuz')
                elif kwargs.get('person', 3) == 3:
                    self.word = self.plural().to_string()
                    self.concat(' m')
                    self.concat(self.letter_i())
        else:
            if not kwargs.get('plural', False):
                if kwargs.get('person', 3) == 1:
                    self.concat('um')
                elif kwargs.get('person', 3) == 2:
                    self.concat('sun')
            else:
                if kwargs.get('person', 3) == 1:
                    self.concat('uz')
                elif kwargs.get('person', 3) == 2:
                    self.concat('sunuz')
                elif kwargs.get('person', 3) == 3:
                    self.word = self.plural().to_string()

        return self.common_return(**kwargs)
    
    def present_continuous_alternative(self, **kwargs):
        """
            There are two ways to express 'present continuous tense in Turkish '
            This kind is not common in daily Turkish usage anymore
            Example:
                * aramaktayım
                * yapmaktayım
        """
        ae = self.letter_a()

        from_able = self.is_from_able()

        if kwargs.get('negative', False) and not from_able:
            self.concat(f'm{ae}')

        self.word = self.infinitive().to_string()

        self.concat(f't{ae}')

        if not kwargs.get('question', False):
            if not kwargs.get('plural', False):
                if kwargs.get('person', 3) == 1:
                    self.concat(f'y{self.minor()}m')
                elif kwargs.get('person', 3) == 2:
                    self.concat(f's{self.minor()}n')
            else:
                if kwargs.get('person', 3) == 1:
                    self.concat(f'y{self.minor()}z')
                elif kwargs.get('person', 3) == 2:
                    self.concat(f's{self.minor()}n')
                    self.concat(f'{self.minor()}z')
                elif kwargs.get('person', 3) == 3:
                    self.word = self.plural().to_string()
        elif kwargs.get('question', False):
            if not kwargs.get('plural', False):
                if kwargs.get('person', 3) == 1:
                    self.concat(f' m{self.minor}y')
                    self.concat(f'{self.minor()}m')
                elif kwargs.get('person', 3) == 2:
                    self.concat(f' m{self.minor()}s')
                    self.concat(f' {self.minor()}n')
            else:  # plural
                if kwargs.get('person', 3) == 1:
                    self.concat(f' m{self.minor()}y')
                    self.concat(f'{self.minor()}z')
                elif kwargs.get('person', 3) == 2:
                    self.concat(f' m{self.minor()}')
                    self.concat(f's{self.minor()}n')
                    self.concat(f'{self.minor()}z')
                elif kwargs.get('person', 3) == 3:
                    self.word = self.plural().to_string()
                    self.concat(f' m{self.minor()}')

        return self.common_return(**kwargs)
    
    def present_simple(self, **kwargs):
        """
            Geniş zaman
        """
        minor = self.minor()
        minor_harmony_letter_for_future = MINOR_HARMONY_FOR_FUTURE[self.last_vowel()['letter']]
        minor_harmony_for_future = MINOR_HARMONY_FOR_FUTURE[minor]

        ver_bil = self.word[-3:] in ('ver', 'bil')
        from_able = self.is_from_able()

        if not kwargs.get('negative', False):
            self.soften()

            self.harden_verb()

        if kwargs.get('question', False):
            if not kwargs.get('negative', False):

                if self.word in ['al', 'kal']:
                    self.concat('ır')
                else:
                    if not self.last_letter_is_vowel():
                        if ver_bil:
                            self.concat('i')
                        else:
                            self.concat(minor_harmony_letter_for_future)

                    self.concat('r')

                if not kwargs.get('plural', False):
                    if kwargs.get('person', 3) == 1:
                        self.concat(f' m{minor}y{minor}m')
                    elif kwargs.get('person', 3) == 2:
                        self.concat(f' m{minor}s{minor}n')
                    elif kwargs.get('person', 3) == 3:
                        self.concat(f' m{minor}')
                else:
                    if kwargs.get('person', 3) == 1:
                        self.concat(f' m{minor}y{minor}z')
                    elif kwargs.get('person', 3) == 2:
                        self.concat(f' m{minor}s{minor}n{minor}z')
                    elif kwargs.get('person', 3) == 3:
                        self.concat(f' m{minor}')
            elif kwargs.get('negative', False):
                ae = self.letter_a()
                
                if not from_able:
                    self.concat(f'm{ae}')

                self.concat(f'z')

                if not kwargs.get('plural', False):
                    if kwargs.get('person', 3) == 1:
                        self.concat(f' m{minor}y{minor}m')
                    elif kwargs.get('person', 3) == 2:
                        self.concat(f' m{minor}s{minor}n')
                    elif kwargs.get('person', 3) == 3:
                        self.concat(f' m{minor}')
                elif kwargs.get('plural', False):
                    if kwargs.get('person', 3) == 1:
                        self.concat(f' m{minor}y{minor}z')
                    elif kwargs.get('person', 3) == 2:
                        self.concat(f' m{minor}s{minor}n{minor}z')
                    elif kwargs.get('person', 3) == 3:
                        self.word = self.plural().to_string()
                        self.concat(f' m{minor}')
        elif not kwargs.get('question', False):
            if not kwargs.get('negative', False):
                if self.word in ['al', 'kal']:
                    self.concat('ır')
                else:
                    if not self.last_letter_is_vowel():
                        if self.word[-3:] in ('ver', 'bil'):
                            self.concat('i')
                        else:
                            self.concat(minor_harmony_letter_for_future)

                    self.concat('r')

                if not kwargs.get('plural', False):
                    if kwargs.get('person', 3) == 1:
                        self.concat(f'{minor}m')
                    elif kwargs.get('person', 3) == 2:
                        self.concat(f's{minor}n')
                else:
                    if kwargs.get('person', 3) == 1:
                        self.concat(f'{minor}z')
                    elif kwargs.get('person', 3) == 2:
                        self.concat(f's{minor}n{minor}z')
                    elif kwargs.get('person', 3) == 3:
                        self.word = self.plural().to_string()
            elif kwargs.get('negative', False):
                ae = self.letter_a()

                if not kwargs.get('plural', False):
                    if kwargs.get('person', 3) == 1:
                        if not from_able:
                            self.concat(f'm{ae}')
                        else:
                            self.concat(f'm')
                    elif kwargs.get('person', 3) == 2:
                        if not from_able:
                            self.concat('m')
                            self.concat(ae)
                        self.concat('z')
                        self.concat('s')
                        self.concat(MINOR_HARMONY[minor_harmony_for_future])
                        self.concat('n')
                    elif kwargs.get('person', 3) == 3:
                        if not from_able:
                            self.concat(f'm{ae}')
                        self.concat(f'z')
                else:
                    if kwargs.get('person', 3) == 1:
                        if not from_able:
                            self.concat(f'm{ae}')
                        self.concat('y')
                        self.concat(MINOR_HARMONY[minor_harmony_for_future])
                        self.concat('z')
                    elif kwargs.get('person', 3) == 2:
                        if not from_able:
                            self.concat('m{ae}')
                        self.concat('z')
                        self.concat('s')
                        self.concat(MINOR_HARMONY[ae])
                        self.concat('n')
                        self.concat(MINOR_HARMONY[ae])
                        self.concat('z')
                    elif kwargs.get('person', 3) == 3:
                        if not from_able:
                            self.concat(f'm{minor_harmony_letter_for_future}')
                        self.concat(f'z')
                        self.word = self.plural().to_string()

        return self.common_return(**kwargs)

    def future(self, **kwargs):
        """
            Gelecek zaman
        """
        ae = self.letter_a()

        from_able = self.is_from_able()

        if kwargs.get('negative', False) and not from_able:
            self.concat(f'm{ae}')

        if self.last_letter_is_vowel():
            self.verbs_losing_vowels()
            self.concat('y')

        self.soften()

        if not kwargs.get('negative', False):
            self.harden_verb()
        
        letter_a = self.letter_a()
        letter_i = self.letter_i()

        if kwargs.get('question', False):
            if kwargs.get('person', 3) == 3 and kwargs.get('plural', False):
                self.concat(f'{letter_a}c{letter_a}kl{letter_a}r ')
            else:
                self.concat(f'{letter_a}c{letter_a}k ')

            if not kwargs.get('plural', False):
                if kwargs.get('person', 3) == 1:
                    self.concat(f'm{letter_i}y{letter_i}m')
                elif kwargs.get('person', 3) == 2:
                    self.concat(f'm{letter_i}s{letter_i}n')
                elif kwargs.get('person', 3) == 3:
                    self.concat(f'm{letter_i}')
            else:
                if kwargs.get('person', 3) == 1:
                    self.concat(f'm{letter_i}y{letter_i}z')
                elif kwargs.get('person', 3) == 2:
                    self.concat(f'm{letter_i}s{letter_i}n{letter_i}z')
                elif kwargs.get('person', 3) == 3:
                    self.concat(f'm{letter_i}')

        elif not kwargs.get('question', False):
            if not kwargs.get('plural', False):
                if kwargs.get('person', 3) == 1:
                    self.concat(f'{letter_a}c{letter_a}ğ{letter_i}m')
                elif kwargs.get('person', 3) == 2:
                    self.concat(f'{letter_a}c{letter_a}ks{letter_i}n')
                elif kwargs.get('person', 3) == 3:
                    self.concat(f'{letter_a}c{letter_a}k')
            else:
                if kwargs.get('person', 3) == 1:
                    self.concat(f'{letter_a}c{letter_a}ğ{letter_i}z')
                elif kwargs.get('person', 3) == 2:
                    self.concat(f'{letter_a}c{letter_a}ks{letter_i}n{letter_i}z')
                elif kwargs.get('person', 3) == 3:
                    self.concat(f'{letter_a}c{letter_a}kl{letter_a}r')

        return self.common_return(**kwargs)
    
    def learned_past(self, **kwargs):
        """
            Not the same with English past perfect tense
            This usage is for past tense of an action which is heared/learned but not witnessed.
            mişli geçmiş zaman veya öğrenilen geçmiş zaman
        """

        ae = self.letter_a()

        from_able = self.is_from_able()

        if kwargs.get('negative', False) and not from_able:
            self.concat(f'm{ae}')

        minor = self.minor()

        self.concat(f'm{minor}ş')

        if not kwargs.get('question', False):
            if not kwargs.get('plural', False):
                if kwargs.get('person', 3) == 1:
                    self.concat(f'{minor}m')
                elif kwargs.get('person', 3) == 2:
                    self.concat(f's{minor}n')
            else:
                if kwargs.get('person', 3) == 1:
                    self.concat(f'{minor}z')
                elif kwargs.get('person', 3) == 2:
                    self.concat(f's{minor}n{minor}z')
                elif kwargs.get('person', 3) == 3:
                    self.word = self.plural().to_string()
        elif kwargs.get('question', False):
            if not kwargs.get('plural', False):
                if kwargs.get('person', 3) == 1:
                    self.concat(f' m{minor}y{minor}m')
                elif kwargs.get('person', 3) == 2:
                    self.concat(f' m{minor}s{minor}n')
                elif kwargs.get('person', 3) == 3:
                    self.concat(f' m{minor}')
            else:
                if kwargs.get('person', 3) == 1:
                    self.concat(f' m{minor}y{minor}z')
                elif kwargs.get('person', 3) == 2:
                    self.concat(f' m{minor}s{minor}n{minor}z')
                elif kwargs.get('person', 3) == 3:
                    self.word = self.plural().to_string()
                    self.concat(f' m{minor}')

        return self.common_return(**kwargs)
    
    def unify_verbs(self, **kwargs):
        """
            Unified verbs (Birleşik fiiler) (Not a suffix but for 'can-bil' modal verb, this is necessary)
            Ability - Yeterlilik: kızabil (bil) (English modal auxiliary verb: Can)
            Swiftness - Tezlik: koşuver (ver)
            Continuity - Süreklilik: gidedur, bakakal, alıkoy (dur, kal, gel, koy)
            Approach - Yaklaşma: (yaz) düzeyaz
        """
        self.verbs_losing_vowels()

        minor = self.minor()

        self.concat_if_ends_with_vowel('y')

        self.soften()
        ae = self.letter_a()

        self.harden_verb()

        if not kwargs.get('negative', False):
            if kwargs.get('auxiliary') in ['ver', 'koy']:
                self.concat(minor)
            else:
                self.concat(ae)

            self.concat(kwargs.get('auxiliary'))
        if kwargs.get('negative', False):
            if kwargs.get('auxiliary') == 'bil':
                self.concat(f'{ae}m{ae}')
            else:
                if kwargs.get('auxiliary') in ['ver', 'koy']:
                    self.concat(minor)
                else:
                    self.concat(ae)

                self.concat(kwargs.get('auxiliary'))

                self.concat(ae)

        return self.common_return(**kwargs)

    
    def must(self, **kwargs):
        """
            Gereklilik kipi
        """

        letter_a = self.letter_a()
        letter_i = self.letter_i()
        from_able = self.is_from_able()

        if kwargs.get('negative', False) and not from_able:
            self.concat(f'm{letter_a}')

        self.concat(f'm{letter_a}l{letter_i}')
        
        if kwargs.get('person', 3) == 3 and kwargs.get('plural', False):
            self.word = self.plural().to_string()

        if kwargs.get('question', False):
            self.concat(f' m{letter_i}')

        if not kwargs.get('plural', False):
            if kwargs.get('person', 3) == 1:
                self.concat(f'y{letter_i}m')
            elif kwargs.get('person', 3) == 2:
                self.concat(f's{letter_i}n')
        else:
            if kwargs.get('person', 3) == 1:
                self.concat(f'y{letter_i}z')
            elif kwargs.get('person', 3) == 2:
                self.concat(f's{letter_i}n{letter_i}z')

        return self.common_return(**kwargs)
    
    def wish_condition(self, **kwargs):
        """
            Dilek - Şart kipi (-se, -sa)
        """
        letter_a = self.letter_a()
        letter_i = self.letter_i()

        from_able = self.is_from_able()

        if kwargs.get('negative', False) and not from_able:
            self.concat(f'm{letter_a}')

        self.concat(f's{letter_a}')

        if not kwargs.get('plural', False):
            if kwargs.get('person', 3) == 1:
                self.concat('m')
            elif kwargs.get('person', 3) == 2:
                self.concat('n')
        else:  # Plural
            if kwargs.get('person', 3) == 1:
                self.concat('k')
            elif kwargs.get('person', 3) == 2:
                self.concat(f'n{letter_i}z')
            elif kwargs.get('person', 3) == 3:
                self.word = self.plural().to_string()

        if kwargs.get('question', False):
            self.concat(f' m{letter_i}')

        return self.common_return(**kwargs)

    
    def wish(self, **kwargs):
        """
            İstek kipi (geleyim, gelesin, gele, gelelim, gelesiniz, geleler)
        """
        letter_a = self.letter_a()
        letter_i = self.letter_i()

        from_able = self.is_from_able()

        if kwargs.get('negative', False):
            if not from_able:
                self.concat(f'y{letter_a}')
            self.concat(f'y{letter_a}')
        else:
            self.verbs_losing_vowels()

            self.harden_verb()

            self.concat_if_ends_with_vowel('y')

            self.soften()

            self.concat(letter_a)

        if not kwargs.get('plural', False):
            if kwargs.get('person', 3) == 1:
                self.concat(f'y{letter_i}m')
            elif kwargs.get('person', 3) == 2:
                self.concat(f's{letter_i}n')
        else:
            if kwargs.get('person', 3) == 1:
                self.concat(f'l{letter_i}m')
            elif kwargs.get('person', 3) == 2:
                self.concat(f's{letter_i}n{letter_i}z')
            elif kwargs.get('person', 3) == 3:
                self.word = self.plural().to_string()

        if kwargs.get('question', False):
            self.concat(f' m{letter_i}')

        return self.common_return(**kwargs)

    def command(self, **kwargs):
        """
            Make the verb command
            Usage: do it, break it, come!
            As different from English, command optative mood is valid also for 3rd person in Turkish
                but never for 1st person.
            For the second person, there is no suffix
        """

        ae = self.letter_a()

        from_able = self.is_from_able()

        if kwargs.get('negative', False) and not from_able:
            self.concat(f'm{ae}')

        minor = self.minor()

        if not kwargs.get('plural', False):
            if kwargs.get('person', 2) == 3:
                self.concat(f's{minor}n')

                if kwargs.get('question', False):
                    self.concat(f' m{minor}')
        else:  # Plural
            if kwargs.get('person', 2) == 2:
                self.verbs_losing_vowels()

                self.concat_if_ends_with_vowel('y')

                self.soften()

                self.harden_verb()

                self.concat(f'{minor}n')

                if kwargs.get('formal', False):
                    self.concat(f'{minor}z')
            elif kwargs.get('person', 2) == 3:
                self.concat(f's{minor}n')
                self.word = self.plural().to_string()
                if kwargs.get('question', False):
                    self.concat(f' m{minor}')

        return self.common_return(**kwargs)

    def past(self, **kwargs):
        """
            Past tense
            -di'li geçmiş zaman
        """
        
        ae = self.letter_a()

        from_able = self.is_from_able()

        if kwargs.get('negative', False) and not from_able:
            self.concat(f'm{ae}')

        minor = self.minor()

        if self.last_letter_is_vowel() or not self.last_letter_is_hard():
            ps = 'd'
        else:
            ps = 't'

        if not kwargs.get('plural', False):
            if kwargs.get('person', 3) == 1:
                self.concat(f'{ps}{minor}m')
            elif kwargs.get('person', 3) == 2:
                self.concat(f'{ps}{minor}n')
            elif kwargs.get('person', 3) == 3:
                self.concat(f'{ps}{minor}')
        else:  # plural
            if kwargs.get('person', 3) == 1:
                self.concat(f'{ps}{minor}k')
            elif kwargs.get('person', 3) == 2:
                self.concat(f'{ps}{minor}n{minor}z')
            elif kwargs.get('person', 3) == 3:
                self.concat(f'{ps}{minor}')
                self.word = self.plural().to_string()

        if kwargs.get('question', False):
            minor = self.minor()

            self.concat(f' m{minor}')

        return self.common_return(**kwargs)

    def past_past(self, **kwargs):
        """
            Bilinen geçmiş zamanın hikayesi
            yaptıydım, yaptıydın, yaptıydı, yaptıydık, yaptıydınız, yaptıydılar
            yaptı mıydım, yaptı mıydın, yaptı mıydı, yaptı mıydık, yaptı mıydınız, yaptılar mıydı
        """

        if kwargs.get('person', 3) == 3 \
                and kwargs.get('question', False) \
                and kwargs.get('plural', False):
            self.word = self.past(
                person=3,
                plural=False,
                negative=kwargs.get('negative', False),
            ).to_string()
        else:
            self.word = self.past(
                person=3,
                plural=False,
                negative=kwargs.get('negative', False),
                question=kwargs.get('question', False)
            ).to_string()

            self.concat('y')

        if kwargs.get('person', 3) == 3 \
                and kwargs.get('question', False) \
                and kwargs.get('plural', False):

            self.word = self.plural().to_string()

            self.concat(' m')
            self.concat(self.letter_i())
        else:
            self.word = self.past(
                person=kwargs.get('person', 3),
                plural=kwargs.get('plural', False)
            ).to_string()

        return self.common_return(**kwargs)

    def past_condition(self, **kwargs):
        """
            Bilinen geçmiş zamanın şartı
                durduysam, durduysan, durduysa, durduysak, durduysanız, durdularsa
                dursa mıydım, dursa mıydın, dursa mıydı, dursa mıydık, dursalar mıydı
        """

        if not kwargs.get('question', False):
            self.word = self.past(
                person=3,
                negative=kwargs.get('negative', False)
            ).to_string()

            self.concat('y')

            self.word = self.wish_condition(
                person=kwargs.get('person', 3),
                plural=kwargs.get('plural', False)
            ).to_string()
        else:
            self.word = self.wish_condition(
                person=3,
                negative=kwargs.get('negative', False)
            ).to_string()

            if kwargs.get('person', 3) == 3 and kwargs.get('plural', False):
                self.word = self.plural().to_string()

            letter_i = self.letter_i()

            self.concat(f' m{letter_i}yd{letter_i}')

            if not kwargs.get('plural', False):
                if kwargs.get('person', 3) == 1:
                    self.concat('m')
                elif kwargs.get('person', 3) == 2:
                    self.concat('n')
            else:
                if kwargs.get('person', 3) == 1:
                    self.concat('k')
                elif kwargs.get('person', 3) == 2:
                    self.concat(f'n{letter_i}z')

        return self.common_return(**kwargs)

    def past_learned_past(self, **kwargs):
        """
            Öğrenilen geçmiş zamanın hikayesi
            Yapmışlardı (-miş -di)
            Example: It is heard by someone that somebody did something in the past
        """

        if kwargs.get('person') == 3 and kwargs.get('plural', False) and kwargs.get('question', False):
            self.word = self.learned_past(
                negative=kwargs.get('negative', False),
                question=kwargs.get('question', False),
                person=kwargs.get('person', 3),
                plural=kwargs.get('plural', False)
            ).to_string()
        else:
            self.word = self.learned_past(
                negative=kwargs.get('negative', False),
                question=kwargs.get('question', False),
            ).to_string()

        if kwargs.get('question', False):
            self.concat('y')

        if kwargs.get('person') == 3 and kwargs.get('plural', False) and kwargs.get('question', False):
            self.word = self.past(person=kwargs.get('person', 3)).to_string()
        else:
            self.word = self.past(
                person=kwargs.get('person', 3),
                plural=kwargs.get('plural', False)
            ).to_string()

        return self.common_return(**kwargs)

    def learned_past_learned_past(self, **kwargs):
        """
            Öğrenilen geçmiş zamanın rivayeti
            Duymuşmuşum Duymuşmuşsun Duymuşmuş Duymuşmuşuz Duymuşmuşunuz Duymuşmuşlar
            Duymuş mumuymuşum? Duymuş mumuymuşsun? Duymuş mumuymuş? Duymuş mumuymuşuz?
            Duymuş mumuymuşsunuz Duymuşlar mıymış?
        """

        self.word = self.learned_past(negative=kwargs.get('negative', False)).to_string()

        if not kwargs.get('question', False):
            self.word = self.learned_past(
                person=kwargs.get('person', 3),
                plural=kwargs.get('plural', False),
                question=kwargs.get('question', False)
            ).to_string()
        else:
            if kwargs.get('person', 3) == 3 and kwargs.get('plural', False):
                self.word = self.plural().to_string()
                minor = self.minor()

                self.concat(f' m{minor}ym{minor}ş')
            else:
                minor = self.minor()
                self.concat(f' m{minor}y')
                self.word = self.learned_past(
                    person=kwargs.get('person', 3),
                    plural=kwargs.get('plural', False)
                ).to_string()

        return self.common_return(**kwargs)

    def learned_past_future(self, **kwargs):
        """
            Gelecek zamanın rivayeti
            Yapacaklardı (-acak -mış)
            Example: It is heard by someone that somebody will do something in the past
        """

        if kwargs.get('person') == 3 and kwargs.get('plural', False) and kwargs.get('question', False):
            self.word = self.future(
                negative=kwargs.get('negative', False),
                question=kwargs.get('question', False),
                person=kwargs.get('person', 3),
                plural=kwargs.get('plural', False)
            ).to_string()
        else:
            self.word = self.future(
                negative=kwargs.get('negative', False),
                question=kwargs.get('question', False),
            ).to_string()

        if kwargs.get('person') == 3 and kwargs.get('plural', False) and kwargs.get('question', False):
            self.concat('m')
            self.concat(self.minor())
            self.concat('y')
            self.word = self.learned_past(person=kwargs.get('person', 3)).to_string()
        else:
            if kwargs.get('question', False):
                self.concat('y')

            self.word = self.learned_past(
                person=kwargs.get('person', 3),
                plural=kwargs.get('plural', False)
            ).to_string()

        return self.common_return(**kwargs)

    def past_future(self, **kwargs):
        """
            Gelecek zamanın hikayesi
                Yapacaklardı (-acak -tı)
                Example: Somebody will do something in the past
        """

        if kwargs.get('person') == 3 and kwargs.get('plural', False) and kwargs.get('question', False):
            self.word = self.future(
                negative=kwargs.get('negative', False),
                question=kwargs.get('question', False),
                person=kwargs.get('person', 3),
                pplural=kwargs.get('plural', False)
            ).to_string()
        else:
            self.word = self.future(
                negative=kwargs.get('negative', False),
                question=kwargs.get('question', False)
            ).to_string()

        if kwargs.get('person') == 3 and kwargs.get('plural', False) and kwargs.get('question', False):
            self.concat('m')
            self.concat(self.minor())
            self.concat('y')
            self.word = self.past(person=kwargs.get('person', 3)).to_string()
        else:
            if kwargs.get('question', False):
                self.concat('y')

            self.word = self.past(
                person=kwargs.get('person', 3),
                plural=kwargs.get('plural', False)
            ).to_string()

        return self.common_return(**kwargs)

    def ordinal(self, **kwargs):
        """
            Ordinal numbers: One->First, Two->Second etc.

            bir-i-nci, iki-nci...

            This rule is also valid for words:
            * son (last) -> sonuncu
            * ilk (first) -> ilkinci (ilk already means "first" but you can still put this suffix)
        """

        minor = self.minor()

        self.if_ends_with('t', 'd')

        if not self.last_letter_is_vowel():
            self.concat(minor)

        self.concat(f'nc{minor}')

        return self.common_return(**kwargs)

    def distributive(self, **kwargs):
        """
            Distributive numbers: One->One each, Two->Two each.

            bir-er, iki-şer...
        """

        ae = self.letter_a()

        self.if_ends_with('t', 'd')

        if self.last_letter_is_vowel():
            self.concat('ş')

        self.concat(f'{ae}r')

        return self.common_return(**kwargs)

    def passive(self, **kwargs):
        """
            Turns verb into passive (edilgen):

            Kirdim -> Kirildim
            I brake -> I am broken

            Use passive always before conjuncting the verb with tense and person

            Example:
            Turkish('ver').passive().present_continuous_alternative(person=1)
            verilmekteyim
        """
        self.harden_verb()

        minor = self.minor()
        lower_word = self.lower()

        if lower_word in PASSIVE_EXCEPTION:
            self.from_upper_or_lower(PASSIVE_EXCEPTION.get(lower_word))
        else:
            if self.last_letter_is_vowel():
                self.concat('n')

            self.concat(f'{minor}l')

        return self.common_return(**kwargs)
    
    def adverb_during_action(self, **kwargs):
        """
            Giderken etc. (iken)

            Generates adverb-verb for "while", doing two things together:

            He was smoking while sipping vodka.
            Sigara icerken vodka yudumluyordu.

            Use this method after conjuncting the verb with tense and person

            Person should be always 3rd person plural or 3rd person singular

            Example:
            Turkish('ver').present_continuous_alternative(person=3).adverb_during_action()
        """
        self.concat_if_ends_with_vowel('y')

        self.concat(f'ken')

        return self.common_return(**kwargs)
    
    def adverb_continuity(self, **kwargs):
        """
            Git -> Gide gide etc. (-e)

            Use this method without conjuncting
        """
        ae = self.letter_a()

        from_able = self.is_from_able()

        if kwargs.get('negative'):
            if not from_able:
                self.concat(f'm{ae}')

            self.concat('y')
        else:
            self.harden_verb()

            self.concat_if_ends_with_vowel('y')

        self.concat(ae)

        self.word = f'{self.word} {self.word}'

        return self.common_return(**kwargs)

    def adverb_repeatedly(self, **kwargs):
        """
            Git -> Gide gide etc. (-e)

            Use this method without conjuncting
        """
        ae = self.letter_a()

        self.word = self.past(
            negative=kwargs.get('negative'),
            person=1,
            plural=True
        ).to_string()

        self.concat(f'ç{ae}')

        return self.common_return(**kwargs)

    def adverb_after_action(self, **kwargs):
        """
            Gidince etc. (-nca)

            Generates adverb-verb for "after"

            Use this method without any conjuncting
        """

        ae = self.letter_a()
        letter_i = self.letter_i()
        minor = self.minor()
        from_able = self.is_from_able()

        self.harden_verb()

        if kwargs.get('negative'):
            if not from_able:
                self.concat(f'm{ae}')
            
            self.concat(f'y{letter_i}')
        elif self.last_letter_is_vowel():
            self.concat(f'y{minor}')
        else:
            self.concat(f'{minor}')

        self.concat(f'nc{ae}')

        return self.common_return(**kwargs)

    def adverb_after_action_alternative(self, **kwargs):
        """
            Gidip etc. (-p)

            Generates adverb-verb for "after"

            Use this method without any conjuncting
        """

        ae = self.letter_a()
        minor = self.minor()

        from_able = self.is_from_able()

        if kwargs.get('negative'):
            if not from_able:
                self.concat(f'm{ae}')

            self.concat('y')
        elif self.last_letter_is_vowel():
            self.concat('y')
        else:
            self.harden_verb()

        self.concat(f'{minor}p')

        return self.common_return(**kwargs)

    def adverb_without_action(self, **kwargs):
        """
            Gitmeden etc. (-madan)

            Generates adverb-verb for "without action"

            Use this method without any conjuncting
        """

        ae = self.letter_a()

        from_able = self.is_from_able()

        if not from_able:
            self.concat(f'm{ae}')

        self.concat(f'd{ae}n')

        return self.common_return(**kwargs)

    def adverb_without_action_alternative(self, **kwargs):
        """
            Gitmeksizin etc. (-meksizin)

            Generates adverb-verb for "without action"

            Use this method without any conjuncting
        """

        letter_i = self.letter_i()
        self.word = self.infinitive().to_string()
        self.concat(f's{letter_i}z{letter_i}n')

        return self.common_return(**kwargs)

    def adverb_by_action(self, **kwargs):
        """
            Giderek etc. (-erek)

            Generates adverb-verb for "by action"

            Use this method without any conjuncting
        """

        ae = self.letter_a()

        from_able = self.is_from_able()

        if kwargs.get('negative'):
            if not from_able:
                self.concat(f'm{ae}')
        else:
            self.harden_verb()
            
        self.concat_if_ends_with_vowel('y')

        self.concat(f'{ae}r{ae}k')

        return self.common_return(**kwargs)
    
    def adverb_since_action(self, **kwargs):
        """
            Gideli etc. (-eli)

            Generates adverb-verb for "since action"

            Use this method without any conjuncting
        """

        ae = self.letter_a()
        letter_i = self.letter_i()

        from_able = self.is_from_able()

        if kwargs.get('negative'):
            if not from_able:
                self.concat(f'm{ae}')
        else:
            self.harden_verb()

        self.concat_if_ends_with_vowel('y')

        self.concat(f'{ae}l{letter_i}')

        return self.common_return(**kwargs)
