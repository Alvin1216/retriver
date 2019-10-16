import os, re
from django.shortcuts import render, redirect
from ft_retriver.parser import xml_parser as ps
from ft_retriver.parser import python_parser as js
from . import utility as ut

def get_artical_set_xml(path,keyword,count):
    artical_set = []
    title = []
    content = []
    title, content = ps.parse_xml_abstract_title(path)
    numbers = len(title)
    index = 0
    for i in range(0, numbers):
        print(i)
        artical = {}
        artical['status_title'], artical['located_title'] = ps.located_keyword(keyword, title[i])
        artical['status_content'], artical['located_content'] = ps.located_keyword(keyword, content[i])

        if artical['status_title'] == True or artical['status_content'] == True:
            # 有重再全算
            if index >count:
                break
            artical['character_content'] = ps.count_character(content[i])
            artical['wordset'], artical['word_content'] = ps.count_words(content[i])
            artical['wordset'] = artical['wordset'].most_common(10)
            artical['sentence_content'] = ps.count_sentence2(content[i])

            artical['keyword_title_hit'] = len(artical['located_title'])
            artical['keyword_content_hit'] = len(artical['located_content'])

            artical['title'] = ut.mark_string(title[i], keyword)
            artical['o_title'] = title[i]
            artical['content'] = ut.mark_string(content[i], keyword)

            artical['id'] = str(index)

            #artical['common'] = wheather_important_words(artical['wordset'])

            artical_set.append(artical)
            index = index + 1
    hit = len(artical_set)
    return artical_set

def same_rate(a,b):
    count = 0
    limit = min(len(a),len(b),5)
    for i in range(0,limit):
        for j in range(0,limit):
            if a[i]['o_title'] == b[j]['o_title']:
                count = count + 1
    print(count)
    return count/5*100

def wheather_important_words(wordsets):
    words = ['UN', 'CDC', 'FDA', 'WHO', 'WTO', 'NCKU', 'NIH','ZIKV','zika','DENV','dengue','Dengue','Zika']
    key = wordsets.keys()

    c = set(words) & set(key)  # & calculates the intersection.
    print(c)

    return c
    #print(a for a in words if a in key)

def hello(request):
    #return render(request, "ft_retriver/upload.html", locals())
    return render(request, "ft_retriver/index.html", locals())

def hello_result(request):
    #return render(request, "ft_retriver/upload.html", locals())
    return render(request, "ft_retriver/result2.html", locals())

def upload_file(request):
    if request.method == "POST":
        myFile = request.FILES.get("myfile", None)
        if not myFile:
            return redirect('../hello')
        elif ut.check_xml(myFile.name):
            #print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            destination = open(os.path.join("./files", myFile.name), 'wb+')
            for chunk in myFile.chunks():
                destination.write(chunk)
            destination.close()
            now = 'xml'
            status = 'XML upload SUCCESSFUL!'
            information = 'Your xml file had been uploaded!'
            url = '../xml/'
            button_content = 'RESULT'
            file_name = myFile.name
            display_input = True
            #return render(request, "ft_retriver/status.html", locals())
            return render(request, "ft_retriver/result2.html", locals())
        elif ut.check_json(myFile.name):
            destination = open(os.path.join(".\\files", myFile.name), 'wb+')
            for chunk in myFile.chunks():
                destination.write(chunk)
            destination.close()
            now = 'json'
            status = 'JSON upload SUCCESSFUL!'
            display_input = True
            information = 'Your json file had been uploaded!'
            url = '../json/'
            button_content = 'RESULT'
            file_name = myFile.name
            #return render(request, "ft_retriver/status.html", locals())
            return render(request, "ft_retriver/result2.html", locals())
        else:
            status = 'FAILED!'
            information = 'Your file is not a xml/json file.'
            url = '../hello'
            button_content = 'BACK'
            #return render(request, "ft_retriver/status.html", locals())
            return render(request, "ft_retriver/result2.html", locals())

