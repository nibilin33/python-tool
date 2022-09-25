# coding: utf-8
from turtle import rt
import pdfcrowd
import sys
from requests_html import HTMLSession

# document: https://requests.readthedocs.io/projects/requests-html/en/latest/

# english digest: https://mp.weixin.qq.com/s/JdtaFknT4FBYTBIZM4BqAw

rule_map = {
    'link': 1,
    'li': 2
}
session = HTMLSession()
SAVE_PATH = '/Users/nibl/Desktop/雅思学习/作文备考/跟着外刊学写作/'

def analyseRule(url='',type=1):
    r = session.get(url)
    # 滚动加载处理
    r.html.render(scrolldown=5,sleep=2)
    if rule_map['link'] == type:
        return r.html.absolute_links
    if rule_map['li'] == type:
        def get_link(it):
            return it.attrs['data-link']
        result = map(get_link,r.html.find('li.album__list-item'))
        return list(result)


def analyseHtml(url,type=1):
    links = analyseRule(url,type)
    # asysession = AsyncHTMLSession()
    print('total length:'+ str(len(links)))
    for item in links:
        # find class name 'rich_media_title' or id '#activity-name'
        item_view = session.get(item)
        title_result = item_view.html.search('<h1 class="rich_media_title " id="activity-name">{}</h1>')
        if title_result is not None:
            title = title_result[0].strip()
            print(item,title)
            createPdf(item,title)
            

def createPdf(url,filename):
    try:
        # create the API client instance
        client = pdfcrowd.HtmlToPdfClient('nibilin33', 'c924b725c175f0069056faafee7fe78f')
         # run the conversion and write the result to a file
        print('start save '+ filename)
        client.convertUrlToFile(url, SAVE_PATH+filename+'.pdf')
    except pdfcrowd.Error as why:
    # report the error
        sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))


if __name__ ==  '__main__':
    # ana_url = 'https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI2MDYzNjQ2MA==&action=getalbum&album_id=1747213984925057027&scene=173&from_msgid=2247499658&from_itemidx=1&count=3&nolastread=1&devicetype=iOS15.2&version=18001a2f&lang=zh_CN&nettype=WIFI&ascene=78&fontScale=100&wx_header=3'
    work_list = [
        # 'https://mp.weixin.qq.com/mp/homepage?__biz=Mzg5MDA5Mzk0MQ==&hid=5&sn=4e77f0a0c22a165a643fc7e9e1527e29&scene=18&devicetype=iOS15.2&version=18001a2f&lang=zh_CN&nettype=WIFI&ascene=7&session_us=gh_1bc7b3947244&fontScale=100&wx_header=3',
        'https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI2MDYzNjQ2MA==&action=getalbum&album_id=2467381321611558912&scene=173&from_msgid=2247500859&from_itemidx=1&count=3&nolastread=1#wechat_redirect',
        'http://mp.weixin.qq.com/mp/homepage?__biz=MzI2MDYzNjQ2MA==&hid=5&sn=434d2fc9f419ea35328fdc38403a425e&scene=18#wechat_redirect'
    ]
    for ana_url in work_list:
        analyseHtml(ana_url,1)


