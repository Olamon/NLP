#-*- coding: utf-8 -*-
import codecs

nr_sen = 0
nr_not_project_sen = 0

no_to_word = dict({})
no_to_children = dict({})
no_to_parent = dict({})

def check_connected(start, finish):
    if start == finish:
        return True
    if start not in no_to_children:
        return False
    for child in no_to_children[start]:
        if child == finish:
            return True
        else:
            if check_connected(child, finish):
                return True
    return False

def check_in_order(node):
    if node not in no_to_children or not no_to_children[node]:
        return [node, node, True]
    for child in no_to_children[node]:
        guilty,found_in,good = check_in_order(child)
        if not good:
            return [guilty,found_in,good]
        if int(node) < int(child):
            for no in range(int(node) + 1, int(child)): 
                if not check_connected(node, str(no)):
                    return [node, child, False]
        else:
            for no in range(int(child) + 1, int(node)):
                if not check_connected(node, str(no)):
                    return [child, node, False]   
    return [node, node, True]

for line in open('zaleznosci.cnoll', 'r'):
    if line == '\n':
        for no in no_to_children:
            no_to_children[no] = sorted(no_to_children[no])
        left,right,good = check_in_order('0')
        nr_sen +=1
        if not good:
            nr_not_project_sen +=1
            print 'SENTENCE:' + reduce(lambda x, y: x + ' ' + y, \
[no_to_word[str(no)] for no in sorted([int(x) for x in no_to_word])])
            print 'GUILTY: ' + no_to_word[left] + ' ' + no_to_word[right]
        no_to_word.clear()
        no_to_children.clear()
    else:
        line = line.split()
        no_to_word[line[0]] = line[1]
        no_to_parent[line[0]] = line[6]
        if line[6] not in no_to_children:
            no_to_children[line[6]] = []
        no_to_children[line[6]].append(line[0])

print 'RESULT' + str(float(nr_not_project_sen)/float(nr_sen))
