import json
import re

with open('fedosov.json', 'r', encoding='utf-8') as file:
    fedosov = json.load(file)
with open('kveselevich.json', 'r', encoding='utf-8') as file:
    kveselevich = json.load(file)
with open('myurrey.json', 'r', encoding='utf-8') as file:
    myurrey = json.load(file)
with open('volkova.json', 'r', encoding='utf-8') as file:
    volkova = json.load(file)
with open('fedorov.json', 'r', encoding='utf-8') as file:
    fedorov = json.load(file)


def leave_letters_only(phrase):
    return re.sub(r'[^а-я]', '', phrase.lower())


dict_abbrs = {}
style_phrase = {}
all_abbrs = []

key_dict = fedorov
style_phrase[key_dict[0]['semantics'][0]['dictionary']] = {'phrases': len(key_dict)}
all_phrases = set()
current_dict_left = set()
for phrase in key_dict:
    all_phrases.union(set([leave_letters_only(p) for p in phrase['phrase'] if len(leave_letters_only(p)) > 1]))
    '''    abbrs_here = sum([len(dic.get('abbr', [])) for dic in phrase['semantics']])
    dict_abbrs[phrase['semantics'][0]['dictionary']] = dict_abbrs.get(
        phrase['semantics'][0]['dictionary'], 0) + abbrs_here'''
    for sem in phrase['semantics']:
        if 'abbr' in sem.keys():
            all_abbrs.extend(sem['abbr'])

for dictionary in [fedosov, kveselevich, myurrey, volkova]:
    style_phrase[dictionary[0]['semantics'][0]['dictionary']] = {'phrases': len(dictionary)}

    for article in dictionary:
        for phrase in article['phrase']:
            if leave_letters_only(phrase) in all_phrases:
                for key_phrase in key_dict:
                    if leave_letters_only(phrase) in [leave_letters_only(p) for p in key_phrase['phrase']]:
                        key_phrase['semantics'].extend(article['semantics'])
                        abbrs_here = sum([len(dic.get('abbr', [])) for dic in article['semantics']])
                        dict_abbrs[article['semantics'][0]['dictionary']] = dict_abbrs.get(
                            article['semantics'][0]['dictionary'], 0) + abbrs_here
                        for sem in article['semantics']:
                            if 'abbr' in sem.keys():
                                all_abbrs.extend(sem['abbr'])
                        break

                break
        else:
            current_dict_left.union(set([leave_letters_only(phr) for phr in article['phrase']]))
            key_dict.append(article)
            abbrs_here = sum([len(dic.get('abbr', [])) for dic in article['semantics']])
            dict_abbrs[article['semantics'][0]['dictionary']] = dict_abbrs.get(
                article['semantics'][0]['dictionary'], 0) + abbrs_here
            for sem in article['semantics']:
                if 'abbr' in sem.keys():
                    all_abbrs.extend(sem['abbr'])

    all_phrases.union(current_dict_left)

for dic in dict_abbrs:
    style_phrase[dic]['abbrs'] = dict_abbrs[dic]
    print(dic, style_phrase[dic])

clean_abbrs = [ab for ab in list(set(all_abbrs)) if ab[-1] == '.']

with open('all_idioms.json', 'w', encoding='utf8') as fp:
    json.dump(key_dict, fp, ensure_ascii=False, indent=4)
