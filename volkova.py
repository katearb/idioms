import re
import json

dictionary_dsl = open('ru-ru_PhraseVolkova_1_0.dsl', 'r', encoding='utf-8').readlines()
# dictionary_dsl.close()

idioms_lists = []
full_dict = {'phrase': [], 'semantics': [{'role': [], 'meaning': '', 'abbr': [], 'example': []}]}
list_skip = ['перен', 'редко', 'с', 'поговорка', 'вводное слово', 'противоп', 'слова']


def clean(text) -> str:
    almost_clean = re.sub(r"(\[.*?(; )?])| | |\t|\n|►|\\|( , )", '', text)
    return re.sub(r"\( ?,?( )*?\)|\( \.\)|\(\.\)|( {2})", '', almost_clean).strip()


for ind, line in enumerate(dictionary_dsl):

    if re.match(r'\[b]\(?[А-Я]', line[6:]):
        idioms_lists.append(full_dict)
        full_dict = {'phrase': [], 'semantics': [{'role': [], 'meaning': '', 'abbr': [], 'examples': []}]}

        line_short = line[9:]

        if '[i]' in line_short:
            full_dict['semantics'][0]['role'].extend([clean(find)
                                                      for find in re.findall(r'\[i](.*?)\[/i]', line_short)
                                                      if 'или' not in clean(find) and 'в знач.' not in clean(find) and\
                                                      clean(find) not in list_skip])
            for role in re.findall(r'\[i](.*?)\[/i]', line_short):
                line_short = line_short.replace(role, '')

        if '[p]' in line_short:
            for find in re.findall(r'\[p](.*?)\[/p]', line_short):
                full_dict['semantics'][0]['abbr'].append(clean(find))
                line_short = line_short.replace(find, '')

        if '—' in line_short:
            phrase_mean = line_short.split(' — ')
            if len(phrase_mean) in [2, 3]:
                print(clean(phrase_mean[0]))
                full_dict['phrase'].append(clean(phrase_mean[0]))
                full_dict['semantics'][0]['meaning'] = clean(phrase_mean[-1])
        else:
            full_dict['phrase'].append(clean(line_short))

    elif line[6:].startswith('[b][c darkblue'):
        if full_dict['semantics'][-1]['meaning']:
            full_dict['semantics'].append({'role': [], 'meaning': '', 'abbr': [], 'examples': []})

        if '[i]' in line:
            full_dict['semantics'][-1]['role'].extend([clean(find)
                                                        for find in re.findall(r'\[i](.*?)\[/i]', line)
                                                        if 'или' not in clean(find) and \
                                                        clean(find) not in ['с', 'поговорка']])
            for role in full_dict['semantics'][-1]['role']:
                line = line.replace(role, '')

        if '[p]' in line:
            full_dict['semantics'][-1]['abbr'].extend(
                [clean(find) for find in re.findall(r'\[p](.*?)\[/p]', line)])
            for abbr in full_dict['semantics'][-1]['abbr']:
                line = line.replace(abbr, '')

        full_dict['semantics'][-1]['meaning'] = clean(line[23:])

    elif line[6:].startswith('[c darkviolet'):
        full_dict['semantics'][-1]['examples'].append(clean(line[6:]))

with open('volkova.json', 'w', encoding='utf8') as fp:
    json.dump(idioms_lists, fp, ensure_ascii=False, indent=4)
