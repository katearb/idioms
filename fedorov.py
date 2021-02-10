import re
import os
import json


def clean(text) -> str:
    return re.sub(r"(\[.*?])| | |(\\u2003)|\t|\n|\\|{|}|—{2,}|(\.  )|( \.)|\[']|\[/']", '', text)


def clean_source(source):
    return re.sub(r"\\|\[|\)\.?|(—?\[? *?\()|(\\u2003)", '', source)


def parse_m1(line: str):
    x = {}
    t = line

    abbrObj = re.search(r'\[p\](.*)\[/p\]', t)
    if abbrObj:
        x['abbr'] = []
        for a in re.finditer(r'\[p\](.*?)\[/p\]', t):
            x['abbr'].append(a.group(1))
        t = re.sub(r'\[p\](.*)\[/p\]', '', t)
    roleObj = re.search(r'\[i\](.*)\[/i\]', t)
    if roleObj:
        x['role'] = []
        for a in re.finditer(r'\[i\](.*?)\[/i\]', t):
            x['role'].append(a.group(1))
        t = re.sub(r'\[i\](.*)\[/i\]', '', t)
    bObj = re.search(r'\[b\](.*)\[/b\]', t)
    if bObj:
        x['num'] = []
        for a in re.finditer(r'\[b\](.*?)\[/b\]', t):
            x['num'].append(a.group(1))
        t = re.sub(r'\[b\](.*)\[/b\]', '', t)

    res = re.search(r'\[m1\](?P<meaning>.*)\[/m\]', t)
    x['meaning'] = res.group('meaning')
    return x


def parse_m2(line: str):
    x = {}
    x['text'] = ''
    t = line
    roleObj = re.search(r'\[i\](.*)\[/i\]', t)
    if roleObj:
        for a in re.finditer(r'\[i\](.*?)\[/i\]', t):
            x['text'] += clean(a.group(1))
        t = re.sub(r'\[i\](.*)\[/i\]', '', t)
    # '\t[m2]\u2003 (В. Астафьев. Сон о белых горах).[/m]
    sourceObj = re.search(r'\[m2\](.*)\[/m\]', t)
    if sourceObj:
        x['source'] = clean_source(sourceObj.group(1).strip())
    else:
        x['source'] = clean_source(t)
    return x


def transform_idiom_description_to_dictionary(idiom_description_list: list):
    current_element = {}
    current_element['phrase'], current_element['semantics'] = [], []
    semantic_element = {}
    for line in idiom_description_list:
        if line.startswith('\t'):
            if line.strip().startswith('[m1]'):
                if line.strip() == "[m1] [/m]":
                    continue
                if semantic_element and any(semantic_element.values()):
                    if not semantic_element.get('dictionary', 0):
                        semantic_element['dictionary'] = 'Fedorov'
                    current_element['semantics'].append(semantic_element)
                    semantic_element = {}
                semantic_element['examples'] = []
                res = parse_m1(line.strip())
                if 'abbr' in res:
                    semantic_element['abbr'] = res['abbr']
                if 'meaning' in res:
                    if res['meaning'].startswith('— '):
                        semantic_element['source'] = clean(res['meaning'].strip())
                    else:
                        semantic_element['meaning'] = clean(res['meaning'].strip())
                if 'role' in res:
                    semantic_element['role'] = res['role']
            elif line.strip().startswith('[m2]'):
                try:
                    semantic_element['examples'].append(parse_m2(line))
                except KeyError:
                    semantic_element['examples'] = [] #TODO: Fix this dirty hack
        else:
            current_element['phrase'].append(clean(line.strip()))
    semantic_element['dictionary'] = 'Fedorov'
    current_element['semantics'].append(semantic_element)
    return current_element


#print(os.getcwd())
# dsl_fname = os.path.join('DSLDictionary', 'fedorov.dsl')
dsl_dictionary = open('fedorov.dsl', 'r', encoding='utf-8')

idioms_lists = []
current_idiom_description = []
new_idiom_indicator = False

for line_index, line in enumerate(dsl_dictionary):
    if line.startswith('\t'):
        current_idiom_description.append(line)
        new_idiom_indicator = True
    else:
        if new_idiom_indicator:
            #idioms_lists.append(current_idiom_description)
            idioms_lists.append(transform_idiom_description_to_dictionary(current_idiom_description))
            #print(transform_idiom_description_to_dictionary(current_idiom_description))
            current_idiom_description = []
            new_idiom_indicator = False
        current_idiom_description.append(line)



#os.remove('idioms.json')
with open('fedorov.json', 'w', encoding='utf8') as fp:
    json.dump(idioms_lists, fp, ensure_ascii=False, indent=4)