# coding: utf-8
# https://github.com/jsvine/pdfplumber

import pdfplumber
import re,os

def extract_page(page,tag):
    text = page.extract_text() #提所有文字
    print(text)
    createFile('anki.txt',number_string_rule(text),tag)

def createFile(path, result,tag):
    mode = 'w'
    if os.path.exists(path):
           mode = 'a'
    f = open(path, mode)    
    for name in result:
        f.write("*"+name)
        f.write('\n')
        f.write('**'+tag)
        f.write('\n\n')
    f.close()

def number_string_rule(content):
    data = list(filter(lambda s: re.match(r'\d+\.', s),content.split('\n')))
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
    pages = [1,4]
    tag = ''
    extract_content(file,pages,tag)