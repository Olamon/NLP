#-*- coding: utf-8 -*-
import codecs
import collections
import numpy
import sys

bigrams = dict([])
all_bigrams = []
trigrams = dict([])
bigrams_cnt = dict([])
trigrams_cnt = dict([])
all_bigrams_cnt = []
all_bigram_cnt = 0.0
alphabet = u"aąbcćdeęfghijklłmnńoóprsśtuvwxyzźż,"

def is_not_word(word):
    global alphabet
    word = unicode(word, 'utf-8')
    return not reduce(lambda x,y: x and (y in alphabet), word, True)

def init_grams(bigram_k, trigram_k):
    global bigrams
    global trigrams
    global bigrams_cnt
    global trigrams_cnt
    global all_bigrams
    global all_bigrams_cnt
    global all_bigram_cnt
    for line in open('2grams', 'r'):
        cnt,w1,w2 = line.strip().split(' ')
        if int(cnt) < int(bigram_k) or is_not_word(w1) or is_not_word(w2):
            continue
        if w1 not in bigrams:
            bigrams[w1] = []
            bigrams_cnt[w1] = []
        bigrams[w1].append(w2)
        all_bigrams.append(w1 + ' ' + w2)
        bigrams_cnt[w1].append(float(cnt))
        all_bigram_cnt += float(cnt)
        all_bigrams_cnt.append(float(cnt))
    for line in open('3grams', 'r'):
        cnt,w1,w2,w3 = line.strip().split(' ')
        if int(cnt) < int(trigram_k) or is_not_word(w1) or is_not_word(w2) or is_not_word(w3):
                continue
        key = w1 + ' ' + w2
        if key not in trigrams:
            trigrams[key] = []
            trigrams_cnt[key] = []
        trigrams[key].append(w3)
        trigrams_cnt[key].append(float(cnt))
 
def get_bigram_seed():
    global all_bigrams
    global all_bigrams_cnt
    return numpy.random.choice(all_bigrams, p=[x/all_bigram_cnt for x in all_bigrams_cnt])

def generate_text():
    global trigrams
    global bigrams
    global trigrams_cnt
    global bigrams_cnt
    phrase = get_bigram_seed()
    sys.stdout.write(phrase) 
    next_word_possible = trigrams.get(phrase, [])
    next_word_possible_cnt = trigrams_cnt.get(phrase, [])
    if not next_word_possible:
        next_word_possible = bigrams.get(phrase.split(' ')[1], [])
        next_word_possible_cnt = bigrams_cnt.get(phrase.split(' ')[1], [])
    while next_word_possible:
        next_word = numpy.random.choice(next_word_possible, p=[x/sum(next_word_possible_cnt) for x in next_word_possible_cnt])
        sys.stdout.write(' ' + next_word)
        phrase = phrase.split(' ')[1] + ' ' + next_word
        next_word_possible = trigrams.get(phrase, [])
        next_word_possible_cnt = trigrams_cnt.get(phrase, [])
        if not next_word_possible:
            next_word_possible = bigrams.get(next_word, [])
            next_word_possible_cnt = bigrams_cnt.get(next_word, [])
def main():
    init_grams(50, 50)
    input_text = raw_input('More? If so type \'Y\'.')
    while input_text == 'Y':
            generate_text()
            input_text = raw_input('More? If so type \'Y\'.')

if __name__ == "__main__":
    main()
