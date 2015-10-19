#-*- coding: utf-8 -*-
import codecs
import collections
import random
import sys
    
class RandomTextGenerator:
  
  def __init__(self, bigram_file, trigram_file, bigram_K, trigram_K):
    self.next_phrases = dict([])
    bigram_data = codecs.open(bigram_file, 'r', 'utf-8')
    for line in bigram_data:
      words = line.strip().split(' ')
      count = int(words[0])
      if count > int(bigram_K):
        words = words[1:]
        if not words[0] in self.next_phrases.keys():
          self.next_phrases[words[0]] = []
        self.next_phrases[words[0]].append([words[1]])
    trigram_data = codecs.open(trigram_file, 'r', 'utf-8')
    for line in trigram_data:
      words = line.strip().split(' ')
      count = int(words[0])
      if count > int(trigram_K):
        words = words[1:]
        if not words[0]  in self.next_phrases.keys():
            self.next_phrases[words[0]] = []
        self.next_phrases[words[0]].append([words[1], words[2]])
	
  def possible_next_for(self, word):
    if not word in self.next_phrases.keys():
      return []
    else:
      index = random.randint(0, self.next_phrases[word].size()-1)
      return self.next_phrases[word][index]
  
  def genrate_text(self, word):
    result = [word]
    next_phrase = possible_next_for(result[-1])
    while next_phrase:
      result += next_phrase
    return ' '.join(result)

def main():
    args = sys.argv[1:]
    random_text_generator = RandomTextGenerator(args[0], args[1], args[2], args[3])
    word = input('Word:')
    while word != 'q':
        print random_text_generator.generate_text(word)
        word = input('Word:')

if __name__ == "__main__":
  main()
