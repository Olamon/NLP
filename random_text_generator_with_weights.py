#-*- coding: utf-8 -*-
import codecs
import collections
import dbm
import numpy
import sys

class RandomTextGeneratorWithWeights:
    def __init__(self, bigram_k, trigram_k):
        self.mapping = dict([])
        self.bigram_cnt = 0.0
        for line in open('2grams', 'r'):
            cnt,w1,w2 = line.strip().split(' ')
            if int(cnt) < int(bigram_k):
                continue
            value = self.mapping.get('#' + w1, '') + ('#' + cnt + '^' + w2)
            self.mapping['#' + w1] = value
            self.bigram_cnt += float(cnt)
        for line in open('3grams', 'r'):
            cnt,w1,w2,w3 = line.strip().split(' ')
            if int(cnt) < int(trigram_k)
                continue
            value = self.mapping.get(w1 + ' ' + w2, '') + ('#' + cnt + '^' + w3)
            self.mapping[w1 + ' ' + w2] = value
 
    def get_bigram_seed(self):
        words = []
        counts = []
        for w1 in self.mapping:
            if w1[0] == '#':
            for cnt_and_w2 in self.mapping[w1].split('#'):
                if '^' in cnt_and_w2:
                    words.append(cnt_and_w2.split('^')[1])
                    counts.append(float(cnt_and_w2.split('^')[0]/self.bigram_cnt))
        return numpy.random.choice(words, p=counts)

    def generate_text(self):
        phrase = self.get_bigram_seed()
        print phrase 
        next_word_possible = self.mapping.get(phrase, '').split('#')[1:]
        if not next_word_possible:
            next_word_possible = self.mapping.get('#' + phrase.split(' ')[1]).split('#')[1:]
        while next_word_possible:
            words_and_counts = [list(t) for t in zip(*[(x.split('^')[-1], float(x.split('^')[0])) for x in next_word_possible])]
            next_word = numpy.random.choice(words_and_counts[0], p=[x/sum(words_and_counts[1]) for x in words_and_counts[1]])
            print next_word
            phrase = phrase.split(' ')[1] + ' ' + next_word
            next_word_possible = self.mapping.get(phrase, '').split('#')[1:]
            if not next_word_possible:
                next_word_possible = self.mapping.get('#' + phrase.split(' ')[1]).split('#')[1:]

def main():
    random_text_generator = RandomTextGeneratorWithWeights(25, 25)
    input_text = raw_input('More? If so type \'Y\'.')
    while input_text == 'Y':
            random_text_generator.generate_text()
            input_text = raw_input('More? If so type \'Y\'.')

if __name__ == "__main__":
    main()
