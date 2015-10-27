#-*- coding: utf-8 -*-
import codecs
import dbm
import numpy
import sys

class RandomTextGeneratorWithWeights:
    def __init__(self):
        self.mapping = dbm.open('ngrams_mapping_weighted', 'r')

    def get_bigram_seed(self):
        all_count = float(self.mapping.get('_bigram_cnt_', ''))
        list_with_keys = self.mapping.get('_key_set_', '').split('#')
        words_and_counts = [list(t) for t in zip(*[(x.split('^')[1], int(x.split('^')[0])) for x in list_with_keys if '^' in x])]
        return numpy.random.choice(words_and_counts[0], p=[x/all_count for x in words_and_counts[1]])

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
    random_text_generator = RandomTextGeneratorWithWeights()
    input_text = raw_input('More? If so type \'Y\'.')
    while input_text == 'Y':
            random_text_generator.generate_text()
            input_text = raw_input('More? If so type \'Y\'.')

if __name__ == "__main__":
    main()
