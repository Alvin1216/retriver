# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:53:12 2019

@author: user
"""

# twetter
import json, re
import xml.etree.cElementTree as ET
from collections import Counter
from nltk.tokenize import sent_tokenize


def load_json_from_file(path):
    f = open(path, 'r', encoding="utf-8")
    json_string = f.read()
    json_object = json.loads(json_string)
    # print(json_object)
    return json_object


def get_text_from_json_object(json_object):
    content = []
    for i in range(0, len(json_object)):
        if 'text' in json_object[i]:
            content.append(json_object[i]['text'])
        elif 'Text' in json_object[i]:
            content.append(json_object[i]['Text'])
        else:
            print('not a twitter format!')
    return content


def count_character(input_string):
    return len(input_string)


def count_words(input_string):
    words = Counter(input_string.split())
    wordcount = sum(words.values())
    # print(wordcount)
    return wordcount


def located_keyword(keyword, searched_string):
    keyword = keyword.lower()
    searched_string = searched_string.lower()
    located = []
    for m in re.finditer(keyword, searched_string):
        located.append(list(m.span()))
    # print(located)

    if len(located) == 0:
        return False, located
    else:
        return True, located


def count_sentence(artical):
    # with model in nltk
    return len(sent_tokenize(artical))


def load_from_file():
    path = input("輸入檔案路徑:")
    keyword = input("請輸入想找的關鍵字:")
    json_obj = load_json_from_file(path)
    content = get_text_from_json_object(json_obj)

    print('檔案中一共有 ' + str(len(content)) + ' 篇推文')
    for i in range(0, len(content)):
        print('\n')
        print('這是第 ' + str(i + 1) + ' 篇推文')
        print('推文:' + content[i])
        print('這篇的推文有 ' + str(count_character(content[i])) + ' 個字元')
        print('這篇的推文有 ' + str(count_words(content[i])) + ' 個詞')
        print('這篇的推文有 ' + str(count_sentence(content[i])) + ' 個句子')

        status, located = located_keyword(keyword, content[i])
        print('關鍵字是否存在於推文中:' + str(status))

        if status == True:
            for j in range(0, len(located)):
                print('關鍵字存在於推文中的第:' + str(located[j]) + '個字元之間')

# load_from_file()
