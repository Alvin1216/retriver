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
    replacement = ' <span style="color:red;">' + keyword + '</span> '
    original_string = original_string.replace(keyword, replacement)
    return original_string