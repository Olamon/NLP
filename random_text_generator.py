#-*- coding: utf-8 -*-
import codecs
import collections
import dbm
import random
import sys
    
class RandomTextGenerator:
  
  def __init__(self, bigram_k, trigram_k):
    self.mapping = dict([])
    #key_set_const = '_key_set_'
    for line in open('2grams', 'r'):
      cnt,w1,w2 = line.strip().split(' ')
      if int(cnt) < int(bigram_k):
          continue
      value = self.mapping.get('#' + w1, '') + '#' + w2
      #key_set = self.mapping.get(key_set_const, '') + '#' + w1
      self.mapping['#' + w1] = value
      #self.mapping[key_set_const] = key_set
    for line in open('3grams', 'r'):
      cnt,w1,w2,w3 = line.strip().split(' ')
      if int(cnt) < int(trigram_k):
          continue
      key = w1 + ' ' + w2
      value = self.mapping.get(key, '') + '#' + w3
      #key_set = self.mapping.get(key_set_const, '') + '#' + key
      self.mapping[key] = value
      #self.mapping[key_set_const] = key_set
	
  def possible_next_for(self, phrase):
    next_words = (self.mapping.get(phrase, '#')).split('#')[1:]
    if not next_words:
        return None
    index = random.randint(0, len(next_words) -1)
    return next_words[index]
  
  def get_seed(self):
    possible_keys = [x for x in self.mapping if x[0] != '#']
    index = random.randint(0, len(possible_keys) -1)
    return possible_keys[index]
  
  def generate_text(self):
    phrase = self.get_seed()
    print phrase
    w1,w2 = phrase.split(' ')
    next_word = self.possible_next_for(phrase)
    while next_word:
      phrase = w2 + next_word
      print ' ' + next_word
      w2 = next_word
      next_word = self.possible_next_for(phrase)
      if not next_word:
          next_word = self.possible_next_for('#' + w2)
          
def main():
    random_text_generator = RandomTextGenerator(100, 50)
    input_text = raw_input('More? If so type \'Y\'.')
    while input_text == 'Y':
        random_text_generator.generate_text()
        input_text = raw_input('More? If so type \'Y\'.')

if __name__ == "__main__":
  main()
