# coding: utf-8
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import os
import time
import re
import sys
from createHtml import create_html
from googletrans import Translator
# reload(sys)
# sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()
api_time = 0
wait_time = 1
word_map = set()
def remove_black(str):
    return re.sub('\s+', '', str).strip()

def remove_nrt(str):
    return ''.join(str.split())

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        return
        print "Encountered a start tag:", tag, attrs

    def handle_data(self, data):
        data = remove_black(remove_nrt(data))
        if len(data):
            global word_map
            word_map.add(data)

class I18nTranslate:
    def __init__(self,file_path):
        self.word_translate = {}
        module, file_name = os.path.split(file_path)
        module = os.path.split(module)[1]
        self.module = module
        self.file_name = file_name
        self.file_path = file_path

    def get_word_translate(self):
        return self.word_translate

    def set_string(self,child,html_map):
        if hasattr(child, 'string') and child.string is not None:
            result = remove_black(remove_nrt(child.string))
            if len(result) and html_map.get(result) is not None:
                print html_map.get(result)
                child.string = '{{$t("' +html_map.get(result) + '")}}'

    def translate(self):
        with open(self.file_path) as fb:
            parse = MyHTMLParser()
            file_result = fb.read()
            parse.feed(file_result)
            for s in word_map:
                self.translate_api(s)
            html_map = {} # 生成.html
            js_map = {}
            for item in self.word_translate:
                filename = self.file_path.split('.')[0].split('/').pop()
                enkey = ''.join(self.word_translate[item].lower())[:20]
                key = remove_black(self.module+'.'+filename+'.'+enkey)
                html_map[item] = key
                js_map[key] = item
            create_html(html_map)
            soup = BeautifulSoup(file_result, 'html.parser')
            for child in soup.descendants:
                self.set_string(child,html_map)
            if len(html_map) > 0:
                open('%s_out.vue' % self.file_path.replace('.vue',''), 'w').write(soup.prettify().encode('utf-8'))
                open('%s_out.js' % self.file_path.replace('.vue', ''), 'w').write(self.to_js(js_map).encode('utf-8'))

    def to_js(self,word_map):
        js = "module.exports = {\n%s\n}\n"
        word = ',\n'.join(["'%s': '%s'" % (word_map[word].decode('utf-8'), word) for word in word_map])
        print (js % word)
        return (js % word)

    def translate_api(self,word):
        global api_time
        st_time = time.time() # 避免频率太高
        if st_time - api_time < wait_time:
            time.sleep(wait_time - st_time + api_time)
        translator = Translator(service_urls=[
              'translate.google.cn',
        ])
        translations = translator.translate([word], dest='en')
        for translation in translations:
            self.word_translate[remove_black(remove_nrt(translation.origin))] = translation.text
            print(translation.origin, ' -> ', translation.text)
        api_time = time.time()


if __name__ == '__main__':
    while True:
        path = raw_input('请输入待翻译的目录[输入exit退出]：')
        if path.lower() == 'exit':
            break
        if os.path.isdir(path):
            for (root, dirs, files) in os.walk(path):
                for f in files:
                    if '_out.vue' in f:
                        continue
                    if '.vue' in f:
                        print root + '\\' + f
                        I18nTranslate(root + '\\' + f).translate()
        elif os.path.isfile(path):
            if '.vue' in path:
                print path
                I18nTranslate(path).translate()
            else:
                print "%s 不是一个vue文件" % path
        else:
            print "请输入一个目录或者vue文件路径"