# coding: utf-8
import pdfcrowd
import sys
from requests_html import HTMLSession

# document: https://requests.readthedocs.io/projects/requests-html/en/latest/

# english digest: https://mp.weixin.qq.com/s/JdtaFknT4FBYTBIZM4BqAw

def analyseHtml(url):
    session = HTMLSession()
    r = session.get(url)
    links = r.html.absolute_links
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
        client.convertUrlToFile(url, filename+'.pdf')
    except pdfcrowd.Error as why:
    # report the error
        sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))


if __name__ ==  '__main__':
    ana_url = 'https://mp.weixin.qq.com/s/JdtaFknT4FBYTBIZM4BqAw'
    analyseHtml(ana_url)


