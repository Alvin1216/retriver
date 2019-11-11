import os,re,nltk
import numpy as np
from django.shortcuts import render, redirect
from ft_retriver.parser import xml_parser as ps
from ft_retriver.parser import python_parser as js
from ft_retriver.parser import edit_distance as ed
from ft_retriver.parser import tf_idf as ti
from . import utility as ut
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from collections import Counter
from scipy import sparse


def get_artical_set_xml(path, keyword, count):
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
            if index > count:
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

            # artical['common'] = wheather_important_words(artical['wordset'])

            artical_set.append(artical)
            index = index + 1
    hit = len(artical_set)
    return artical_set


def same_rate(a, b):
    count = 0
    limit = min(len(a), len(b), 5)
    for i in range(0, limit):
        for j in range(0, limit):
            if a[i]['o_title'] == b[j]['o_title']:
                count = count + 1
    print(count)
    return count / 5 * 100


def wheather_important_words(wordsets):
    words = ['UN', 'CDC', 'FDA', 'WHO', 'WTO', 'NCKU', 'NIH', 'ZIKV', 'zika', 'DENV', 'dengue', 'Dengue', 'Zika']
    key = wordsets.keys()

    c = set(words) & set(key)  # & calculates the intersection.
    print(c)

    return c
    # print(a for a in words if a in key)


def hello(request):
    # return render(request, "ft_retriver/upload.html", locals())
    return render(request, "ft_retriver/index.html", locals())


def text_distribution(request):
    if request.method == "POST":
        status = 'filein'
        myFile = request.FILES.get("myfile", None)
        if not myFile:
            return redirect('../text_distribution/')
        elif ut.check_xml(myFile.name):
            destination = open(os.path.join("./files", myFile.name), 'wb+')
            for chunk in myFile.chunks():
                destination.write(chunk)
            destination.close()
            status = 'xml'
            title, content = ps.parse_xml_abstract_title('./files/' + myFile.name)
            new_dic_x, new_dic_y = ut.make_text_distribution(content)
            title = myFile.name + " distribution"
            new_dic_x_p, new_dic_y_p = ut.make_text_distribution_poter(content)
            title_p = myFile.name + " distribution by poter algorithm"
            # set = ut.make_text_distribution(content,-1)
            # print (set)

            display_list = []
            length = len(new_dic_x)
            for i in range(0, length):
                display = {}
                if i < len(new_dic_x_p):
                    display['key'] = new_dic_x[i]
                    display['value'] = new_dic_y[i]
                    display['key_p'] = new_dic_x_p[i]
                    display['value_p'] = new_dic_y_p[i]
                else:
                    display['key'] = new_dic_x[i]
                    display['value'] = new_dic_y[i]
                    display['key_p'] = ''
                    display['value_p'] = ''
                display['row'] = i+1
                display_list.append(display)

            return render(request, "ft_retriver/whole.html", locals())
        elif ut.check_json(myFile.name):
            destination = open(os.path.join("./files", myFile.name), 'wb+')
            for chunk in myFile.chunks():
                destination.write(chunk)
            destination.close()
            status = 'json'
            json_obj = js.load_json_from_file('./files/' + myFile.name)
            content, user = js.get_text_from_json_object(json_obj)
            new_dic_x, new_dic_y = ut.make_text_distribution(content)
            title = myFile.name + " distribution"
            new_dic_x_p, new_dic_y_p = ut.make_text_distribution_poter(content)
            title_p = myFile.name + " distribution by poter algorithm"

            display_list = []
            length = len(new_dic_x)
            for i in range(0, length):
                display = {}
                if i < len(new_dic_x_p):
                    display['key'] = new_dic_x[i]
                    display['value'] = new_dic_y[i]
                    display['key_p'] = new_dic_x_p[i]
                    display['value_p'] = new_dic_y_p[i]
                else:
                    display['key'] = new_dic_x[i]
                    display['value'] = new_dic_y[i]
                    display['key_p'] = ''
                    display['value_p'] = ''
                display['row'] = i + 1
                display_list.append(display)

            return render(request, "ft_retriver/whole.html", locals())
        else:
            status = 'error'
            return render(request, "ft_retriver/whole.html", locals())
    else:
        status = 'none'
        return render(request, "ft_retriver/whole.html", locals())


