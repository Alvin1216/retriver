from ft_retriver.parser import xml_parser as ps
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path=os.path.join(BASE_DIR, "files\pubmed_fever_100.xml")
print(BASE_DIR)
print(path)
keyword = 'brca'
artical_set = []
title = []
content = []
title, content = ps.parse_xml_abstract_title(path)
numbers = len(title)
#print(title[0])
for i in range(0, numbers):
    print(i)
    artical = {}
    artical['title'] = title[i]
    artical['content'] = content[i]
    artical['character_content'] = ps.count_character(content[i])
    artical['word_content'] = ps.count_words(content[i])
    artical['sentence_content'] = ps.count_sentence(content[i])

    artical['status_title'], artical['located_title'] = ps.located_keyword(keyword, title[i])
    artical['status_content'], artical['located_content'] = ps.located_keyword(keyword, content[i])

    artical_set.append(artical)

print(len(artical_set))