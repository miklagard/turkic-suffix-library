Turkish.py
==========

### Turkish Suffix Library for Python

## Install 
    pip install turkish-suffix-library

## Using

#### Nouns
    from turkish_suffix_library.turkish import Turkish

    print(f'{Turkish("Elif").genitive(proper_noun=True)} {Turkish("öküz").possessive(person=3)}.')

    print(Turkish('Öykü').genitive(proper_noun=True))
    print(Turkish('Cem').dative(proper_noun=True))
    print(Turkish('Nil').dative(proper_noun=True))
    print(Turkish('ALİ').dative(proper_noun=True))
    print(Turkish('Taylan').ablative(proper_noun=True))
    print(Turkish('Amasya').accusative(proper_noun=True))
    print(Turkish('ağaç').genitive(proper_noun=False))
    print(Turkish('erik').accusative(proper_noun=False))
    print(Turkish('Erik').accusative(proper_noun=True))
    print(Turkish('kavanoz').possessive(person=1))
    print(Turkish('kavanoz').possessive(person=2))
    print(Turkish('kavanoz').possessive(person=3))
    print(Turkish('halter').possessive(person=1, plural=True))
    print(Turkish('halter').possessive(person=2, plural=True))
    print(Turkish('halter').possessive(person=3, plural=True))
    print(Turkish('Kenya').possessive(person=3, plural=True))
    print(Turkish('çanta').plural().possessive(person=1).ablative().to_json())
        
##### Output
    Elif'in öküzü.
    Öykü'nün
    Cem'e
    Nil'e
    ALİ'YE
    Taylan'dan
    Amasya'yı
    ağacın
    eriği
    Erik'i
    kavanozum
    kavanozun
    kavanozu
    halterimiz
    halteriniz
    halterleri
    Kenyaları
    {'result': 'çantalarımdan', 'stem': 'çanta', 'history': [{'action': 'plural', 'current': 'çantalar', 'kwargs': {}}, {'action': 'possessive', 'current': 'çantalarım', 'kwargs': {'person': 1}}, {'action': 'ablative', 'current': 'çantalarımdan', 'kwargs': {}}]}


### Verbs
    Parameters: person (1, 2, 3), negative (boolean), question (boolean), plural (boolean)

    Turkish('git').infinitive()
    > gitmek 
    
    Turkish('git').infinitive(negative=True)
    > gitmemek

    Turkish('al').future(person=2, plural=True)  # Second person plural
    > alacaksınız

    Turkish('al').present_simple(person=1)  # First person single
    > alırım
    
    Turkish('al').past(person=3, plural=True)
    > aldılar
    
    Turkish('al').command(person=3, plural=True)
    > alsınlar
    
    Turkish('ver').present_continuous(person=1)
    > veriyorum
    
    Turkish('ver').present_continuous_alternative(person=1)
    > vermekteyim
    
    Turkish('ver').must(person=2)
    > vermelisin
    
    Turkish('anlat').wish_condition(person=3)
    > anlatsa
    
    Turkish('sakla').wish(person=3, plural=True)
    > saklayalar
    
    Turkish('anla').learned_past(person=3, question=True)
    > anlamış mı
    
    Turkish('sat').past_learned_past(person=2, negative=True)
    > satmamıştın
    
    Turkish('kork').learned_past_learned_past(person=3)
    > korkmuşmuş
    
    Turkish('oyna').learned_past_future(person=2, negative=True)
    > oynamayacakmışsın
    
    Turkish('oyna').past_future(person=2, negative=True, question=True)
    > oynamayacak mıydın
    
    Turkish('oyna').past_past(person=2, negative=True)
    > oynamadıydın
    
    Turkish('gül').past_condition(person=2)
    > güldüysen

## Turkish Grammar
 * Turkish is a highly agglutinative language, i.e., Turkish words have many 
   grammatical suffixes or endings that determine meaning. Turkish vowels 
   undergo vowel harmony. When a suffix is attached to a stem, the vowel in 
   the suffix agrees in frontness or backness and in roundedness with the last 
   vowel in the stem. Turkish has no gender.

 * Turkish Language is a language with strict rules with an only couple of 
   exceptions which makes it very easy for simulating by coding.

 * [More Info](http://en.wikipedia.org/wiki/Turkish_grammar)

## Other Languages 
      C# Version
      https://github.com/yasinkuyu/Turkish.cs
      
      PHP Version
      https://github.com/yasinkuyu/Turkish.php
      
      JavaScript Version
      https://github.com/yasinkuyu/Turkish.js


## Special thanks for C#, PHP and JavaScript versions
      Yasin Kuyu
      https://github.com/yasinkuyu/