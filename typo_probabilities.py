#-*- coding: utf-8 -*-
import collections
import codecs
import editdist

polish_letters = u"ąćęłńóśźż"
unpolished_letters = u"acelnoszz"
unpolished_letters_edit = u"ACELNOSZX"
alphabet = u"aąbcćdeęfghijklłmnńoóprsśtuvwxyzźż"

vocabulary = set([])
unigrams = []
unigrams_cnt = dict([])
Probabilities = dict([('ins', 0), ('del', 0), ('trans', 0), ('repl', 0), ('alt', 0), ('no_alt', 0)])
Probabilities_repl = dict([])
Probabilities_trans = dict([])
Proabilities_trans_rev = dict([])

def is_word(word):
    global alphabet
    return reduce(lambda x,y: x and y in alphabet, word, True)

def find_edit(word, cnt, treshold):
    global vocabulary
    global unigrams
    global unigrams_cnt
    global polish_letters
    global unpolished_letters
    global alphabet
    global Probabilities
    global Probabilities_repl
    global Probabilities_trans
    global Proabilities_trans_rev
    max_cnt = -1
    correction = ''
    type_of_typo = ''
    c1 = ''
    c2 = ''
    for i in range(0, len(word) + 1):
        for letter in alphabet:
            new_word = word[:i] + letter + word[i:]
            if new_word in unigrams:
                if unigrams_cnt[new_word] > max_cnt:
                    correction = new_word
                    max_cnt = unigrams_cnt[new_word]
                    type_of_typo = 'ins'    
            if i != len(word):
                new_word = word[:i] + letter + word[(i+1):]
                if new_word in unigrams:
                    if unigrams_cnt[new_word] > max_cnt:
                        correction = new_word
                        c1 = word[i]
                        c2 = letter
                        max_cnt = unigrams_cnt[new_word]
                        if letter in polish_letters and \
                        word[i] == unpolished_letters[polish_letters.index(letter)]:
                            type_of_typo = 'no_alt'
                        else:
                            if letter in unpolished_letters and \
                            (word[i] == polish_letters[unpolished_letters.index(letter)] or \
                                    (letter == 'z' and word[i] == [unpolished_letters.index(letter) + 1])):
                                type_of_typo = 'alt'
                            else:
                                type_of_typo = 'repl'                 
        if i !=  len(word):
            new_word = word[0:i] + word[(i+1):]
            if new_word in unigrams and unigrams_cnt[new_word] > max_cnt:
                correction = new_word
                max_cnt = unigrams_cnt[new_word]
                type_of_typo = 'del'
            if i != len(word) -1:
                new_word = word[0:i] + word[i+1] + word[i] + word[i+2:]
                if new_word in unigrams and unigrams_cnt[new_word] > max_cnt:
                    correction = new_word
                    c1 = word[i]
                    c2 = word[i+1]
                    max_cnt = unigrams_cnt[new_word]
                    type_of_typo = 'trans'
    if type_of_typo:
        if max_cnt/cnt >= treshold:
            Probabilities[type_of_typo] += int(cnt)
            if type_of_typo in ['alt', 'no_alt']:
                Probabilities['repl'] += int(cnt)
            if type_of_typo in ['alt', 'no_alt', 'repl']:
                Probabilities_repl[c1+c2] += int(cnt)
            else:
                if type_of_typo == 'trans':
                    Probabilities_trans[c1+c2] += int(cnt)
                    Proabilities_trans_rev[c1+c2] += int(cnt) + max_cnt
        else:
            return ''
    return correction

def count_probabilities():
    global vocabulary
    global unigrams
    global unigrams_cnt
    global alphabet
    global Probabilities
    global Probabilities_repl
    global Probabilities_trans
    global Proabilities_trans_rev
    for c1 in alphabet:
        for c2 in alphabet:
            if not c1 == c2:
                Probabilities_repl[c1 + c2] = 0.0
                Probabilities_trans[c1 + c2] = 0.0
                Proabilities_trans_rev[c1 + c2] = 0.0
    file_out = codecs.open('typos_from_unigrams', 'w','utf-8')
    for line in open('slownik_do_literowek.txt', 'r'):
        word = unicode(line.strip(), 'utf-8')
        if is_word(word):
            vocabulary.add(word)
    for line in open('1grams', 'r'):
        cnt,word = line.strip().split(' ')
        word = unicode(word, 'utf-8')
        if is_word(word) and int(cnt) >= 8: 
            if word not in vocabulary:
                correction = find_edit(word, int(cnt), 1000.0)
                if correction:
                    file_out.write(word + ' ' + correction+ '\n')
            else:
                if int(cnt) >= 1000.0:
                    unigrams.append(word)
                    unigrams_cnt[word] = int(cnt)
    all_typos_count = float(sum([Probabilities[x] for x in Probabilities]))
    file_out.close()
    file_out = codecs.open('typos_stats', 'w', 'utf-8')
    file_out.write('INSERTS: ' + str(Probabilities['ins']/all_typos_count) + '\n')
    file_out.write('DELETIONS: ' + str(Probabilities['del']/all_typos_count) + '\n')
    file_out.write('REPLACES: ' + str(Probabilities['repl']/all_typos_count) + '\n')
    file_out.write('TRANSPOSITIONS: ' + str(Probabilities['trans']/all_typos_count) + '\n')
    file_out.write('ALT+: ' + str(Probabilities['alt']/all_typos_count) + '\n')
    file_out.write('AlT-: ' + str(Probabilities['no_alt']/all_typos_count) + '\n')
    file_out.write('\n' + 'REPLACES - conditional probabilities:' + '\n')
    for c1 in alphabet:
        for c2 in alphabet:
            if not c1 == c2: 
                file_out.write(c1 + ' --> ' + c2 + ' ' + str(Probabilities_repl[c1+c2] / float(Probabilities['repl'])) + '\n')
    file_out.write('\n' + 'TRANSPOSITION - conditional probabilities:' + '\n')
    for c1 in alphabet:
        for c2 in alphabet:
            if not c1 == c2:
                file_out.write(c1 + ' <-> ' + c2 + ' ' + str(Probabilities_trans[c1+c2] / float(Probabilities['trans'])) + '\n')
    file_out.write('\n' + 'PROBABILITY OF TRANSPOSITION OF LETTERS:' + '\n')
    for c1 in alphabet:
        for c2 in alphabet:
            if not c1 == c2:
                if float(Proabilities_trans_rev[c1+c2]) > 0.0:
                    file_out.write(c1 + ' ?-? ' + c2 + ' ' + str(Probabilities_trans[c1+c2] / float(Proabilities_trans_rev[c1+c2])) + '\n')
                else:
                    file_out.write(c1 + ' ?-? ' + c2 + ' ' + str(0.0) + '\n')
    file_out.close()

def main():
    count_probabilities()

if __name__ == '__main__':
    main()

