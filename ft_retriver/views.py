import os, re
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from ft_retriver.parser import xml_parser as ps


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
            url = '#'
            button_content = 'RESULT'
            return render(request, "ft_retriver/status.html", locals())


def mark_string(original_string, keyword):
    replacement = ' <span style="color:red;">' + keyword + '</span> '
    original_string = original_string.replace(keyword, replacement)
    return original_string

def xml_deal(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "files\pubmed_fever_100.xml")
    # print(BASE_DIR)
    # print(path)
    keyword = 'fever'
    artical_set = []
    title = []
    content = []
    title, content = ps.parse_xml_abstract_title(path)
    numbers = len(title)
    # print(title[0])
    for i in range(0, numbers):
        print(i)
        artical = {}

        artical['character_content'] = ps.count_character(content[i])
        artical['word_content'] = ps.count_words(content[i])
        artical['sentence_content'] = ps.count_sentence(content[i])

        artical['status_title'], artical['located_title'] = ps.located_keyword(keyword, title[i])
        artical['status_content'], artical['located_content'] = ps.located_keyword(keyword, content[i])

        artical['title'] = mark_string(title[i], keyword)
        artical['content'] = mark_string(content[i], keyword)

        artical_set.append(artical)

    for x in artical_set:
        print(x)

    return render(request, "ft_retriver/result.html", locals())