def upload_file(request):
    if request.method == "POST":
        myFile = request.FILES.get("myfile", None)
        if not myFile:
            return redirect('../hello')
        elif ut.check_xml(myFile.name):
            # print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
            # return render(request, "ft_retriver/status.html", locals())
            return render(request, "ft_retriver/result2.html", locals())
        elif ut.check_json(myFile.name):
            destination = open(os.path.join("./files", myFile.name), 'wb+')
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
            # return render(request, "ft_retriver/status.html", locals())
            return render(request, "ft_retriver/result2.html", locals())
        else:
            status = 'FAILED!'
            information = 'Your file is not a xml/json file.'
            url = '../hello'
            button_content = 'BACK'
            # return render(request, "ft_retriver/status.html", locals())
            return render(request, "ft_retriver/result2.html", locals())


def xml_deal(request):
    print(request.POST['keyword'])
    print(request.POST['file_name'])
    print(request.POST['statusParse'])
    file_name = request.POST['file_name']
    statusParse = request.POST['statusParse']
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(BASE_DIR)
    path = os.path.join(BASE_DIR, "./files/" + file_name)
    upload_file_type = 'xml'
    cheacker = request.POST['keyword'].find(',')
    if cheacker != -1:
        keyword = request.POST['keyword']
        keywords = request.POST['keyword'].split(',')
        articalset_b = get_artical_set_xml(path, keywords[0], 5)
        articalset_a = get_artical_set_xml(path, keywords[1], 5)
        sr = same_rate(articalset_b, articalset_a)
        return render(request, "ft_retriver/result_sep.html", locals())
        # 表示有兩個關鍵字，要分兩邊
    else:
        # 表示跟原來的依樣
        keyword = request.POST['keyword']
        if not ut.check_file_exist(path):
            return render(request, "ft_retriver/status.html", ut.deal_failed())
        else:
            artical_set = []
            title = []
            content = []
            title, content = ps.parse_xml_abstract_title(path)
            ut.make_a_dictionary(content)
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
                    artical['wordset_p'] = ps.wordset_by_poter(content[i])
                    artical['common'] = wheather_important_words(artical['wordset'])
                    artical['words'], artical['value'] = ps.zipf_picture_data(artical['wordset'])
                    artical['words_p'], artical['value_p'] = ps.zipf_picture_data(artical['wordset_p'])
                    artical['ca_id_xml'] = 'ca_id_xml_' + str(i)
                    artical['ca_id_xml_p'] = 'ca_id_xml_p_' + str(i)

                    artical['wordset_len'] = len(artical['wordset'])
                    artical['wordset_p_len'] = len(artical['wordset_p'])
                    artical['len_id_xml'] = 'len_id_xml' + str(i)

                    display_list = []
                    length = len(artical['words'])
                    for j in range(0, length):
                        display = {}
                        if i < len(artical['words_p']):
                            display['key'] = artical['words'][j]
                            display['value'] = artical['value'][j]
                            display['key_p'] = artical['words_p'][j]
                            display['value_p'] = artical['value_p'][j]
                        else:
                            display['key'] = artical['words'][j]
                            display['value'] = artical['value'][j]
                            display['key_p'] = ''
                            display['value_p'] = ''
                        display['row'] = j + 1
                        display_list.append(display)
                    artical['display_list'] = display_list

                    artical_set.append(artical)
            hit = len(artical_set)
            # needToFix = 'no!'
            if (hit != 0):
                return render(request, "ft_retriver/result3.html", locals())
            else:
                hit = 0
                newkeyword = ed.fix_wrong_input(keyword)
                url = '../xml/'
                file_name = file_name
                statusParse = statusParse
                return render(request, "ft_retriver/redirect.html", locals())


