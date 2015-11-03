import collections

mapping = dict([])
text_words = []
text_suffixes = []

def init_text_tokens(text):
    global text_words
    global text_suffixes
    text_words = [x for x in text.split(' ') if x[0] != '#']
    text_suffixes = [x[1:] for x in text.split(' ') if x[0] == '#']

def is_word(word):
    return word in text_words

def possible_suffixes(word):
    result = []
    for suffix in text_suffixes:
        if word[len(word) - len(suffix):] == suffix:
            result.append('#'+suffix)
    if is_word(word):
        result.append(word)
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
                value = mapping.get(elem1 + ' ' + elem2, 0) + int(cnt)
                mapping[elem1 + ' ' + elem2] = value
    for line in open('3grams'):
        cnt,w1,w2,w3 = line.strip().split(' ')
        w1_possible = possible_suffixes(w1)
        w2_possible = possible_suffixes(w2)
        w3_possible = possible_suffixes(w3)
        for elem1 in w1_possible:
            for elem2 in w2_possible:
                for elem3 in w3_possible:
                    value = mapping.get(elem1 + ' ' + elem2 + ' ' + elem3, 0) + int(cnt)
                    mapping[elem1 + ' ' + elem2 + ' ' + elem3] = value

def main():
    global mapping
    input_text = raw_input('Type!')
    filter_ngrams(input_text)
    for gram in mapping.keys():
        print gram + ' --> ' + str(mapping[gram])

if __name__ == "__main__":
    main()
