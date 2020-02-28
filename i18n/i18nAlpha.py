# coding: utf-8

import urllib2
import urllib
import os
import re
import chardet
import hashlib
import json
import time
from config import *

api_time = 0
wait_time = 1


def internationalization(file_path):
    def get_label(html, label):
        if '</%s>' % label in html and '<%s' % label in html:
            return html[html.index('<%s' % label):html.index('</%s>' % label) + len(label) + 3]
        return None

    def translate(word):
        print word
        global api_time
        st_time = time.time()
        if st_time - api_time < wait_time:
            time.sleep(wait_time - st_time + api_time)
        word = word.encode('utf-8')
        url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
        md5 = hashlib.md5()
        md5.update(appid+word+salt+key)
        data = {
            'from': 'zh',
            'to': 'en',
            'q': word,
            'appid': appid,
            'salt': salt,
            'sign': md5.hexdigest(),
        }
        print(data)
        request = urllib2.Request(url, data=urllib.urlencode(data))
        response = urllib2.urlopen(request)
        api_time = time.time()
        if response.getcode() != 200:
            raise Exception('百度翻译API连接出错，错误代码：%s' % response.getcode())
        data = json.loads(response.read())
        if 'trans_result' not in data:
            raise Exception('请求被拒绝，错误代码：%s，错误信息：%s' % (data[u'error_code'], data[u'error_msg']))
        word = data['trans_result'][0]['dst'].split(' ')

        module, file_name = os.path.split(file_path)
        module = os.path.split(module)[1]
        if len(word) == 1:
            return '%s.%s.%s' % (module, file_name, word[0].lower())

        return '%s.%s.%s' % (module, file_name, ''.join([w[0].lower() if len(w) > 0 else '' for w in word]))

    def to_js():
        js = "const i18n = {\n%s\n}\nmodule.exports = i18n"
        word = ',\n'.join(["'%s': '%s'" % (word_map[word], word) for word in word_map])
        return (js % word).encode('utf-8')

    def template_translate(template):
        lines = template.decode('utf-8')
        label = re.findall(u"([_\-\w]+=\s*'[\[\]`\"\s${}()._\w]*[\u4e00-\u9fff]+[[\s${}()\[\]._\w`\"]*[\u4e00-\u9fff\uFE30-\uFFA0]*[\s${}()\[\]._\w`\"]*]*')", lines)
        print label
        label += re.findall(u'([_\-\w]+=\s*"[\[\]`\'\s${}()._\w]*[\u4e00-\u9fff]+[[\s${}()\[\]._\w`\']*[\u4e00-\u9fff\uFE30-\uFFA0]*[\s${}()\[\]._\w`\"]*]*")', lines)
        for line in label:
            chinese = re.findall(u'\w*[\u4e00-\u9fff]+[\w+[\u4e00-\u9fff]*]*', line)
            tmp = line
            for w in chinese:
                if w not in word_map:
                    word_map[w] = translate(w)
                tmp = tmp.replace(w, "$t('%s')" % word_map[w])
            lines = lines.replace(u' %s' % line, " :" + tmp)
            lines = lines.replace(line, tmp)
        chinese = re.findall(u'(\w*[\u4e00-\u9fff]+([\s\uFE30-\uFFA0]*[\w\u4e00-\u9fff]+)*\w*)', lines)
        chinese = sorted(chinese, key=lambda c: len(c[0]), reverse=True)
        for line in chinese:
            line = line[0]
            if line not in word_map:
                word_map[line] = translate(line)
            lines = lines.replace(line, "{{$t('%s')}}" % word_map[line])
        lines = str(lines.encode('utf-8'))
        js = re.findall('\{\{.*?\}\}', template)
        js = list(set(js))
        for i in range(len(js)):
            lines = lines.replace(js[i], script_translate(js[i]))

        return lines

    def script_translate(script=None):
        res = ""
        len_script = len(script)

        exports = []    # 记录所有的export的起止下标
        start = 0
        tmp = re.findall('export\s+default', script)    # 找出所有的export
        for t in tmp:
            start += script[start:].index(t)    # 计算本次的起点
            now = start + script[start:].index('{')     # 记录本次最近的一个左括号位置
            if now < start or now + 1 >= len_script:
                # 最近的一个左括号的位置小于起点 或者 左括号已经是最后一个字符 则退出
                continue
            count = 1   # 未匹配的左括号数
            for i in range(now + 1, len_script):
                if script[i] == '}':
                    count -= 1  # 每一个右括号会匹配掉一个左括号
                    if count == 0:  # 未匹配的左括号数为0，表示本次export结束，记录起点和终点
                        exports.append([start, i])
                        start = i + 1
                        break
                elif script[i] == '{':
                    count += 1

        lines = script.split('\n')
        for line in lines:
            if chardet.detect(line)['encoding'] != 'utf-8':
                # 在编码为utf-8时，仅当出现非字母数字的字符时编码判断结果为utf-8。未出现中文，编码判断结果为ascii，直接合并结果。
                res += line + '\n'
                continue
            line = line.decode('utf-8')     # 解码为unicode，为正则判断做准备
            words = re.findall(u'[\'\"]', line)     # 找出所有的引号
            if len(words) < 2:  # 包围字符串的引号一定是2个及以上
                continue
            prev = None     # 用于记录前一个有效引号
            end = 0     # 记录最后一次处理字符串的位置
            res_len = len(res)  # 已合并的字符串长度，用于判断当前是否在export内
            for now in words:
                if not prev:
                    # 没有前一个有效引号的记录，则将当前引号记为有效引号
                    prev = now
                    continue
                if now != prev:
                    # 与前一个有效引号不同，则将当前引号是一个字符串里的引号，故跳过
                    continue
                start = end + line[end:].index(prev) + 1    # 找到当前起点位置， +1的目的是要将位置移动到引号之后
                end = start + line[start:].index(prev)  # 找到当前终点位置
                w = line[start: end]    # 提取出来的字符串
                if not re.match(u'[\u4e00-\u9fff]+', w):
                    continue
                if w not in word_map:
                    word_map[w] = translate(w)
                prev = None     # 初始化前一个有效引号的记录
                if reduce(lambda x, y: x + int(y[0] < res_len < y[1]), exports, 0):
                    # 判断是否在export里
                    line = line.replace(line[end] + w + line[end], "this.$t('%s')" % word_map[w])
                    # 字符串被替换，长度发生变化，更新终点的位置，避免计算的开始位置定位到一个已经处理的引号
                    end = start + len("this.$t('%s')" % word_map[w])
                else:
                    line = line.replace(line[end] + w + line[end], "t('%s')" % word_map[w])
                    end = start + len("t('%s')" % word_map[w])
            line = str(line.encode('utf-8'))
            res += line + '\n'
        return res

    in_file = file('%s.vue' % file_path).read()
    word_map = {}
    script_map = {}
    index = 0
    while True:
        old = get_label(in_file[index:], 'script')
        if not old:
            break
        new = script_translate(old)
        script_key = '<furongfeng_script_%d>' % len(script_map)
        script_map[script_key] = new
        in_file = in_file.replace(old, script_key)
        index += len(script_key)

    in_file = template_translate(in_file)

    for script_key in script_map:
        in_file = in_file.replace(script_key, script_map[script_key])

    # 可视化还原
    # for key in word_map:
    #     in_file = in_file.replace(word_map[key], str(key.encode('utf-8')))
    if len(word_map) > 0:
        open('%s_out.vue' % file_path, 'w').write(in_file)
        open('%s_out.js' % file_path, 'w').write(to_js())


if __name__ == '__main__':
    while True:
        local = raw_input('是否优先从项目I18N提取，请输入yes/no')
        if local.lower() == 'yes':
            dbName = raw_input('请输入项目名')
            if dbName:
                filePath = raw_input('请输入I18N路径')
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
                        internationalization(root + '\\' + f.replace('.vue', ''))
        elif os.path.isfile(path):
            if '.vue' in path:
                print path
                internationalization(path.replace('.vue', ''))
            else:
                print "%s 不是一个vue文件" % path
        else:
            print "请输入一个目录或者vue文件路径"