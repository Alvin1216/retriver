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
    replacement = ' <span style="color:red;">' + key_lower + '</span> '
    original_string = original_string.replace(key_lower, replacement)
    replacement = ' <span style="color:red;">' + key_capi + '</span> '
    original_string = original_string.replace(key_capi, replacement)
    replacement = ' <span style="color:red;">' + key_up + '</span> '
    original_string = original_string.replace(key_up, replacement)

    return original_string