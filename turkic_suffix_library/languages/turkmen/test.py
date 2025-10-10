from turkic_suffix_library.turkmen import Turkmen
from turkic_suffix_library.languages.turkmen.nouns import NOUNS

for noun in NOUNS:
    # print(noun, ' -> ', Turkmen(noun).plural())
    print(noun, ' -> ', Turkmen(noun).accusative())
    # print(noun, ' -> ', Turkmen(noun).dative())
