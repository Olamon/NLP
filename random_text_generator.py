#-*- coding: utf-8 -*-
import codecs
import collections
import dbm
import random
import sys
    
class RandomTextGenerator:
  
  def __init__(self):
    self.mapping = dbm.open('ngrams_mapping_uniform', 'r')
	
  def possible_next_for(self, phrase):
      next_words = (self.mapping.get(phrase, '#')).split('#')[1:]
      if not next_words:
          return None
      index = random.randint(0, len(next_words) -1)
      return next_words[index]
  
  def generate_text(self):
    word = self.possible_next_for('_key_set_')
    result = [word]
    print word
    next_phrase = self.possible_next_for(result[-1])
    while next_phrase:
      print ' ' + next_phrase
      result = [result[-1], next_phrase]
      next_phrase = self.possible_next_for(result[0] + ' ' + result[1])
      if not next_phrase:
          next_phrase = self.possible_next_for(result[1])

  def __del__(self):
    self.mapping.close()

def main():
    random_text_generator = RandomTextGenerator()
    input_text = raw_input('More? If so type \'Y\'.')
    while input_text == 'Y':
        random_text_generator.generate_text()
        input_text = raw_input('More? If so type \'Y\'.')

if __name__ == "__main__":
  main()
