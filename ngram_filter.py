#-*- coding: utf-8 -*-
import codecs
import collections
import itertools

mapping = dict([])
text_words = []
text_suffixes = []
alpha = 0.1

def init_text_tokens(text):
    global text_words
    global text_suffixes
    text_words = [x for x in text.split(' ') if x[0] != '#']
    text_suffixes = [x for x in text.split(' ') if x[0] == '#']

def is_word(word):
    return word in text_words

def possible_suffixes(word):
    global text_words
    global text_suffixes
    result = []
    for i in range(0, len(text_suffixes)):
        if word[len(word) - len(text_suffixes[i]) + 1:] == text_suffixes[i][1:]:
            result.append(i)
    for i in range(0, len(text_words)):
        if word == text_words[i]:
            result.append(i+len(text_suffixes))
    return result

def filter_ngrams(text):
    global mapping
    init_text_tokens(text)
    for line in open('2grams'):
        cnt,w1,w2 = line.strip().split(' ')
        w1_possible = possible_suffixes(w1)
        w2_possible = possible_suffixes(w2)
        for elem1 in w1_possible:
            for elem2 in w2_possible:
                if elem1 == elem2:
                    continue
                if elem1 >= len(text_suffixes):
                    w1 = text_words[elem1 - len(text_suffixes)]
                else:
                    w1 = text_suffixes[elem1]
                if elem2 >= len(text_suffixes):
                    w2 = text_words[elem2 - len(text_suffixes)]
                else:
                    w2 = text_suffixes[elem2]
                key = w1 + ' ' + w2
                value = mapping.get(key, 0.0) + float(cnt)
                mapping[key] = value
    for line in open('3grams'):
        cnt,w1,w2,w3 = line.strip().split(' ')
        w1_possible = possible_suffixes(w1)
        w2_possible = possible_suffixes(w2)
        w3_possible = possible_suffixes(w3)
        for elem1 in w1_possible:
            for elem2 in w2_possible:
                for elem3 in w3_possible:
                    if elem1 == elem2 or elem1 == elem3 or elem2 == elem3:
                        continue
                    if elem1 >= len(text_suffixes):
                        w1 = text_words[elem1 - len(text_suffixes)]
                    else:
                        w1 = text_suffixes[elem1]
                    if elem2 >= len(text_suffixes):
                        w2 = text_words[elem2 - len(text_suffixes)]
                    else:
                        w2 = text_suffixes[elem2]
                    if elem3 >= len(text_suffixes):
                        w3 = text_words[elem3 - len(text_suffixes)]
                    else:
                        w3 = text_suffixes[elem3]
                    key = w1 + ' ' + w2 + ' ' + w3
                    value = mapping.get(key, 0) + float(cnt)
                    mapping[key] = value

def score_permutation(perm):
    global mapping
    score = 0.0
    for i in range(0, len(perm) - 2):
        all_score = 1.0
        elements = [perm[i], perm[i+1], perm[i+2]]
        for all_perm in itertools.permutations(elements):
            all_score += mapping.get(all_perm[0] + ' ' + all_perm[1] + ' ' + all_perm[2], 0.0)
        score += (1-alpha)*mapping.get(elements[0] + ' ' + elements[1] + ' ' + elements[2], 0.0)/all_score
    for i in range(0, len(perm) - 1):
        all_score = 1.0
        elements = [perm[i], perm[i+1]]
        for all_perm in itertools.permutations(elements):
            all_score += mapping.get(all_perm[0] + ' ' + all_perm[1], 0.0)
        score += alpha*mapping.get(elements[0] + ' ' + elements[1], 0.0)/all_score
    return score

def main():
    global mapping
    input_text = 'judyta #ła wczoraj #anowi czekoladki' 
    filter_ngrams(input_text)
    perm = input_text.split(' ')
    perm_and_score = [(score_permutation(perm), reduce(lambda x,y: x + ' ' + y, perm)) for perm in itertools.permutations(perm)]
    perm_and_score = sorted(perm_and_score)
    out_file = codecs.open('judyta', 'w', 'utf-8')
    for s,p in perm_and_score:
        p = unicode(p, 'utf-8')
        out_file.write(str(s) +  ' ' + p + '\n')
    out_file.close()
    mapping = dict([])
    input_text = '#eńka #ła dwa #ate #ołki' 
    filter_ngrams(input_text)
    perm = input_text.split(' ')
    perm_and_score = [(score_permutation(perm), reduce(lambda x,y: x + ' ' + y, perm)) for perm in itertools.permutations(perm)]
    perm_and_score = sorted(perm_and_score)
    out_file = codecs.open('babulenka', 'w', 'utf-8')
    for s,p in perm_and_score:
        p = unicode(p, 'utf-8')
        out_file.write(str(s) +  ' ' + p + '\n')
    out_file.close()

if __name__ == "__main__":
    main()
