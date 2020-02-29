# -*- coding: UTF-8 -*-
import zerorpc
import urllib
import urllib2
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import sys
import os
from time import sleep
import zipfile
from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
from string import Template
pUrl = 'https://github.com/nibilin33/frontTool/archive/master.zip'
cpath = os.getcwd()+'\\lib\\phantomjs.exe'

def unzip_file(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        print('This is not zip')

def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)
def updatePakage():
    print "downloading with urllib2"
    f = urllib2.urlopen(pUrl)
    data = f.read()
    with open(os.getcwd()+'my-tools.zip','wb') as codes:
        codes.write(data)
    # del_file(os.getcwd())
    # unzip_file(os.getcwd()+'my-tools.zip',os.getcwd())

def GetDesktopPath():
    return os.path.join(os.path.expanduser("~"), 'Desktop')

def getPage(obj):
    print 'getPage'
    url = obj['type']
    username = obj['name']
    passord = obj['region']
    browser = webdriver.PhantomJS(cpath)
    browser.get('http://gitlab.yealink.com/users/sign_in')
    userName = browser.find_element_by_id("username")
    if userName:
        userName.send_keys(username)
    else:
        sleep(2)
        userName = browser.find_element_by_id("username")
        userName.send_keys(username)
    password = browser.find_element_by_id('password')
    if passord:
        password.send_keys(passord)
    btn = browser.find_element_by_name('commit')
    btn.click()
    browser.get(url)
    sleep(3)
    the_page = BeautifulSoup(browser.page_source, 'html.parser')
    browser.close()
    browser.quit()
    urls = the_page.find_all('li', string=re.compile("/api"))
    result = {}
    cResult = {}
    for item in urls:
        meth = re.search(r'POST|GET|PUT|DELETE',
                         item.get_text(), re.IGNORECASE).group()
        m = re.search(r'\/api\/[\s\S]+', item.get_text()).group()
        constARR = m.split('/')
        constName = constARR[-2].capitalize()+'_'+constARR[-1].capitalize()
        print constName
        print constARR
        result[constName.upper()] = m
        cResult[meth+constName.upper()] = {'method': meth.lower(
        ), 'url': constName.upper(), 'fname': meth.lower()+constARR[-1].capitalize()}
    filename = urls[0].get_text().split('/')[-2]
    path = GetDesktopPath()+'\\'+filename+'.js'
    createFile(path, result)
    aPath = GetDesktopPath()+'\\api'+filename.capitalize()+'.js'
    createApi(aPath, cResult, result)
    return path


def createFile(path, result):
    f = open(path, 'w')
    for name in result:
        f.write("export const "+name+" = '" + str(result[name]) + "';")
        f.write('\n')
    f.close()


def createApi(path, cResult, result):
    f = open(path, 'w')
    f.write("import AjaxRequest from './fetchConfig/ajaxRequest';")
    f.write('\n')
    imPortData = ",\n ".join(result.keys())
    f.write("import { "+imPortData+" } from'@/constants/url-constants';")
    f.write('\n')
    f.write("const request = new AjaxRequest('');")
    f.write('\n')
    for name in cResult:
        mtName = cResult[name]['fname']
        f.write("export const "+mtName+" = (params, show = false, type) => request." +
                cResult[name]['method']+"("+cResult[name]['url']+", params, show, type);")
        f.write('\n')
    f.write('\n')

def createTemplate(obj):
    rules = obj['rules']
    values = obj['template']
    tem = Template(rules).safe_substitute(values)
    browser = webdriver.PhantomJS(cpath)
    browser.add_cookie(obj['cookie'])
    browser.get(obj['url'])
    sleep(3)

route_dict = {
    'getPage':getPage,
    'updatePakage':updatePakage,
    'createTemplate':createTemplate
}
class RPC(BaseHTTPRequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',#'*')
                        'authorization, Authorization, Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')
    def do_POST(self):
        #获取post提交的数据
        try:
            print self.path
            obj = self.rfile.read(int(self.headers['content-length']))
            obj = urllib.unquote(obj).decode("utf-8", 'ignore')
            self.send_response(200)
            # self.send_header("Content-type","application/json")
            self.end_headers()
            fn = ''.join(self.path.split('/api/'))
            buf = route_dict[fn](obj)
            self.wfile.write(buf)
        except:
            self.wfile.write('{ret:-1}')
    def do_GET(self):
        print self.path
        self.send_response(200)
        self.end_headers()
        fn = ''.join(self.path.split('/api/'))
        route_dict[fn]()
        self.wfile.write(self.path)
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(self.path)
    # def runScript(self,obj):
    #     #getPage(obj['type'], obj['name'], obj['region'])
    #     return obj


def StartServer():
    sever = HTTPServer(("",4242),RPC)
    print 'start server'
    sever.serve_forever()




if __name__=='__main__':
    StartServer()
# s = zerorpc.Server(RPC())
# s.bind("tcp://0.0.0.0:4242")
# s.run()

