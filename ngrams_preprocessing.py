#-*- coding: utf-8 -*-
import dbm
import collections

def init_words_mapping(bigram_file, trigram_file, bigram_K, trigram_K):
  ngrams_mapping = dbm.open('ngrams_mapping_uniform', 'c')
  key_set_const = '_key_set_'
  for line in open(bigram_file, 'r'):
      cnt,w1,w2 = line.strip().split(' ')
      if int(cnt) < int(bigram_K):
          continue
      value = ngrams_mapping.get(w1, '') + '#' + w2
      key_set = ngrams_mapping.get(key_set_const, '') + '#' + w1
      ngrams_mapping[w1] = value
      ngrams_mapping[key_set_const] = key_set
  for line in open(trigram_file, 'r'):
      cnt,w1,w2,w3 = line.strip().split(' ')
      if int(cnt) < int(trigram_K):
          continue
      key = w1 + ' ' + w2
      value = ngrams_mapping.get(key, '') + '#' + w3
      key_set = ngrams_mapping.get(key_set_const, '') + '#' + key
      ngrams_mapping[key] = value
      ngrams_mapping[key_set_const] = key_set
  ngrams_mapping.close()

def init_words_mapping_with_counts(bigram_file, trigram_file, bigram_K, trigram_K):
    ngrams_mapping = dbm.open('ngrams_mapping_weighted', 'c')
    bigram_cnt_const = '_bigram_cnt_'
    key_set_const = '_key_set_'
    ngrams_mapping[bigram_cnt_const] = '0'
    for line in open(bigram_file, 'r'):
        all_bigram_cnt = int(ngrams_mapping[bigram_cnt_const])
        cnt,w1,w2 = line.strip().split(' ')
        if int(cnt) < int(bigram_K):
            continue
        key = w1 + ' ' + w2
        ngrams_mapping[bigram_cnt_const] = str(all_bigram_cnt + int(cnt))
        ngrams_mapping[key_set_const] = ngrams_mapping.get(key_set_const, '') + '#' + cnt + '^' + key
        ngrams_mapping['#'+w1] = ngrams_mapping.get('#'+w1, '') + '#' + cnt + '^' + key
    for line in open(trigram_file, 'r'):
        cnt,w1,w2,w3 = line.strip().split(' ')
        if  int(cnt) < int(trigram_K):
            continue
        key = w1 + ' ' + w2
        value = ngrams_mapping.get(key, '') + '#' + cnt + '^' + w3
        ngrams_mapping[key] = value
    ngrams_mapping.close()
