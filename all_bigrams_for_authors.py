#-*- coding: utf-8 -*-
import codecs
import string

all_bigrams = set()
common_prefix = 'dane_pozytywistyczne2/korpus_'
common_suffix='.txt.bigrams'

authors = ['kraszewskiego', 'orzeszkowej', 'prusa', 'sienkiewicza']

for author in authors:
    print 'BEGIN: ' + author
    for line in open(common_prefix+author+common_suffix, 'r'):
        line = unicode(line.replace('\n', ''), 'utf-8')
        all_bigrams.add(line)
    print 'END: ' + author

save_file = codecs.open(common_prefix+'all_bigrams', 'w', 'utf-8')
for bigram in all_bigrams:
    save_file.write(bigram+'\n')
