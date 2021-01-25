import inspect
from turkic_suffix_library.languages.kazakh.kazakh_class import KazakhClass


class Kazakh(KazakhClass):
    def common_return(self, **kwargs):
        self.history.append({
            'action': inspect.stack()[1][3],
            'current': self.word,
            'kwargs': kwargs
        })

        return Kazakh(
            self.word,
            stem=self.stem,
            history=self.history
        )

    def plural(self, **kwargs):
        return self.common_return(**kwargs)

    def accusative(self, **kwargs):
        return self.common_return(**kwargs)
