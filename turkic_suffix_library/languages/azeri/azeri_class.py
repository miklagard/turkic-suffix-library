from turkic_suffix_library.languages.common.turkic_class import TurkicClass


class AzeriClass(TurkicClass):
    def __init__(self, parameter_word: str, **kwargs):
        super().__init__(parameter_word, **kwargs)
        self.language = 'azeri'