def json_deal(request):
    file_name = request.POST['file_name']
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "./files/" + file_name)
    keyword = request.POST['keyword']
    type = 'json'

    if not ut.check_file_exist(path):
        return render(request, "ft_retriver/status.html", ut.deal_failed())
    else:
        json_obj = js.load_json_from_file(path)
        content, user = js.get_text_from_json_object(json_obj)
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
                artical['wordset'], artical['word_content'] = ps.count_words(content[i])
                artical['sentence_content'] = ps.count_sentence2(content[i])

                artical['keyword_content_hit'] = len(artical['located_content'])

                artical['content'] = ut.mark_string(content[i], keyword)
                print(artical['content'])
                artical['tag'] = ut.sperate_tag(content[i])
                artical['http'] = ut.sperate_http(content[i])
                artical['id'] = 'id' + str(i)
                # print(type(content[i]))
                if len(user) != 0:
                    artical['title'] = "這是第 " + str(count) + "篇含有關鍵字的推文，來自author_id: " + str(user[i])
                else:
                    artical['title'] = "這是第 " + str(count) + "篇含有關鍵字的推文"
                count += 1

                artical['common'] = wheather_important_words(artical['wordset'])
                artical['words'], artical['value'] = ps.zipf_picture_data(artical['wordset'])
                # artical['a'] = sperate_tag(content[i])
                # print(type(content[i]))
                artical['wordset_p'] = ps.wordset_by_poter(content[i])
                artical['words_p'], artical['value_p'] = ps.zipf_picture_data(artical['wordset_p'])
                artical['ca_id_json'] = 'ca_id_json_' + str(i)
                artical['ca_id_json_p'] = 'ca_id_json_p_' + str(i)

                artical['wordset_len'] = len(artical['wordset'])
                artical['wordset_p_len'] = len(artical['wordset_p'])
                artical['len_id_json'] = 'len_id_json' + str(i)

                display_list = []
                length = len(artical['words_p'])
                for j in range(0, length):
                    display = {}
                    if i < len(artical['words_p']):
                        display['key'] = artical['words'][j]
                        display['value'] = artical['value'][j]
                        display['key_p'] = artical['words_p'][j]
                        display['value_p'] = artical['value_p'][j]
                    else:
                        display['key'] = artical['words'][j]
                        display['value'] = artical['value'][j]
                        display['key_p'] = ''
                        display['value_p'] = ''
                    display['row'] = j + 1
                    display_list.append(display)
                artical['display_list'] = display_list

                artical_set.append(artical)
        hit = len(artical_set)
        if (hit != 0):
            return render(request, "ft_retriver/result3.html", locals())
        else:
            hit = 0
            newkeyword = ed.fix_wrong_input(keyword)
            url = '../json/'
            file_name = file_name
            # statusParse = statusParse
            return render(request, "ft_retriver/redirect.html", locals())


def getCompare(request):
    print(request.POST['keyword'])
    print(request.POST['file_name'])
    print(request.POST['statusParse'])
    file_name = request.POST['file_name']
    statusParse = request.POST['statusParse']
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "./files/" + file_name)
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
                artical['wordset'], artical['word_content'] = ps.count_words(content[i])
                artical['sentence_content'] = ps.count_sentence2(content[i])

                artical['keyword_title_hit'] = len(artical['located_title'])
                artical['keyword_content_hit'] = len(artical['located_content'])

                artical['title'] = ut.mark_string(title[i], keyword)
                artical['content'] = ut.mark_string(content[i], keyword)

                artical['id'] = 'id_' + str(i)

                artical_setA.append(artical)
        hitA = len(artical_setA)
        return render(request, "ft_retriver/result3.html", locals())


