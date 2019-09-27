import os, re
from django.shortcuts import render, redirect
from ft_retriver.parser import xml_parser as ps
from ft_retriver.parser import python_parser as js
from pathlib import Path
from django.template import loader


def hello(request):
    a = 'hello'
    return render(request, "ft_retriver/upload_xml.html", locals())


def check_xml_json(filename):
    pattern = re.compile(r'^.*?.xml$|^.*?.json$')
    match = pattern.match(filename)
    if match:
        return True
    else:
        return False


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


def upload_file(request):
    if request.method == "POST":
        myFile = request.FILES.get("myfile", None)
        if not myFile:
            return redirect('../hello')
        elif check_xml(myFile.name):
            destination = open(os.path.join(".\\files", myFile.name), 'wb+')
            for chunk in myFile.chunks():
                destination.write(chunk)
            destination.close()
            status = 'XML upload SUCCESSFUL!'
            information = 'Your xml file had been uploaded!'
            url = '../xml/'
            button_content = 'RESULT'
            file_name = myFile.name
            display_input = True
            return render(request, "ft_retriver/status.html", locals())
        elif check_json(myFile.name):
            destination = open(os.path.join(".\\files", myFile.name), 'wb+')
            for chunk in myFile.chunks():
                destination.write(chunk)
            destination.close()
            status = 'JSON upload SUCCESSFUL!'
            display_input = True
            information = 'Your json file had been uploaded!'
            url = '../json/'
            button_content = 'RESULT'
            file_name = myFile.name
            return render(request, "ft_retriver/status.html", locals())
        else:
            status = 'FAILED!'
            information = 'Your file is not a xml/json file.'
            url = '../hello'
            button_content = 'BACK'
            return render(request, "ft_retriver/status.html", locals())


def mark_string(original_string, keyword):
    replacement = ' <span style="color:red;">' + keyword + '</span> '
    original_string = original_string.replace(keyword, replacement)
    return original_string


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


def xml_deal(request):
    print(request.POST['keyword'])
    print(request.POST['file_name'])
    file_name = request.POST['file_name']
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "files/" + file_name)
    keyword = request.POST['keyword']
    upload_file_type = 'xml'
    # print(check_file_exist(path))
    # print(path)

    if not check_file_exist(path):
        return render(request, "ft_retriver/status.html", deal_failed())
    else:
        artical_set = []
        title = []
        content = []
        title, content = ps.parse_xml_abstract_title(path)
        numbers = len(title)
        type = 'xml'
        for i in range(0, numbers):
            print(i)
            artical = {}
            artical['status_title'], artical['located_title'] = ps.located_keyword(keyword, title[i])
            artical['status_content'], artical['located_content'] = ps.located_keyword(keyword, content[i])

            if artical['status_title'] == True or artical['status_content'] == True:
                # 有重再全算
                artical['character_content'] = ps.count_character(content[i])
                artical['word_content'] = ps.count_words(content[i])
                artical['sentence_content'] = ps.count_sentence(content[i])

                artical['keyword_title_hit'] = len(artical['located_title'])
                artical['keyword_content_hit'] = len(artical['located_content'])

                artical['title'] = mark_string(title[i], keyword)
                artical['content'] = mark_string(content[i], keyword)

                artical_set.append(artical)
        hit = len(artical_set)
        return render(request, "ft_retriver/result.html", locals())


def json_deal(request):
    file_name = request.POST['file_name']
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "files/" + file_name)
    keyword = request.POST['keyword']
    type = 'json'

    if not check_file_exist(path):
        return render(request, "ft_retriver/status.html", deal_failed())
    else:
        json_obj = js.load_json_from_file(path)
        content = js.get_text_from_json_object(json_obj)
        print(json_obj)
        artical_set = []
        title = []
        numbers = len(content)
        count = 1
        print(content)
        for i in range(0, numbers):
            print(i)
            artical = {}
            artical['status_content'], artical['located_content'] = ps.located_keyword(keyword, content[i])

            if artical['status_content'] == True:
                # 有重再全算
                artical['character_content'] = ps.count_character(content[i])
                artical['word_content'] = ps.count_words(content[i])
                artical['sentence_content'] = ps.count_sentence(content[i])

                artical['keyword_content_hit'] = len(artical['located_content'])

                artical['content'] = mark_string(content[i], keyword)
                artical['title'] = "這是第 " + str(count) + "篇含有關鍵字的推文"
                count += 1

                artical_set.append(artical)
        hit = len(artical_set)
        return render(request, "ft_retriver/result.html", locals())
