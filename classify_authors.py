#-*- coding: utf-8 -*-
import codecs
import sys
import string
import math

def classify(test_file):
    bigram_pref = 'dane_pozytywistyczne2/korpus_'

    authors_to_bigrams = { \
    'kraszewski':(bigram_pref+'kraszewskiego.txt.bigrams'), \
    'orzeszkowa':(bigram_pref+'orzeszkowej.txt.bigrams'), \
    'prus':(bigram_pref+'prusa.txt.bigrams'), \
    'sienkiewicz':(bigram_pref+'sienkiewicza.txt.bigrams')}

    authors_to_score = dict({})

    for author in authors_to_bigrams:
        bigram_to_prob = dict({})
        for line in open(authors_to_bigrams[author], 'r'):
            tokens = line.split()
            if not tokens:
                continue
            prob = tokens[0]
            bigram = string.join(tokens[1:], ' ')
            bigram = unicode(bigram, 'utf-8')
            bigram_to_prob[bigram] = math.log(float(prob))
        last_word = ''
        score = 0
        for line in open(test_file, 'r'):
            words = line.split(' ')
            for word in words:
                word = unicode(word, 'utf-8')
                key = last_word + ' ' + word
                last_word = word
                if key in bigram_to_prob:
                    score+=bigram_to_prob[key]
        authors_to_score[author] = score

    author, _ = max(authors_to_score.iteritems(), key=lambda x:x[1])
    return author