def tf_idf_auto(request):
    if request.method == "POST":
        status = 'filein'
        myFile = request.FILES.get("myfile", None)
        if not myFile :
            return redirect('../tf_idf/')
        elif ut.check_xml(myFile.name):
            destination = open(os.path.join("./files", myFile.name), 'wb+')
            for chunk in myFile.chunks():
                destination.write(chunk)
            destination.close()

            file_name = myFile.name
            titles, contents = ti.parse_xml_abstract_title('./files/' + myFile.name)
            artical_set = []
            title = []
            content = []



            print("----Merge Start----")
            contents = ti.merge_contents_titles(titles, contents)
            print("----Merge finished----")

            print("----Delete stop words in every artical and remove numbers Start----")
            contents_clean_wordset = ti.filter_to_clean_wordset(contents)
            print("----Delete stop words in every artical and remove numbers finished----")

            print("----Count numbers of every artical start----")
            contents_words_after_count = ti.count_words_in_one_document(contents_clean_wordset)
            print("----Count numbers of every artical finished----")


            #最多算50篇就好
            if len(titles) > 50:
                limit = 50
            else:
                limit = len(titles)


            for i in range(0,limit):

                artical = {}
                artical['title'] = titles[i]
                artical['content'] = contents[i]
                artical['id'] = 'id_' + str(i)

                keyword_set = titles[i] + contents[i]
                word_list = nltk.word_tokenize(keyword_set)
                filtered_words = [word.lower() for word in word_list if
                                  word.lower() not in stopwords.words('english') and word.isalpha()]
                filtered_words_count = Counter(filtered_words).most_common()

                numbers_of_words_in_this_doc = sum(Counter(filtered_words_count).values())
                tf_idf_list = []
                for one_word in filtered_words_count:
                    keyword = one_word[0]
                    numbers_of_keyword_in_this_doc = one_word[1]
                    tf = numbers_of_keyword_in_this_doc / numbers_of_words_in_this_doc
                    idf = ti.count_idf(keyword, contents_clean_wordset)
                    tf_idf_with_keyword = (keyword, tf * idf)
                    tf_idf_list.append(tf_idf_with_keyword)

                sorted_tfidf_importance = []
                sorted_tfidf_importance = sorted(tf_idf_list, key=lambda tup: tup[1])
                sorted_tfidf_importance.reverse()
                pro_keyword = sorted_tfidf_importance[0:5]
                artical['keyword'] = []
                for item in pro_keyword:
                    artical['keyword'].append("<span style=\"color:red;\">[TF-IDF = "+str(round(item[1],5))+" ] </span>"+ item[0])

                artical_set.append(artical)
            return render(request, "ft_retriver/tf_idf_auto.html", locals())
        else:
            status='missing something'
            return render(request, "ft_retriver/tf_idf_auto.html", locals())
    else:
        status = 'none'
        return render(request, "ft_retriver/tf_idf_auto.html", locals())

