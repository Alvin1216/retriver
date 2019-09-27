import os, re
from django.shortcuts import render, redirect
from ft_retriver.parser import xml_parser as ps
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


def upload_file(request):
    if request.method == "POST":
        myFile = request.FILES.get("myfile", None)
        if not myFile:
            return redirect('../hello')
        elif not check_xml_json(myFile.name):
            status = 'FAILED!'
            information = 'Your file is not a xml/json file.'
            url = '../hello'
            button_content = 'BACK'
            return render(request, "ft_retriver/status.html", locals())
        else:
            destination = open(os.path.join(".\\files", myFile.name), 'wb+')
            for chunk in myFile.chunks():
                destination.write(chunk)
            destination.close()
            status = 'SUCCESSFUL!'
            information = 'Your file had been uploaded!'
            url = '../xml/'
            button_content = 'RESULT'
            file_name=myFile.name
            #return render(request, "ft_retriver/status.html", deal_failed())
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
    load_data = {'status': 'FAILED!', 'information': 'Your file not exist', 'url':'.../hello',
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
    #print(check_file_exist(path))
    #print(path)

    if not check_file_exist(path):
        return render(request, "ft_retriver/status.html", deal_failed())
    else:
        artical_set = []
        title = []
        content = []
        title, content = ps.parse_xml_abstract_title(path)
        numbers = len(title)
        for i in range(0, numbers):
            print(i)
            artical = {}

            artical['character_content'] = ps.count_character(content[i])
            artical['word_content'] = ps.count_words(content[i])
            artical['sentence_content'] = ps.count_sentence(content[i])

            artical['status_title'], artical['located_title'] = ps.located_keyword(keyword, title[i])
            artical['status_content'], artical['located_content'] = ps.located_keyword(keyword, content[i])

            artical['keyword_title_hit'] = len(artical['located_title'])
            artical['keyword_content_hit'] = len(artical['located_content'])

            artical['title'] = mark_string(title[i], keyword)
            artical['content'] = mark_string(content[i], keyword)

            if artical['status_title']==True or artical['keyword_content_hit'] ==True:
                artical_set.append(artical)

        hit=len(artical_set)
        return render(request, "ft_retriver/result.html", locals())

