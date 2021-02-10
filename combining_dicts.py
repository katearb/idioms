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

num_abbrs = 0
dict_abbrs = {}

key_dict = fedorov
all_phrases = set()
current_dict_left = set()
for phrase in key_dict:
    all_phrases.union(set([leave_letters_only(p) for p in phrase['phrase'] if len(leave_letters_only(p)) > 1]))
    abbrs_here = sum([len(dic.get('abbr', [])) for dic in phrase['semantics']])
    dict_abbrs[phrase['semantics'][0]['dictionary']] = dict_abbrs.get(
        phrase['semantics'][0]['dictionary'], 0) + abbrs_here
    num_abbrs += abbrs_here

for dictionary in [fedosov, kveselevich, myurrey, volkova]:
    for article in dictionary:

        for phrase in article['phrase']:
            if leave_letters_only(phrase) in all_phrases:
                for key_phrase in key_dict:
                    if leave_letters_only(phrase) in [leave_letters_only(p) for p in key_phrase['phrase']]:
                        key_phrase['semantics'].extend(article['semantics'])
                        abbrs_here = sum([len(dic.get('abbr', [])) for dic in article['semantics']])
                        num_abbrs += abbrs_here
                        dict_abbrs[article['semantics'][0]['dictionary']] = dict_abbrs.get(
                            article['semantics'][0]['dictionary'], 0) + abbrs_here
                        break

                break
        else:
            current_dict_left.union(set([leave_letters_only(phr) for phr in article['phrase']]))
            key_dict.append(article)
            num_abbrs += sum([len(dic.get('abbr', [])) for dic in article['semantics']])
            dict_abbrs[article['semantics'][0]['dictionary']] = dict_abbrs.get(
                article['semantics'][0]['dictionary'], 0
            ) + len(article['semantics'][0].get('abbr', []))

    all_phrases.union(current_dict_left)

print(num_abbrs)
print(dict_abbrs)
with open('all_idioms.json', 'w', encoding='utf8') as fp:
    json.dump(key_dict, fp, ensure_ascii=False, indent=4)