def tf_idf(request):
    if request.method == "POST":
        status = 'filein'
        keyword = 'notfound'
        keyword = request.POST['keyword']
        version = 'notfound'
        version = request.POST['tf_idf_version']
        myFile = request.FILES.get("myfile", None)
        if not myFile or keyword == 'notfound' or version == 'notfound':
            return redirect('../tf_idf/')
        elif ut.check_xml(myFile.name) and keyword != 'notfound' and version != 'notfound':
            destination = open(os.path.join("./files", myFile.name), 'wb+')
            for chunk in myFile.chunks():
                destination.write(chunk)
            destination.close()

            file_name = myFile.name
            titles, contents = ti.parse_xml_abstract_title('./files/' + myFile.name)
            artical_set = []
            title = []
            content = []
            numbers = len(title)

            print(len(titles))

            print("----Merge Start----")
            contents = ti.merge_contents_titles(titles, contents)
            print("----Merge finished----")

            print("----Delete stop words in every artical and remove numbers Start----")
            contents_clean_wordset = ti.filter_to_clean_wordset(contents)
            print("----Delete stop words in every artical and remove numbers finished----")

            print("----Count numbers of every artical start----")
            contents_words_after_count = ti.count_words_in_one_document(contents_clean_wordset)
            print("----Count numbers of every artical finished----")

            idf = ti.count_idf(keyword, contents_clean_wordset)

            if version == "v1":
                tf_idf_list = []
                tf_list = []
                tf_list = ti.count_tf(keyword, contents_words_after_count)
                for index in range(0, len(tf_list)):
                    tf_idf = tf_list[index] * idf
                    tf_idf_with_index = (tf_idf, index)
                    tf_idf_list.append(tf_idf_with_index)
                sorted_tf_idf_list = []
                sorted_tf_idf_list = sorted(tf_idf_list, key=lambda tup: tup[0])
                sorted_tf_idf_list.reverse()
            elif version == "v2":
                tf_idf_list = []
                tf_list = []
                tf_list = ti.tf_raw_count(keyword, contents_words_after_count)
                for index in range(0, len(tf_list)):
                    tf_idf = ti.tf_logarithm(tf_list[index]) * idf
                    tf_idf_with_index = (tf_idf, index)
                    tf_idf_list.append(tf_idf_with_index)
                sorted_tf_idf_list = []
                sorted_tf_idf_list = sorted(tf_idf_list, key=lambda tup: tup[0])
                sorted_tf_idf_list.reverse()
            elif version == "v3":
                tf_idf_list = []
                tf_list = []
                tf_list = ti.tf_double_k_normalization(keyword, contents_words_after_count, 0.5)
                for index in range(0, len(tf_list)):
                    tf_idf = tf_list[index] * idf
                    tf_idf_with_index = (tf_idf, index)
                    tf_idf_list.append(tf_idf_with_index)
                sorted_tf_idf_list = []
                sorted_tf_idf_list = sorted(tf_idf_list, key=lambda tup: tup[0])
                sorted_tf_idf_list.reverse()

            #count cosine similarity
            print("----Cosine Similarity initialize----")
            corpus = ti.merge_contents_titles(titles, contents)
            vectorizer = CountVectorizer(min_df=1)
            X = vectorizer.fit_transform(corpus)
            feature_name = vectorizer.get_feature_names()

            A = X.toarray()
            A_sparse = sparse.csr_matrix(A)
            similarities = cosine_similarity(A_sparse)
            print("----Cosine Similarity initialize finished----")


            for content_index in sorted_tf_idf_list:
                #print(content_index[0])
                print(content_index)
                i = content_index[1]
                score = content_index[0]
                print(score)
                artical = {}
                artical['status_title'], artical['located_title'] = ps.located_keyword(keyword, titles[i])
                artical['status_content'], artical['located_content'] = ps.located_keyword(keyword, contents[i])

                if artical['status_title'] == True or artical['status_content'] == True:
                    # 有重再全算
                    artical['character_content'] = ps.count_character(contents[i])
                    artical['wordset'], artical['word_content'] = ps.count_words(contents[i])
                    artical['sentence_content'] = ps.count_sentence2(contents[i])
                    artical['title'] = ut.mark_string(titles[i], keyword)
                    artical['content'] = ut.mark_string(contents[i], keyword)

                    artical['tf_idf'] = content_index[0]
                    artical['tf_idf_about'] =round(content_index[0], 3)

                    artical['keyword_title_hit'] = len(artical['located_title'])
                    artical['keyword_content_hit'] = len(artical['located_content'])

                    artical['title'] = ut.mark_string(titles[i], keyword)
                    artical['content'] = ut.mark_string(contents[i], keyword)

                    artical['id'] = 'id_' + str(i)
                    artical['wordset_p'] = ps.wordset_by_poter(contents[i])
                    artical['common'] = wheather_important_words(artical['wordset'])
                    artical['wordset_len'] = len(artical['wordset'])
                    artical['wordset_p_len'] = len(artical['wordset_p'])

                    relative_index = list(np.argsort(-similarities[i]))[1:6]
                    artical['relative_artical'] = []
                    artical['ra_simlarity'] = []

                    for k in relative_index:
                        print(k)
                        ra_string = "[Similarity:"+str(round(similarities[i][k], 3))+"] "+titles[k]
                        artical['relative_artical'].append(ra_string)


                    artical_set.append(artical)
            return render(request, "ft_retriver/tf_idf.html", locals())
        else:
            status='missing something'
            return render(request, "ft_retriver/tf_idf.html", locals())
    else:
        status = 'none'
        return render(request, "ft_retriver/tf_idf.html", locals())
