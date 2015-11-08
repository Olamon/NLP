#-*- coding: utf-8 -*-
import codecs

alphabet = u"aąbcćdeęfghijklłmnńoóprsśtuvwxyzźż"

#filter vocabulary and 1/2-grams for simple_spell
def main():
  global alphabet
  vocabulary = []
  out_vocabulary = codecs.open('vocabulary_filtered', 'w', 'utf-8')
  for line in open('slownik_do_literowek.txt', 'r'):
    word = unicode(line.strip(), 'utf-8')
    if reduce(lambda x,y: x and (y in alphabet), word, True):
      out_vocabulary.write(word + '\n')
      vocabulary.append(word)
  out_vocabulary.close()
  out_file = codecs.open('1grams_filtered', 'w', 'utf-8')
  for line in open('1grams'):
    cnt,w1 = line.strip().split(' ')
    w1 = unicode(w1, 'utf-8')
    if int(cnt) < 2:
        continue
    if w1 in vocabulary:
      out_file.write(cnt + ' ' + w1 + '\n')
  out_file.close()
  out_file = codecs.open('2grams_filtered', 'w', 'utf-8')
  for line in open('2grams'):
    cnt,w1,w2 = line.strip().split()
    w1 = unicode(w1, 'utf-8')
    w2 = unicode(w2, 'utf-8')
    if int(cnt) < 2:
        continue
    if w1 in vocabulary and w2 in vocabulary:
      out_file.write(cnt + ' ' + w1 + ' ' + w2 + '\n')
  out_file.close()
 
if __name__ == "__main__":
  main()
