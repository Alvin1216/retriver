import os, re ,json
from django.shortcuts import render, redirect
from ft_retriver.parser import xml_parser as ps
from ft_retriver.parser import python_parser as js
from pathlib import Path
from collections import Counter


def make_a_dictionary(contents):
    # make a first version dictionary
    # if can open continue the dictionary
    # new one make it to dictionary
    try:
        f = open('dic.json', 'r')
        original_dictionary = json.loads(f.read())
        f.close()

        original_wordset = Counter(original_dictionary)
        new_dic = original_wordset

        for content in contents:
            input_string = re.sub("[^A-Za-z]", " ", content.strip()).lower()
            input_wordset = Counter(input_string.split())
            new_dic = new_dic + input_wordset
        new_dic = dict(new_dic.most_common())
        write_back = json.dumps(new_dic)

        f = open('dic.json', 'w')
        f.write(write_back)
        f.close()
    except:
        new_dic = Counter()
        for content in contents:
            input_string = re.sub("[^A-Za-z]", " ", content.strip()).lower()
            input_wordset = Counter(input_string.split())
            new_dic = new_dic + input_wordset
        new_dic = dict(new_dic.most_common())
        write_back = json.dumps(new_dic)

        f = open('dic.json', 'w')
        f.write(write_back)
        f.close()

def make_a_dictionary(contents):
    # make a first version dictionary
    # if can open continue the dictionary
    # new one make it to dictionary
    try:
        f = open('dic.json', 'r')
        original_dictionary = json.loads(f.read())
        f.close()

        original_wordset = Counter(original_dictionary)
        new_dic = original_wordset

        for content in contents:
            input_string = re.sub("[^A-Za-z]", " ", content.strip()).lower()
            input_wordset = Counter(input_string.split())
            new_dic = new_dic + input_wordset
        new_dic = dict(new_dic.most_common())
        write_back = json.dumps(new_dic)

        f = open('dic.json', 'w')
        f.write(write_back)
        f.close()
    except:
        new_dic = Counter()
        for content in contents:
            input_string = re.sub("[^A-Za-z]", " ", content.strip()).lower()
            input_wordset = Counter(input_string.split())
            new_dic = new_dic + input_wordset
        new_dic = dict(new_dic.most_common())
        write_back = json.dumps(new_dic)

        f = open('dic.json', 'w')
        f.write(write_back)
        f.close()

def make_text_distribution(contents,size = 50):
    #size = -1  return all
    new_dic = Counter()
    for content in contents:
        input_string = re.sub("[^A-Za-z]", " ", content.strip()).lower()
        input_wordset = Counter(input_string.split())
        new_dic = new_dic + input_wordset
    if(size != -1):
        new_dic_x, new_dic_y = ps.zipf_picture_data(new_dic, length=size)
        return new_dic_x, new_dic_y
    else:
        return dict(new_dic.most_common())

def make_text_distribution_poter(contents,size = 50):
    #size = -1  return all
    new_dic = Counter()
    for content in contents:
        input_wordset = ps.wordset_by_poter(content)
        #input_string = re.sub("[^A-Za-z]", " ", content.strip()).lower()
        #input_wordset = Counter(input_string.split())
        new_dic = new_dic + input_wordset
    if(size != -1):
        new_dic_x, new_dic_y = ps.zipf_picture_data(new_dic, size)
        return new_dic_x, new_dic_y
    else:
        return dict(new_dic.most_common())

def check_json(filename):
    pattern = re.compile(r'^.*?.json$')
    match = pattern.match(filename)
    if match:
        return True
    else:
        return False


def check_xml(filename):
    pattern = re.compile(r'^.*?.xml$')
    match = pattern.match(filename)
    if match:
        return True
    else:
        return False

def check_file_exist(path):
    file = Path(path)
    if file.is_file():
        return True
    else:
        return False

def deal_failed():
    load_data = {'status': 'FAILED!', 'information': 'Your file not exist', 'url': '.../hello',
                 'button_content': 'BACK'}
    return load_data



def mark_string(original_string, keyword):
    key_lower=keyword.lower()
    key_capi=keyword.capitalize()
    key_up=keyword.upper()
    key_title=keyword.title()
    replacement = ' <span style="color:red;">' + key_lower + '</span> '
    original_string = original_string.replace(key_lower, replacement)
    replacement = ' <span style="color:red;">' + key_capi + '</span> '
    original_string = original_string.replace(key_capi, replacement)
    replacement = ' <span style="color:red;">' + key_up + '</span> '
    original_string = original_string.replace(key_up, replacement)
    replacement = ' <span style="color:red;">' + key_title + '</span> '
    original_string = original_string.replace(key_title, replacement)

    return original_string


def sperate_http(original_string):
    regex = r'http://[a-z0-9A-Z./?=#-_]+'
    match = re.findall(regex, original_string)
    http_connect = ''
    for a in match:
        http_connect = '<a href ="' + a + '">' + a + '</a>'
    return http_connect

def sperate_tag(original_string):
    print(original_string)
    regex = r'#\s[a-zA-z0-9]+'
    match = re.findall(regex, original_string)
    return_str = ''
    for a in match:
        url_use = 'https://twitter.com/search?q='+a.replace('# ','%23')
        tag_connect='<a href ="'+ url_use +'">'+a+'</a>'
        return_str = return_str+' '+tag_connect
        print(return_str)
    return return_str