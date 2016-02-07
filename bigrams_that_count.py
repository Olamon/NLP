#-*- coding: utf-8 -*-
import codecs

bigrams_to_rank_list = {}

authors = ['kraszewskiego', 'orzeszkowej', 'sienkiewicza', 'prusa']
scale = []

for author in authors:
    max_for_author = 0
    for line in open('dane_pozytywistyczne2/korpus_'+author+'.txt.ordered'):
        bigram,cnt = line.split('#')
        bigram = unicode(bigram, 'utf-8')
        if not bigram in bigrams_to_rank_list:
            bigrams_to_rank_list[bigram] = []
        if max_for_author < int(cnt):
            max_for_author = int(cnt)
        bigrams_to_rank_list[bigram].append(int(cnt))
    scale.append(max_for_author)

save_file = codecs.open('dane_pozytywistyczne2/allowed_bigrams', 'w', 'utf-8')
for bigram in bigrams_to_rank_list:
    scores = [bigrams_to_rank_list[bigram][i]/float(scale[i]) for i in range(0,4)] 
    if max(scores) == 1 or min(scores)/max(scores) <= 0.5:
        save_file.write(bigram + '\n')
save_file.close()
