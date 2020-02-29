# coding: utf-8
import difflib
from html import HTML
import os

compare = {
    'old_dir':'E:\\front-blog\\python-tool\\diff\\new',
    'new_dir':'E:\\front-blog\\python-tool\\diff\\old'
}

def read_file(path):
    try:
        content = open(path, 'rb')
        text = content.read().splitlines()
        content.close()
        return text
    except IOError as error:
        print 'Read file Error: ' + str(error)

class Diff:
    def __init__(self,compare):
        self.old = {}
        self.new = {}
        self.old = self.read_dir_path(compare['old_dir'])
        self.new = self.read_dir_path(compare['new_dir'])
        self.html = HTML('html','')
        # 如果乱码改编码
        self.html.head('<meta charset="gbk">')

    def read_dir_path(self,dir):
        result = {}
        if os.path.isdir(dir):
            for (root, dirs, files) in os.walk(dir):
                for f in files:
                    full_path = root + '\\'+f
                    key = full_path.replace(dir, '')
                    result[key] = full_path
        return result

    def compare_file(self):
        body = self.html.body('')
        diff_keys = set(self.new.keys()) - set(self.old.keys())
        body.h1('多出的文件')
        for dif in diff_keys:
            body.p(dif)
        print diff_keys,'diff'
        same_keys = set(self.new.keys()) - diff_keys
        print same_keys, 'same'

        for item in same_keys:
            diff = difflib.HtmlDiff()
            body.div(diff.make_file(read_file(self.old[item]), read_file(self.new[item])))

        f = open('diffProjects.html', 'w')
        f.write(str(self.html).replace('&lt;','<').replace('&gt;','>'))
        f.close()


if __name__ == '__main__':
    Diff(compare).compare_file()