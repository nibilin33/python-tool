# coding: utf-8

from html import HTML

def create_html(data):
    h = HTML('html','')
    t = h.table(border='1')
    for it in data:
        r = t.tr
        r.td(it)
        r.td(data[it])
        r.td.input(value=data[it])
    h.button('完成')
    h.script(' function createCORSRequest(method, url) {'
             'var xhr = new XMLHttpRequest();'
             'if ("withCredentials" in xhr) {'
             'xhr.open(method, url, true);'
             ' } else if (typeof XDomainRequest != "undefined") {'
             'xhr = new XDomainRequest();'
             ' xhr.open(method, url);'
             '}'
             'return xhr;'
             '}'
             )
    h.script(' function getI18n() {'
             '}'
             )
    h.script('document.addEventListener("click",function(e){'
             'if(e.target.nodeName =="BUTTON"){'
             'var tr = document.querySelectorAll("tr");'
             'var result = {};'
             'for(var i=0;i < tr.length;i++){ '
             'var ch = tr[i].children;'
             'var key = ch[0].innerText;'
             'var value = ch[2].children[0].value;'
             'result[key] = value;'
             '}'
              'console.log(result);'
             'var url = "http://"+window.location.host+"/finish";'
             'var oreq = createCORSRequest("POST",url);'
              'oreq.setRequestHeader("content-type", "application/json;charset=utf-8");'
             'oreq.send(JSON.stringify(result));'
             'oreq.onload = function(e){'
             'if(oreq.status === 200 || oreq.status == 304){'
             'alert("操作成功,请关闭");'
             '}'
             '}'
             '}'
             '}'
             ')')
    sts = str(h).replace('&lt;','<')
    f = open('translate.html', 'w')
    f.write(sts)
    f.close()


