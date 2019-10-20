#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 08:18:01 2019

@author: alvinhuang
"""
import Levenshtein,json
def read_dic():
    f = open('dic.json','r')
    original_dictionary = json.loads(f.read())
    f.close()
    return original_dictionary

def fix_wrong_input(wantfix):
    word_dict = list(read_dic())
    distance_list = []
    distance_index = []
    for i in range(0,len(word_dict)):
        distance_list.append(Levenshtein.distance(wantfix,word_dict[i]))
        distance_index.append(i)
    index_min = distance_list.index(min(distance_list))
    print(word_dict[index_min])
    return word_dict[index_min]

    
