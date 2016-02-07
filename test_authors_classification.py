#-*- coding: utf-8 -*-
import codecs
import classify_authors as test_class

test_prefix = 'dane_pozytywistyczne2/testy1/'

authors = ['kraszewski', 'orzeszkowej', 'prusa', 'sienkiewicza']

for author in authors:
    print 'REAL AUTHOR: ' + author
    scores = {\
'kraszewski':0, \
'orzeszkowa':0, \
'prus':0, \
'sienkiewicz':0}
    for test_file in open(test_prefix+author+'_files', 'r'):
        test_file = test_file.strip()
        recognized_author = test_class.classify(test_prefix + author+'/'+test_file)
        scores[recognized_author] +=1
    for name in scores:
        print name +': '+str(scores[name])   
