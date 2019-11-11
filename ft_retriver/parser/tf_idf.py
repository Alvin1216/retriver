#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 00:36:48 2019

@author: alvinhuang
"""


import re,math,requests,nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import PorterStemmer
import xml.etree.cElementTree as ET
from collections import Counter
from nltk.corpus import stopwords

def parse_xml_abstract_title(filename):
    # abstract_root = ET.fromstring(abstract_string)
    print('filename:' + filename)
    # filename='que.xml'
    tree = ET.parse(str(filename))
    abstract_root = tree.getroot()
    article_title = []
    article_content = []
    count = 0
    for i in range(0, len(abstract_root.findall('./PubmedArticle'))):
        print(i)
        # 先檢查有沒有abstract 沒有就跳出來
        if (len(abstract_root.findall('./PubmedArticle')[i].findall('./MedlineCitation/Article/Abstract')) == 0):
            # print("number "+str(i)+"artical not find abstract~")
            count = count + 1
            # print('\n')
        else:
            # print("find abstract~")
            abstract_title_element = abstract_root.findall('./PubmedArticle')[i].findall(
                './MedlineCitation/Article/ArticleTitle')
            concat_title = ''
            for text in abstract_title_element[0].itertext():
                concat_title = concat_title + ' ' + text
                # print(text)
            # print(abstract_root.findall('./PubmedArticle')[i].findall('./MedlineCitation/Article/ArticleTitle')[0].text)
            article_title.append(concat_title)
            print(concat_title)
            abstract_text_element = abstract_root.findall('./PubmedArticle')[i].findall(
                './MedlineCitation/Article/Abstract/AbstractText')
            if (len(abstract_text_element) > 1):
                # 多段要接成一段
                concat_to_one_passage = ''
                for j in range(0, len(abstract_text_element)):
                    for text in abstract_text_element[j].itertext():
                        concat_to_one_passage = concat_to_one_passage + ' ' + str(text)
                article_content.append(concat_to_one_passage)
                print(concat_to_one_passage)
                # print('\n')
            else:
                concat = ''
                for text in abstract_text_element[0].itertext():
                    concat = concat + ' ' + text
                article_content.append(concat)
                # print(abstract_text_element[0].text)
                # print('\n')

    print("有 " + str(count) + " 篇沒有摘要喔!")
    return article_title, article_content

def merge_contents_titles(titles, contents):
    new_contents = []
    for index in range(0,len(titles)):
        new_contents.append(titles[index]+contents[index])
    return new_contents

def filter_to_clean_wordset(contents):
    content_wordset = []
    for index in range(0,len(contents)):
        word_list = nltk.word_tokenize(contents[index])
        filtered_words = [word.lower() for word in word_list if word.lower() not in stopwords.words('english') and word.isalpha()]
        content_wordset.append(filtered_words)
        print(filtered_words)
    return content_wordset

def hit_keyword_in_documents(keyword,contents_clean_wordset):
    keyword = keyword.lower()
    total_hit = 0
    for index in range(0,len(contents_clean_wordset)):
        if keyword in contents_clean_wordset[index]:
            total_hit = total_hit + 1
    return total_hit

def count_words_in_one_document(contents_clean_wordset):
    #統計每一篇文章的字詞 例如 deep出現了幾次 從大排到小
    words_most_common_sets = []
    for index in range(0,len(contents_clean_wordset)):
        words_most_common_sets.append(Counter(contents_clean_wordset[index]).most_common())
    return words_most_common_sets

def count_words_in_all_documents(contents_clean_wordset):
    wordsets_all = []
    for index in range(0,len(contents_clean_wordset)):
        wordsets_all.extend(contents_clean_wordset[index])
        #words_most_common_sets.append(Counter(contents_clean_wordset[index]).most_common())
    wordsets_order_all = list(Counter(wordsets_all).most_common())
    return wordsets_order_all

def count_tf(keyword,contents_words_after_count):
    #算一個關鍵字在一個文件中出現的次數
    #一次算全部文章的tf 回傳tf_list
    tf_list = []
    
    for index in range(0,len(contents_words_after_count)):
        numbers_of_this_doc = sum(Counter(contents_words_after_count[index]).values())
        artical = contents_words_after_count[index]
        print(artical)
        word_number_in_this_doc = 0
        for item in artical:
            if item[0] == keyword:
                word_number_in_this_doc = item[1]
                break
        tf = word_number_in_this_doc/numbers_of_this_doc
        tf_list.append(tf)
    return tf_list

def count_idf(keyword,contents_clean_wordset):
    lenth_of_this_doc_set = len(contents_clean_wordset)
    hit_numbers_keyword_in_documents = hit_keyword_in_documents(keyword,contents_clean_wordset)
    return math.log(lenth_of_this_doc_set/(hit_numbers_keyword_in_documents+1))
    #
    
def tf_logarithm(original_fd):
    #傳入單個fd值
    #from wikipedia
    if original_fd >0:
        return 1+math.log(original_fd)
    else:
        return 0
    
def tf_boolean(original_tf):
    #傳入單個tf值
    if original_tf > 0:
        return 1
    else:
        return 0
    
def tf_raw_count(keyword,contents_words_after_count):
    #from wikipedia
    tf_list=[]
    for index in range(0,len(contents_words_after_count)):
        artical = contents_words_after_count[index]
        word_number_in_this_doc = 0
        for item in artical:
            if item[0] == keyword:
                word_number_in_this_doc = item[1]
                break
        tf = word_number_in_this_doc
        tf_list.append(tf)
    return tf_list

def tf_double_k_normalization(keyword,contents_words_after_count,k):
    #from wikipedia
    tf_list = []
    for index in range(0,len(contents_words_after_count)):
        artical = contents_words_after_count[index]
        word_number_in_this_doc = 0
        for item in artical:
            if item[0] == keyword:
                word_number_in_this_doc = item[1]
                break
        numbers_of_top_words = artical[0][1]
        tf = k + (1-k) * word_number_in_this_doc/numbers_of_top_words
        tf_list.append(tf)
    return tf_list

def idf_smooth(original_idf):
    #from_wikipedia
    return original_idf+1

def idf_max(keyword,contents_clean_wordset):
    #from wikipedia
    #numbers_of_top_words = contents_clean_wordset[]
    max_nt = count_words_in_all_documents(contents_clean_wordset)[0][1]
    hit_numbers_keyword_in_documents = hit_keyword_in_documents(keyword,contents_clean_wordset)
    return math.log(max_nt/(hit_numbers_keyword_in_documents+1))
    
    
# titles, contents = parse_xml_abstract_title("pubmed_brca.xml")
# keyword = "cancer"
# contents = merge_contents_titles(titles, contents)
# contents_clean_wordset = filter_to_clean_wordset(contents)
# contents_words_after_count = count_words_in_one_document(contents_clean_wordset)
# idf = count_idf(keyword,contents_clean_wordset)

# #拿到這個就可以用來排序
#
# #v1
# #from_text_book
# #tftd x logn/dft
# tf_idf_list = []
# tf_list=[]
# tf_list = count_tf(keyword,contents_words_after_count)
# for index in range(0,len(tf_list)):
#     tf_idf = tf_list[index]*idf
#     tf_idf_with_index = (tf_idf,index)
#     tf_idf_list.append(tf_idf_with_index)
# sorted_tf_idf_list_v1 = []
# sorted_tf_idf_list_v1 = sorted(tf_idf_list, key=lambda tup: tup[0])
# sorted_tf_idf_list_v1.reverse()
#
# #v2
# #from_wiki recommendation
# #1+log(ftd) x logn/dft
# tf_idf_list = []
# tf_list=[]
# tf_list =  tf_raw_count(keyword,contents_words_after_count)
# for index in range(0,len(tf_list)):
#     tf_idf = tf_logarithm(tf_list[index])*idf
#     tf_idf_with_index = (tf_idf,index)
#     tf_idf_list.append(tf_idf_with_index)
# sorted_tf_idf_list_v2 = []
# sorted_tf_idf_list_v2 = sorted(tf_idf_list, key=lambda tup: tup[0])
# sorted_tf_idf_list_v2.reverse()
#
# #v3
# #from_wiki recommendation
# #0.5+0.5*ftd/maxftd x logn/dft
# tf_idf_list = []
# tf_list=[]
# tf_list =  tf_double_k_normalization(keyword,contents_words_after_count,0.5)
# for index in range(0,len(tf_list)):
#     tf_idf = tf_list[index]*idf
#     tf_idf_with_index = (tf_idf,index)
#     tf_idf_list.append(tf_idf_with_index)
# sorted_tf_idf_list_v3 = []
# sorted_tf_idf_list_v3 = sorted(tf_idf_list, key=lambda tup: tup[0])
# sorted_tf_idf_list_v3.reverse()



#keyword_set = merge_contents_titles(titles[0], contents[0])
#keyword_set_clean = filter_to_clean_wordset(keyword_set)



