import re
import json


def find_examples(article):

    for a in re.finditer(r'\[ex]\[lang id=1049](.*)\[/lang]\[/i]', article):
        text = re.search(r'\[ex]\[lang id=1049](.*)\[i]\(', a.group()).group().replace('[/i]', '')
        text = text.replace('1049', '')
        source = re.search(r'\[i](.*)\[/lang]', a.group()).group()
        text_example = re.sub('[^А-Яа-я- .,ё!?0-9]', '', text).strip()
        source_example = re.sub('[^А-Яа-я- .,ё!?0-9]', '', source)

    return text_example, source_example


dsl_dictionary = open('kveselevich.dsl', 'r', encoding='utf-8')

idioms_lists = []
with open('abbrs.txt', encoding='utf-8') as abbrs:
    abbr_list = list(map(lambda x: x[:-1], abbrs.readlines()[::2]))


def clean(text: str) -> str:
    return re.sub(r"(\[.*?]|\(|\))|({\[/?']})", '', text).strip()


def get_phrase_and_semantics(line, full_dict):
    text = re.search(r'\[com]\(\[i]\[lang id=1049](.*?)\[/m]', line.group()).group()
    text_double = text.split('[/i]')
    for ind_elem, elem in enumerate(text_double):
        if 'тж.' in elem:
            more_phrase = text_double[ind_elem + 1].split('[com]([i][lang id=1049]')

            full_dict['phrase'].append(clean(more_phrase[0]))
            if len(more_phrase) > 1:
                full_dict['semantics'][0]['role'].append(clean(more_phrase[1]))

    return [clean(element) for element in text_double if clean(element)]


for article_index, article in enumerate(dsl_dictionary.read().split('\n\n')[1:]):
    article_lines = [article_line for article_line in article.split('\n') if '[ref]' not in article_line]
    if len(article_lines) == 1:
        continue
    full_dict = dict(phrase=[clean(article_lines[0])], semantics=[{'dictionary': 'Kveselevich', 'role': [], 'meaning': '', 'abbr': [], 'examples': []}])

    if '[ex][lang id=1049]' in article:
        text_example, source_example = find_examples(article)
        full_dict['semantics'][0]['examples'].append({'text': text_example, 'source': source_example})

    full_dict['semantics'][0]['abbr'] = [abbr for abbr in abbr_list if ']'+abbr in article]

    if '[com]([i][lang id=1049]' in article:
        for line in re.finditer(r'\[com]\(\[i]\[lang id=1049](.*?)\[/m]', article):
            author = re.search(r'\[com]\(\[i]\[lang id=1049](приписывается )?[А-Я](.*?)\[/m]', line.group())
            if author is not None:
                continue

            text_clean = get_phrase_and_semantics(line, full_dict)

            if len(text_clean) == 1 or \
                    (len(text_clean) > 2 and not any([re.match(r'(.*?)[a-z]', elem) for elem in text_clean])):
                full_dict['semantics'][0]['role'].append(text_clean[0])
            else:
                full_dict['semantics'][0]['meaning'] = text_clean[0]

    idioms_lists.append(full_dict)

for idiom in idioms_lists:
    pass
    # print(idiom)

with open('kveselevich.json', 'w', encoding='utf8') as fp:
    json.dump(idioms_lists, fp, ensure_ascii=False, indent=4)
