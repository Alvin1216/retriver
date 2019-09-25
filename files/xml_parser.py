# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 14:28:54 2019

@author: user
"""

# to-do:
# 1. make it to django version
# 2. another struct call 'PubmedBook'
# 3. count_setence is use NLTK now, train a model by yourself!

import re
import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import xml.etree.cElementTree as ET
from collections import Counter

#nltk.download('punkt')

def download_data_from_pubmed(keyword='fever',numbers=100,filename='example'):
    #keyword = 'african swine fever'
    #numbers = 1
    query_artical_id_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    query_artical_id_content = {'db': 'pubmed', 
                     'term': str(keyword),
                     'reldate':'60',
                     'datetype':'edat',
                     'retmax':str(numbers),
                     'usehistory':'title',
                     'field':'title'}
    id_xml_string = requests.post(query_artical_id_url, data = query_artical_id_content).text
    root = ET.fromstring(id_xml_string)
    
    id_list=[]
    for ids in root.iter('Id'):
        id_list.append(ids.text)
    
    query_artical_abstract_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
    query_artical_abstract_content = {'db': 'pubmed', 
                     'id':str(id_list),
                     'retmode':'xml'}
    abstract_string = requests.post(query_artical_abstract_url, data = query_artical_abstract_content).text.encode()
    #filename='pubmed_cancer_100.xml'
    f=open(filename,'wb')
    f.write(abstract_string)
    f.close()
    #parse_xml_abstract_title(abstract_string)
    #print(abstract_string)
    return filename
    

def parse_xml_abstract_title(filename):
    #abstract_root = ET.fromstring(abstract_string)
    print('filename:'+filename)
    tree = ET.parse(str(filename))
    abstract_root = tree.getroot()
    article_title = []
    article_content = []
    count=0
    for i in range(0,len(abstract_root.findall('./PubmedArticle'))):
        #print(i)
        #先檢查有沒有abstract 沒有就跳出來
        if(len(abstract_root.findall('./PubmedArticle')[i].findall('./MedlineCitation/Article/Abstract')) == 0):
            #print("number "+str(i)+"artical not find abstract~")
            count=count+1
            #print('\n')
        else:
            #print("find abstract~")
            article_title.append(abstract_root.findall('./PubmedArticle')[i].findall('./MedlineCitation/Article/ArticleTitle')[0].text)
            #print(abstract_root.findall('./PubmedArticle')[i].findall('./MedlineCitation/Article/ArticleTitle')[0].text)
            
            abstract_text_element=abstract_root.findall('./PubmedArticle')[i].findall('./MedlineCitation/Article/Abstract/AbstractText')
            if(len(abstract_text_element)>1):
                #多段要接成一段
                concat_to_one_passage=''
                for j in range(0,len(abstract_text_element)):
                    concat_to_one_passage=concat_to_one_passage+' '+abstract_text_element[j].text
                article_content.append(concat_to_one_passage)
                #print(concat_to_one_passage)
                #print('\n')
            else:
                concat=''
                for text in abstract_text_element[0].itertext():
                    concat=concat+' '+text
                article_content.append(concat)
                #print(abstract_text_element[0].text)
                #print('\n')
            
    print("有 "+str(count)+" 篇沒有摘要喔!")
    return article_title,article_content

def load_pubmed_from_file(path):
    f = open(path,'r',encoding="utf-8")
    abstract_string=f.read()
    return abstract_string
    #parse_xml_abstract_title(abstract_string)
   # print(type(f.read()))
   
def count_character(input_string):
    return len(input_string)

def count_words(input_string):
    words = Counter(input_string.split())
    wordcount = sum(words.values())
    #print(wordcount)
    return wordcount

def located_keyword(keyword,searched_string):
    keyword=keyword.lower()
    searched_string=searched_string.lower()
    located=[]
    for m in re.finditer(keyword, searched_string):
        located.append(list(m.span()))
    #print(located)
    
    if len(located) == 0:
        return False,located
    else:
        return True,located
    
def count_sentence(artical):
    #with model in nltk
    return len(sent_tokenize(artical))
    
def count_words_v2(artical):
    #this will count a period
    print(word_tokenize(artical))


def load_from_file():
    path = input("輸入檔案路徑:")
    keyword=input("請輸入想找的關鍵字:")
    #xml=load_pubmed_from_file(path)
    title,content=parse_xml_abstract_title(path)
    
    print('檔案中一共有 '+str(len(title))+' 篇含有內文以及標題的文章')
    for i in range(0,len(title)):
        print('這是第 '+str(i+1)+' 篇文章')
        print('標題:'+ title[i])
        print('摘要:'+ content[i])
        print('這篇的摘要有 '+str(count_character(content[i]))+' 個字元')
        print('這篇的摘要有 '+str(count_words(content[i]))+' 個詞')
        print('這篇的摘要有 '+str(count_sentence(content[i]))+' 個句子')
        
        status,located = located_keyword(keyword,title[i])
        print('關鍵字是否存在於標題中:'+ str(status))
        
        if status == True:
            for j in range(0,len(located)):
                print('關鍵字存在於標題中的第:'+ str(located[j]) + '個字元之間')
            
        status,located = located_keyword(keyword,content[i])
        print('關鍵字是否存在於摘要中:'+ str(status))
        
        if status == True:
            for j in range(0,len(located)):
                print('關鍵字存在於摘要中的第:'+ str(located[j]) + '個字元之間')

def load_from_api():
    keyword=input("請輸入想找的關鍵字:")
    filename=input("請輸入儲存檔案的名字:")
    numbers=input("請輸入想找的篇數:")
    xml_filename=download_data_from_pubmed(keyword,numbers,filename)
    #xml=load_pubmed_from_file(path)
    title,content=parse_xml_abstract_title(xml_filename)
    
    print('檔案中一共有 '+str(len(title))+' 篇含有內文以及標題的文章')
    for i in range(0,len(title)):
        print('\n')
        print('這是第 '+str(i+1)+' 篇文章')
        print('標題:'+ title[i])
        print('摘要:'+ content[i])
        print('這篇的摘要有 '+str(count_character(content[i]))+' 個字元')
        print('這篇的摘要有 '+str(count_words(content[i]))+' 個詞')
        print('這篇的摘要有 '+str(count_sentence(content[i]))+' 個句子')
        
        status,located = located_keyword(keyword,title[i])
        print('關鍵字是否存在於標題中:'+ str(status))
        
        if status == True:
            for j in range(0,len(located)):
                print('關鍵字存在於標題中的第:'+ str(located[j]) + '個字元之間')
            
        status,located = located_keyword(keyword,content[i])
        print('關鍵字是否存在於摘要中:'+ str(status))
        
        if status == True:
            for j in range(0,len(located)):
                print('關鍵字存在於摘要中的第:'+ str(located[j]) + '個字元之間')


load_from_api()
