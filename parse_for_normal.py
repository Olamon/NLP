#-*- coding: utf-8 -*-
import codecs
import nltk

word_to_base_and_tags = dict({})
base_to_word_and_tags = dict({})

for line in open('skladnicaTagsBases.pl', 'r'):
  line = line[11:-3]
  word,base,tag = line.split(', ')
  word = unicode(word[1:-1], 'utf-8')
  base = unicode(base[1:-1], 'utf-8')
  if word not in word_to_base_and_tags:
    word_to_base_and_tags[word] = []
  word_to_base_and_tags[word].append((tag,base))
  if base not in base_to_word_and_tags:
    base_to_word_and_tags[base] = []
  base_to_word_and_tags[base].append((tag,word))
#gramm_load = nltk.data.load('grammar_with_normal.fcfg')#, encoding='latin1')
#parser = nltk.load_parser('grammar_with_normal.fcfg')

def getBaseForWordAndLPR(word, L, P, R):
  result = []
  if word not in word_to_base_and_tags:
    if L == 'sg' and P == 'nom':
      result.append(word)
    return result
  for (tag,base) in word_to_base_and_tags[word]: 
    tag_list = tag.split(':')
    if len(tag_list) >=4 and tag_list[1] == L and tag_list[2] == P and tag_list[3] == R:
      if tag_list[0] == 'subst':
        result.append(base)
      else:
        if tag_list[1] == 'sg' and tag_list[2] == 'nom':
          result.append(word)
        for (tag2,word2) in base_to_word_and_tags[base]:
          tag_list2 = tag2.split(':')
          if len(tag_list2) >=4 and tag_list[0] == tag_list2[0] and tag_list2[1] == 'sg' and tag_list2[2] == 'nom' and tag_list2[3] == tag_list[3]:
            result.append(word2) 
  return result

grammarstring = codecs.open("grammar_with_normal.fcfg",'r','utf-8').read()
cfg = nltk.grammar.FeatureGrammar.fromstring(grammarstring) 
parser = nltk.parse.featurechart.FeatureChartParser(cfg)

for line in open('phrases.pl','r'):
  line = line[1:-3] 
  line = map(lambda x: unicode(x[1:-1], 'utf-8'), line.split(', '))
  phrase = reduce(lambda x, y: x + ' ' + y, line, '') 
  parsing = []
  try:
    parsing = parser.parse_all(line)
  except ValueError:
    print 'BAD'.encode('utf-8')
  else:
    if not parsing:
      print 'BAD'.encode('utf-8')
    else:
      normals = set([])
      for tree in parsing:
        result = []
        bad = False
        for leaf in tree.subtrees(lambda t: t.height() == 2):
          if(str(leaf)[1:4] == 'NNP' or str(leaf)[1:5] == 'NADJ'):
            word = leaf[0,]
            bases = getBaseForWordAndLPR(word, leaf.label()['L'], leaf.label()['P'], leaf.label()['R'])
            if not bases:
                bad = True
            else:
                result.append(bases[0])
          else:
            result.append(leaf[0,])
        if not bad:
          normals.add(reduce(lambda x,y: x + ' '+  y, result,  ''))
      if len(normals) == 0:
        print 'GOOD [!]'.encode('utf-8')
        print phrase.encode('utf-8')
      else:
        if len(normals) == 1:
          print 'GOOD []'.encode('utf-8')
        else:
          print 'GOOD [*]'.encode('utf-8')
      for normal_form in normals:
        print normal_form.encode('utf-8')
