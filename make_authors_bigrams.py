#-*- coding: utf-8 -*-
import codecs
import sys

bigrams_count = dict({})
last_word = ''
bigrams_all_count=0

for line in open('dane_pozytywistyczne2/allowed_bigrams'):
    line = unicode(line, 'utf-8').replace('\n', '')
    bigrams_count[line] = 1
    bigrams_all_count +=1

for line in open(sys.argv[1], 'r'):
    line = unicode(line, 'utf-8')
    words = line.split()
    for word in words:
        key = last_word + ' ' + word
        last_word = word
        if key in bigrams_count:
            bigrams_count[key] +=1
            bigrams_all_count +=1

act_count = max(bigrams_count.values())
save_file = codecs.open(sys.argv[1]+'.bigrams', 'w', 'utf-8')
 
counter = 1
new_bigrams_count = {}

#for word in sorted(bigrams_count, key=bigrams_count.get, reverse=True):
#    if not ((act_count >= 100 and act_count <= 2 * bigrams_count[word]) or (act_count<100 and act_count == bigrams_count[word])):
#        counter+=1
#        act_count = bigrams_count[word]
#    new_bigrams_count[word] = counter

#for word in sorted(new_bigrams_count):
#    save_file.write(word + '#'+str(new_bigrams_count[word])+'\n')

for word in bigrams_count:
    save_file.write(str(float(bigrams_count[word])/float(bigrams_all_count)) + ' ' + word +'\n')

save_file.close()
