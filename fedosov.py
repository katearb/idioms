import json
import re

dsl_dictionary = open('fedosov.dsl', 'r', encoding='utf-8')
dictionary_lines = dsl_dictionary.readlines()[38:]

idioms_lists = []
idiom_dict = {'phrase': []}


def clean_phrase(phrase):
    return re.sub(r'(\[b])|(\[/b])|(\[p])|(\[/p])|(\n)|( и т\. п\.)', '', phrase[8:]).strip()


for line in dictionary_lines:
    if line.startswith('\t[m2]'):
        if idiom_dict['phrase']:
            idioms_lists.append(idiom_dict)

        idiom_dict = {'phrase': [], 'semantics': [{'role': [], 'meaning': '', 'abbr': [], 'examples': []}]}
        phrase_mean = line.split(' -')

        abbrs = re.findall(r'\[p](.*?)\[/p]', phrase_mean[0])
        for abbr in abbrs:
            idiom_dict['semantics'][-1]['abbr'].append(abbr)
            phrase_mean[0] = phrase_mean[0].replace('[p]' + abbr + '[/p]', '')

        find_role = phrase_mean[0].replace(')', '').split(']')
        if find_role[-1] in ['', ' ']:
            find_role = find_role[:-1]

        if find_role[-1][-1] != 'b':
            if 'и т. д.' in find_role[-1] or 'и т. п.' in find_role[-1] or '(' in find_role[-1] or \
                    not any([letter.isalpha() for letter in find_role[-1]]):
                pass
            else:
                idiom_dict['semantics'][0]['role'].append(find_role[-1])
                phrase_mean[0] = phrase_mean[0].replace(find_role[-1], '')

        idiom_dict['phrase'] = clean_phrase(phrase_mean[0])

        if phrase_mean[-1] != '\n' and phrase_mean[-1] != '\t' and \
                any([letter.isalpha() for letter in phrase_mean[-1]]):
            phrase_mean[-1] = re.sub(r'(\\t)|(\\n)', '', phrase_mean[-1])
            idiom_dict['semantics'][-1]['meaning'] = phrase_mean[-1][:-1]

    elif line.startswith('\t[m4]'):
        if idiom_dict['semantics'][-1]['meaning']:
            idiom_dict['semantics'].append({'role': [], 'meaning': '', 'abbr': [], 'examples': []})
        abbrs = re.findall(r'\[p](.*?)\[/p]', line)
        for abbr in abbrs:
            idiom_dict['semantics'][-1]['abbr'].append(abbr)
            line = line.replace(abbr, '')
            line = re.sub(r'(\[p])|(\[/p])|(\\t)', '', line)
        idiom_dict['semantics'][-1]['meaning'] = line.split('[/b] ')[-1][:-1]


with open('fedosov.json', 'w', encoding='utf8') as fp:
    json.dump(idioms_lists, fp, ensure_ascii=False, indent=4)
