# coding: utf-8
import os
import re

def list_files(startpath):
    fs = open('STRUCTURE.md', 'w')
    for root, dirs, files in os.walk(startpath):
        if root.find('node_modules') < 0:
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            print('{}{}/'.format(indent, os.path.basename(root)))
            fs.write('{}{}/  '.format(indent, os.path.basename(root)))
            fs.write('\n')
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                if f.find('.js') > -1 or f.find('.vue') > -1:
                    fs.write('{}{}  '.format(subindent, f))
                    fs.write('\n')
                print('{}{}'.format(subindent, f))
    fs.close()

if __name__ ==  '__main__':
    raw = raw_input('请输入项目路径')
    list_files(raw)