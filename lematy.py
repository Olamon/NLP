#-*- coding: utf-8 -*-
import collections

endings = dict([])
good_lemmas = dict([])
cnt_for_unigrams = dict([])
bag_with_words = set([])
interp = u"–:;.,?!*()'\"-“^"

def delete_interp(word):
    global interp
    index = word.find(':')
    if not index == -1:
        word = word[:index]
    word = ''.join(c for c in word if not c in interp)
    return word

def read_morf_dict():
    global good_lemmas
    global cnt_for_unigrams
    global endings
    global bag_with_words
    for line in open('morfeuszTagsAndBasesForNKJP.txt', 'r'):
        word1,word2 = line.strip().split(' ')[0:2]
        word1 = delete_interp(unicode(word1, 'utf-8'))
        word2 = delete_interp(unicode(word2, 'utf-8'))
        if not word1 or not word2:
            continue
        if not word1 in good_lemmas:
            good_lemmas[word1] = []
        good_lemmas[word1].append(word2)
        bag_with_words.add(word1)
        cnt_for_unigrams[word1] = 1
        bag_with_words.add(word2)
        cnt_for_unigrams[word2] = 1
    for line in open('1grams', 'r'):
        cnt,word = line.strip().split(' ')
        word = unicode(word, 'utf-8')
        if word in bag_with_words:
            cnt_for_unigrams[word] += int(cnt)
    for key in good_lemmas:
        for value in good_lemmas[key]:
            index = max(min(len(key), len(value))-5, 1)
            contribution = cnt_for_unigrams[key]/float(len(good_lemmas[key]))
            while index < min(len(key), len(value)) - 1:
                new_key = key[index:]
                new_value = value[index:]
                if not new_key in endings:
                    endings[new_key] = dict([])
                    endings[new_key][new_value] = contribution
                else:
                    if not new_value in endings[new_key]:
                        endings[new_key][new_value] = contribution
                    else:
                        endings[new_key][new_value] += contribution
                index += 1
    for key in endings:
        endings[key] = [(endings[key][value], value) for value in endings[key]]

def get_lemmas(word):
    global good_lemmas
    global endings
    global cnt_for_unigrams
    if word in good_lemmas:
        sum_all = float(sum([cnt_for_unigrams[w] for w in good_lemmas[word]]))
        return sorted([(cnt_for_unigrams[w]/sum_all, w) for w in good_lemmas[word]])
    else:
        endings_for_w = []
        for i in range(0, len(word) - 1):
            if word[i:] in endings:
                sum_all = float(sum([x[0] for x in endings[word[i:]]]))
                endings_for_w += [(cnt/sum_all, word[0:i] + w) for cnt,w in endings[word[i:]]]
        sum_all = sum([x[0] for x in endings_for_w if x[0] >= 0.01])
        endings_result = [(x[0]/sum_all, x[1]) for x in endings_for_w if x[0] >= 0.01]
        return sorted(endings_result)

def main():
    read_morf_dict()
    sentence = raw_input('Type: ')
    while sentence != 'no':
        words = sentence.split(' ')
        for word in words:
            word = unicode(word, 'utf-8')
            lemmas = get_lemmas(word)
            lemmas_dict = dict([])
            for prob,lemma in lemmas:
                if not lemma in lemmas_dict:
                    lemmas_dict[lemma] = 0
                lemmas_dict[lemma] += prob
            print word + ' - '
            for lemma in sorted(lemmas_dict, key=lemmas_dict.__getitem__):
                print str(lemmas_dict[lemma]) + ' ' + lemma
            print '\n'
        sentence = raw_input('Type: ')

if __name__ == "__main__":
    main()
