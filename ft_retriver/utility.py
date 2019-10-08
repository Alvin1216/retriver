import os, re
from django.shortcuts import render, redirect
from ft_retriver.parser import xml_parser as ps
from ft_retriver.parser import python_parser as js
from pathlib import Path

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