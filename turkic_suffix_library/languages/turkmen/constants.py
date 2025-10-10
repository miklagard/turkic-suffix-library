VOWELS = {
    'back': ('i', 'ü', 'e', 'ö', 'ä'),
    'front': ('y', 'u', 'o', 'a'),
    'close': ('i', 'ü', 'y', 'u'),
    'mid': ('e', 'ö', 'o'),
    'open': ('ä', 'a'),
    'unrounded': ('i', 'e', 'ä', 'y', 'a'),
    'rounded': ('ü', 'ö', 'u', 'o'),
}

CONSONANTS = {
    'nasal': ('m', 'n', 'ň'),
    'plosive':   ('p', 'b', 't', 'd', 'ç', 'j', 'k', 'g'),
    'voiceless': ('p', 't', 'ç', 'k', 's', 'ş', 'h'),
    'dental':    ('n', 't', 'd', 's', 'z', 'l', 'r'),
    'fricative': ('s', 'c', 'ş', 'h'),
    'approximant': ('w', 'l', 'ý'),
    'rhotic': ('r', ),
    'voiced': ('b', 'd', 'j', 'g', 'z'),
    'bilabial': ('m', 'p', 'b', 'w'),
    'postalveolar': ('ç', 'j', 'ş', 'ý'),
    'dorsal': ('ň', 'k', 'g', 'h')
}

SOFTEN = {
    'ç': 'j',
    'k': 'g',
    't': 'd',
    'p': 'b'
}

MISSING_VOWEL = {
    'akyl': 'akl',
    'bagyr': 'bagr',
    'burun': 'burn',
    'garyn': 'garn',
    'ogul': 'ogl',
    'uruş': 'urş',
    'ylym': 'ylm'
}

"""


ç -> j
k -> g


k dorsal, plosive, voiceless
g dorsal, plosive, voiced
ç postalveolar, plosive, voiceless
j postalveolar, plosive, voiced

Türkiýede
Aziýada
Ýewropada
şäherindä
tagtada
Dünýäde
"""