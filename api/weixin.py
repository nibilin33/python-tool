from selenium import webdriver
from bs4 import BeautifulSoup
import os
from time import sleep
import xlwt
cpath = os.getcwd()+'\\lib\\phantomjs.exe'

def createExcel(list):
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('sheetname')
    row0 = ['api','URL']
    for i in range(0, len(row0)):
        sheet.write(1, i, row0[i])
    for i in range(0,len(list)):
        sheet.write(i+2, 0, list[i]['api'])
        full = 'https://developers.weixin.qq.com/miniprogram/dev/api/'+list[i]['url']
        sheet.write(i+2, 1, xlwt.Formula('HYPERLINK("'+full+'";"'+list[i]['url']+'")'))
    book.save('weixin.xls')

def getAPI():
    browser = webdriver.PhantomJS(cpath)
    browser.get('https://developers.weixin.qq.com/miniprogram/dev/api/')
    sleep(3)
    the_page = BeautifulSoup(browser.page_source, 'html.parser')
    browser.close()
    browser.quit()
    urls = the_page.find_all('div','table-wrp')
    result = {}
    for tb in urls:
        all_link = tb.find_all('a')
        for link in all_link:
            key = link.get_text()
            result[key] = link.get('href')
    list = []
    for key in result:
        list.append({'api':key,'url':result[key]})
    createExcel(list)

if __name__=='__main__':
    getAPI()
