#-*- coding: utf-8 -*-
import codecs

def main():
  out_sklad = codecs.open('rewritten_skladnica.fcfg', 'w', 'utf-8')
  for line in open('skladnicaTagsBases.pl', 'r'):
    line = unicode(line, 'utf-8')
    line = line[11:-3]
    word,base,tag = line.split(', ')
    if tag[:6] == 'subst:':
      L,P,R = tag.split(':')[1:]
      out_sklad.write('NNP[L='+L+',P='+P+',R='+R+'] -> ' + word + '\n')
      out_sklad.write('NP[L='+L+',P='+P+',R='+R+'] -> ' + word + '\n')
    if tag[:4] == 'adj:':
      L,P,R = tag.split(':')[1:4]
      out_sklad.write('NADJ[L='+L+',P='+P+',R='+R+'] -> ' + word + '\n')
      out_sklad.write('ADJ[L='+L+',P='+P+',R='+R+'] -> ' + word + '\n')
    if tag[:5] == 'ppas:':
      L,P,R = tag.split(':')[1:4]
      out_sklad.write('NADJ[L='+L+',P='+P+',R='+R+'] -> ' + word + '\n')
      out_sklad.write('ADJ[L='+L+',P='+P+',R='+R+'] -> ' + word + '\n')
    if tag[:5] == 'prep:':
      out_sklad.write('PREP -> ' + word + '\n')

if __name__ == "__main__":
  main()
