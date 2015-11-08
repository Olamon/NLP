#-*- coding: utf-8 -*-
import codecs
import collections
import dbm
import random
import sys

bigrams = dict([])
trigrams = dict([])
alphabet = u"aąbcćdeęfghijklłmnńoóprsśtuvwxyzźż,"

def is_not_word(word):
    global alphabet
    word = unicode(word, 'utf-8')
    return not reduce(lambda x,y: x and (y in alphabet), word, True)

def init_grams(bigram_k, trigram_k):
    global bigrams
    global trigrams
    for line in open('2grams', 'r'):
      cnt,w1,w2 = line.strip().split(' ')
      if int(cnt) < int(bigram_k) or is_not_word(w1) or is_not_word(w2):
          continue
      if not w1 in bigrams:
          bigrams[w1] = []
      bigrams[w1].append(w2)
    for line in open('3grams', 'r'):
      cnt,w1,w2,w3 = line.strip().split(' ')
      if int(cnt) < int(trigram_k) or is_not_word(w1) or is_not_word(w2) or is_not_word(w3):
          continue
      key = w1 + ' ' + w2
      if not key in trigrams:
          trigrams[key] = []
      trigrams[key].append(w3)
	
def possible_next_for(phrase):
    global trigrams
    global bigrams
    if phrase[0] == '#':
        next_words = bigrams.get(phrase[1:], [])
    else:
        next_words = trigrams.get(phrase, [])
    if not next_words:
        return None
    index = random.randint(0, len(next_words) -1)
    return next_words[index]
  
def get_seed():
    global trigrams
    possible_keys = [x for x in trigrams]
    index = random.randint(0, len(possible_keys) -1)
    return possible_keys[index]
  
def generate_text():
    phrase = get_seed()
    sys.stdout.write(phrase)
    w1,w2 = phrase.split(' ')
    next_word = possible_next_for(phrase)
    while next_word:
      phrase = w2 + ' ' + next_word
      sys.stdout.write(' ' + next_word)
      w2 = next_word
      next_word = possible_next_for(phrase)
      if not next_word:
          next_word = possible_next_for('#' + w2)
          
def main():
    init_grams(50, 50)
    generate_text()
    input_text = raw_input('Type \'Y\' to see more')
    while input_text == 'Y':
        generate_text()
        input_text = raw_input('More? If so type \'Y\'.')

if __name__ == "__main__":
  main()
