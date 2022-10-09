# coding: utf-8
# https://github.com/jsvine/pdfplumber

import pdfplumber
import re,os

global_mode = 'dot'

def extract_page(page,tag):
    text = page.extract_text() #提所有文字
    createFile('anki.txt',text,tag)

def createFile(path, text,tag):
    if global_mode == 'dot':
        result = dot_string_rule(text)
    else:
        result = number_string_rule(text)
    mode = 'w'
    if os.path.exists(path):
           mode = 'a'
    f = open(path, mode)    
    for name in result:
        if global_mode == 'dot':
            format_dot(name,f)
        else:
            f.write("*"+name)
            f.write('\n')
            f.write('**'+tag)
            f.write('\n\n')
    f.close()

def format_dot(name,f):
    for item in name:
        if len(item) > 0:
            ch = re.findall('[\u4e00-\u9fa5]+',item)
            f.write("*"+''.join(ch))
            f.write('\n')
            f.write('**'+item)
            f.write('\n\n')

def number_string_rule(content):
    data = list(filter(lambda s: re.match(r'\d+\.', s),content.split('\n')))
    return data

def dot_string_rule(content):
    data = list(map(lambda name: re.split(r'\d+\.',name),list(filter(lambda s: re.match(r'\d+\.|\-\w+', s),content.split('\n')))))
    return data

def extract_content(file,pages,tag):
    if not os.path.exists(file):
        return
    with pdfplumber.open(file) as pdf:
        if len(pages) == 2:
            for i in range(pages[0],pages[1]+1):
                page = pdf.pages[i]
                extract_page(page,tag)
        elif len(pages) > 2 or len(pages) == 1:
            for i in pages:
                page = pdf.pages[i]
                extract_page(page,tag)
        else:
            for page in pdf.pages:
                extract_page(page,tag)

if __name__ ==  '__main__':
    file = ''
    pages = []
    tag = ''
    extract_content(file,pages,tag)