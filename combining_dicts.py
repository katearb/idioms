import json

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

"""
fedosov = json.load(open('fedosov.json', 'r'))
kveselevich = json.load(open('kveselevich.json', 'r'))
myurrey = json.load(open('myurrey.json', 'r'))
volkova = json.load(open('volkova.json', 'r'))
durandin = json.load(open('fedorov.json', 'r'))
"""
# TODO: выделить автора в случаях типа "Сыграем еще партию сверх абонемента. Салтыков-Щедрин."
key_dict = volkova  # TODO: choose the main dict here
all_phrases = []
all_phrases.extend([phr['phrase'] for phr in key_dict])

for diction in [kveselevich, myurrey, fedosov]:
    for idiom in diction:
        if idiom['phrase'][0] not in all_phrases:   # all(elem in all_phrases for elem in phrase['phrase'])?? or empty?
            all_phrases.extend(idiom['phrase'])  # TODO: use .strip()
            key_dict.append(idiom)
            continue
        # {'phrase': [], 'semantics': [{'role': [], 'meaning': '', 'abbr': [], 'examples': []}]}
        for phrase in key_dict:
            if idiom['phrase'][0] in phrase['phrase']:
                phrase['semantics'].extend(idiom['semantics'])
                break

with open('all_idioms.json', 'w', encoding='utf8') as fp:
    json.dump(key_dict, fp, ensure_ascii=False, indent=4)