def xml_deal(request):
    print(request.POST['keyword'])
    print(request.POST['file_name'])
    print(request.POST['statusParse'])
    file_name = request.POST['file_name']
    statusParse=request.POST['statusParse']
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(BASE_DIR)
    path = os.path.join(BASE_DIR, "./files/" + file_name)
    upload_file_type = 'xml'
    cheacker = request.POST['keyword'].find(',')
    if cheacker != -1:
        keyword = request.POST['keyword']
        keywords = request.POST['keyword'].split(',')
        articalset_b= get_artical_set_xml(path,keywords[0],5)
        articalset_a= get_artical_set_xml(path,keywords[1],5)
        #print('here!')
        #print(articalset_a)
        #print(articalset_b)
        sr = same_rate(articalset_b,articalset_a)
        return render(request, "ft_retriver/result_sep.html", locals())
        #表示有兩個關鍵字，要分兩邊
    else:
        #表示跟原來的依樣
        keyword = request.POST['keyword']
        if not ut.check_file_exist(path):
            return render(request, "ft_retriver/status.html", ut.deal_failed())
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
                    artical['wordset'], artical['word_content'] = ps.count_words(content[i])
                    artical['sentence_content'] = ps.count_sentence2(content[i])

                    artical['keyword_title_hit'] = len(artical['located_title'])
                    artical['keyword_content_hit'] = len(artical['located_content'])

                    artical['title'] = ut.mark_string(title[i], keyword)
                    artical['content'] = ut.mark_string(content[i], keyword)

                    artical['id'] = 'id_' + str(i)

                    artical['common'] = wheather_important_words(artical['wordset'])
                    artical['zipf_picture'] = ps.generate_zipf_picture(artical['wordset'],title[i][0:10])

                    artical_set.append(artical)
            hit = len(artical_set)
            return render(request, "ft_retriver/result3.html", locals())

def json_deal(request):
    file_name = request.POST['file_name']
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "files/" + file_name)
    keyword = request.POST['keyword']
    type = 'json'

    if not ut.check_file_exist(path):
        return render(request, "ft_retriver/status.html", ut.deal_failed())
    else:
        json_obj = js.load_json_from_file(path)
        content,user = js.get_text_from_json_object(json_obj)
        #print(json_obj)
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
                artical['wordset'],artical['word_content'] = ps.count_words(content[i])
                artical['sentence_content'] = ps.count_sentence2(content[i])

                artical['keyword_content_hit'] = len(artical['located_content'])

                artical['content'] = ut.mark_string(content[i], keyword)
                print(artical['content'])
                artical['tag'] = ut.sperate_tag(content[i])
                artical['http'] = ut.sperate_http(content[i])
                artical['id'] = 'id'+str(i)
                #print(type(content[i]))
                if len(user) != 0:
                    artical['title'] = "這是第 " + str(count) + "篇含有關鍵字的推文，來自author_id: "+str(user[i])
                else:
                    artical['title'] = "這是第 " + str(count) + "篇含有關鍵字的推文"
                count += 1

                artical['common'] = wheather_important_words(artical['wordset'])
                #artical['a'] = sperate_tag(content[i])
                #print(type(content[i]))

                artical_set.append(artical)
        hit = len(artical_set)
        return render(request, "ft_retriver/result3.html", locals())

def getCompare(request):
    print(request.POST['keyword'])
    print(request.POST['file_name'])
    print(request.POST['statusParse'])
    file_name = request.POST['file_name']
    statusParse=request.POST['statusParse']
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "files/" + file_name)
    keyword = request.POST['keyword'].spilt(',')
    upload_file_type = 'xml'
    # print(check_file_exist(path))
    # print(path)

    if not ut.check_file_exist(path):
        return render(request, "ft_retriver/status.html", ut.deal_failed())
    else:
        artical_setA = []
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
                artical['wordset'],artical['word_content'] = ps.count_words(content[i])
                artical['sentence_content'] = ps.count_sentence2(content[i])

                artical['keyword_title_hit'] = len(artical['located_title'])
                artical['keyword_content_hit'] = len(artical['located_content'])

                artical['title'] = ut.mark_string(title[i], keyword)
                artical['content'] = ut.mark_string(content[i], keyword)

                artical['id'] = 'id_'+str(i)

                artical_setA.append(artical)
        hitA = len(artical_setA)
        return render(request, "ft_retriver/result3.html", locals())

