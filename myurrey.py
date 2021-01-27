import json

dsl_dictionary = open('myurrey.dsl', 'r', encoding='utf-8')
dictionary_lines = dsl_dictionary.readlines()

idioms_lists = []
idiom_dict = {}
has_role = False

for line in dictionary_lines:
    if line[0] != '\t':
        has_role = False

        if idiom_dict:
            idioms_lists.append(idiom_dict)
            idiom_dict = {}

        if '{' in line:
            key_role = line.split('{')
        else:
            key_role = [line]

        if key_role[0][-1] == '\n':
            key_role[0] = key_role[0][:-1]

        idiom_dict['phrase'] = [key_role[0]]
        idiom_dict['semantics'] = [{'role': [], 'meaning': '', 'abbr': [], 'examples': []}]

        if len(key_role) == 2:
            idiom_dict['semantics'][-1]['role'].append(key_role[1][2:-3])
            has_role = True

    elif '[m0]' in line:
        if not has_role and (idiom_dict['semantics'][-1]['role'] or idiom_dict['semantics'][-1]['meaning']):
            idiom_dict['semantics'].append({'role': [], 'meaning': '', 'abbr': [], 'examples': []})
            has_role = False

        meaning = line.split('(')
        if len(meaning) > 2:
            idiom_dict['semantics'][-1]['role'].append(meaning[1][:-2])

        idiom_dict['semantics'][-1]['meaning'] = meaning[-1][:-12]

for idiom in idioms_lists:
    # print(idiom)
    pass

with open('myurrey.json', 'w', encoding='utf8') as fp:
    json.dump(idioms_lists, fp, ensure_ascii=False, indent=4)
