#-*- coding: utf-8 -*-
import collections
import codecs
import editdist
import random
import string

vocabulary = set([])
unigrams = []
unigrams_cnt = []
bigrams = dict([])
bigrams_cnt = dict([])
alpha = 0.1

polish_letters = u"ąćęłńóśźż"
unpolished_letters = u"acelnoszz"
unpolished_letters_edit = u"ACELNOSZX"
alphabet = u"aąbcćdeęfghijklłmnńoóprsśtuvwxyzźż"

def init_vocabulary():
    global vocabulary
    global unigrams
    global unigrams_cnt
    global bigrams
    global bigrams_cnt
    global alphabet
    for line in open('vocabulary_filtered', 'r'):
        word = unicode(line.strip(), 'utf-8')
        vocabulary.add(word)
    for line in open('1grams_filtered'):
        cnt,w1 = line.strip().split(' ')
        w1 = unicode(w1, 'utf-8')
        unigrams.append(w1)
        unigrams_cnt.append(int(cnt))
    for line in open('2grams_filtered'):
        cnt,w1,w2 = line.strip().split()
        w1 = unicode(w1, 'utf-8')
        w2 = unicode(w2, 'utf-8')
        if w1 not in bigrams:
            bigrams[w1] = []
            bigrams_cnt[w1] = []
        bigrams[w1].append(w2)
        bigrams_cnt[w1].append(int(cnt))

def erase_polish_letters(word, unpolished_letters):
    global polish_letters
    result = ''
    for i in range(0, len(word)):
        index = polish_letters.find(word[i])
        if index >= 0:
            result += unpolished_letters[index]
        else:
            result += word[i]
    return result

def words_polish_letters_change(prefix, word):
    global vocabulary
    global unpolished_letters
    global polish_letters
    result = set([])
    result.add(prefix+word)
    if not len(word):
        return result
    result =  result | words_polish_letters_change(prefix + word[0], word[1:])
    index = unpolished_letters.find(word[0])
    if index > -1:
        result = result | words_polish_letters_change(prefix + polish_letters[index], word[1:])
        if word[0] == 'z':
            result = result | words_polish_letters_change(prefix + polish_letters[index+1], word[1:])
    return result

def generatate_close_word(prev_word, word, origin_word):
    global vocabulary
    global alpha
    global alphabet
    global unigrams
    global unigrams_cnt
    global bigrams
    global bigrams_cnt
    result = ['']
    result_score = [-1]
    prev_word_bigrams = []
    prev_word_bigrams_cnt = []
    if prev_word:
        prev_word_bigrams = bigrams.get(prev_word, [])
        prev_word_bigrams_cnt = bigrams_cnt.get(prev_word, [])
    def acctualize_score(w, multi=1.0):
        score = alpha/sum(unigrams_cnt)
        if w in unigrams:
            ind_uni = unigrams.index(w)
            score += alpha * (unigrams_cnt[ind_uni]-1)/sum(unigrams_cnt)
        if w in prev_word_bigrams:
            ind_bi = prev_word_bigrams.index(w)
            score += 2*(1-alpha)*prev_word_bigrams_cnt[ind_bi]/sum(prev_word_bigrams_cnt)
        score*=multi
        if score > result_score[0]:
            result[0] = w
            result_score[0] = score
    if word in vocabulary:
        acctualize_score(word, 2.0)
    for i in range(0, len(word) + 1):
        for letter in alphabet:
            new_word = word[:i] + letter + word[i:]
            if new_word in vocabulary:
                acctualize_score(new_word)
            if i != len(word):
                new_word = word[:i] + letter + word[(i+1):]
                if new_word in vocabulary:
                    acctualize_score(new_word)
        if i !=  len(word):
            new_word = word[0:i] + word[(i+1):]
            if new_word in vocabulary:
                if not i in [0, len(word)-1]:
                    acctualize_score(new_word, 1.1)
                else:
                    acctualize_score(new_word, 1.3)
            if i != len(word) -1:
                new_word = word[0:i] + word[i+1] + word[i] + word[i+2:]
                if new_word in vocabulary:
                    acctualize_score(new_word)
    return (result_score[0], result[0])

def get_good_variation(prev_word, word):
    global vocabulary
    global alpha
    global alphabet
    global bigrams
    global bigrams_cnt
    global unigrams
    global unigrams_cnt
    global unpolished_letters
    prev_word_bigrams = []
    prev_word_bigrams_cnt = []
    if prev_word:
        prev_word_bigrams = bigrams.get(prev_word, [])
        prev_word_bigrams_cnt = bigrams_cnt.get(prev_word, [])
    possible_list = words_polish_letters_change('', erase_polish_letters(word, unpolished_letters))
    result = ''
    result_score = -1
    for w in [x for x in possible_list if x in vocabulary]:
        score = alpha/sum(unigrams_cnt)
        if w in unigrams:
            ind_uni = unigrams.index(w)
            score += alpha * unigrams_cnt[ind_uni]/sum(unigrams_cnt)
        if w in prev_word_bigrams:
            ind_bi = prev_word_bigrams.index(w)
            score += 2*(1-alpha)*prev_word_bigrams_cnt[ind_bi]/sum(prev_word_bigrams_cnt)
        if score > result_score:
            result = w
            result_score = score
    return result

def get_all_possible_corrections(prev_word, word):
    result = []
    polish_letters_variation = words_polish_letters_change('', erase_polish_letters(word, unpolished_letters))
    for variation in polish_letters_variation:
        result.append(generatate_close_word(prev_word, variation, erase_polish_letters(word, unpolished_letters_edit)))
    return result

def correct_word(prev_word, word):
    global vocabulary
    w = get_good_variation(prev_word, word)
    if w:
        return w
    if len(word) <= 2:
        possible_variation = get_good_variation('', word)
        return possible_variation
    else:
        corrections = get_all_possible_corrections(prev_word, word)
        if not corrections:
            return word
        score,correction = max(corrections)
        return correction

def main():
    init_vocabulary()
    out_file = codecs.open('corrected1a', 'w', 'utf-8')
    for line in open('zepsute1a.txt', 'r'):
        words = line.split()
        out_line = ''
        prev_word = ''
        for word in words:
            word = unicode(word, 'utf-8')
            word = correct_word(prev_word, word)
            out_line+= (word + ' ')
            prev_word = word
        out_file.write(out_line + '\n')
        print out_line
    out_file.close()
    
if __name__ == "__main__":
  main()
