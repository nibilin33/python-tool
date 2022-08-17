# coding: utf-8
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
        client = pdfcrowd.HtmlToPdfClient('demo', 'ce544b6ea52a5621fb9d55f8b542d14d')
         # run the conversion and write the result to a file
        print('start save '+ filename)
        client.convertUrlToFile(url, SAVE_PATH+filename+'.pdf')
    except pdfcrowd.Error as why:
    # report the error
        sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))


if __name__ ==  '__main__':
    ana_url = 'https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI2MDYzNjQ2MA==&action=getalbum&album_id=1747213984925057027&scene=173&from_msgid=2247499658&from_itemidx=1&count=3&nolastread=1&devicetype=iOS15.2&version=18001a2f&lang=zh_CN&nettype=WIFI&ascene=78&fontScale=100&wx_header=3'
    analyseHtml(ana_url,2)


