import json

with open("all_idioms.json", 'r', encoding='utf-8') as file:
    idioms = tuple(json.load(file))

unique = []
for phrase in idioms:
    dicts = [sem['dictionary'] for sem in phrase['semantics'] if 'dictionary' in sem]
    if len(dicts) == len(set(dicts)) and len(set(dicts)) > 1:
        unique.append(phrase)

print(len(unique))

with open('idioms_in_dicts.json', 'w', encoding='utf8') as fp:
    json.dump(unique, fp, ensure_ascii=False, indent=4)
