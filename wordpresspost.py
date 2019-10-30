#coding: utf-8
import requests
import time
from lxml import etree
import io
import sys
import hashlib
import os

def Sessionrequests(getorpost ,Session,url,params,data):
    while True:  # 一直循环，知道访问站点成功
        if getorpost =="get":
            try:
                # 以下except都是用来捕获当requests请求出现异常时，
                # 通过捕获然后等待网络情况的变化，以此来保护程序的不间断运行
                response = Session.get(url, params=params, timeout=20)
                break
            except requests.exceptions.ConnectionError:
                print('ConnectionError -- please wait 3 seconds')
                time.sleep(3)
            except requests.exceptions.ChunkedEncodingError:
                print('ChunkedEncodingError -- please wait 3 seconds')
                time.sleep(3)
            except:
                print('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
                time.sleep(3)
        else:
            try:
                response = Session.post(url, params=params,data=data, timeout=20)
                break
            except requests.exceptions.ConnectionError:
                print('ConnectionError -- please wait 3 seconds')
                time.sleep(3)
            except requests.exceptions.ChunkedEncodingError:
                print('ChunkedEncodingError -- please wait 3 seconds')
                time.sleep(3)
            except:
                print('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
                time.sleep(3)
    return response
def w_file(filepath,content):
    with open(filepath,'wb') as wf:
        wf.write(content)
        wf.close()

if __name__ == "__main__":
    host = "网址/hm-locowp/hm-locowp.php"
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
    session = requests.session()
    os.system("echo 启动")
    with open('./mcweb/map.txt') as f:
        for line in f.readlines():
            response = Sessionrequests('get',session,line,"","")
            etreeobj = etree.HTML(response.text)
            os.system("echo "+line)
            try:
                resulttitle = etreeobj.xpath('//*[@id="primary"]/main/article/header/h1/text()')[0]
                resultimge = etreeobj.xpath('//*[@id="primary"]/main/article/div/div[1]//@src')
                resulttext = etreeobj.xpath('//*[@id="primary"]/main/article/div/div[1]')[0]
                conttext = etree.tostring(resulttext, pretty_print=True, method='html').decode('utf-8')
                for i in resultimge:
                    if i.endswith('.jpg'):
                        responseimg = Sessionrequests('get',session,i,"","")
                        md5obj = hashlib.md5()
                        md5obj.update(responseimg.content)
                        hash = md5obj.hexdigest()
                        conttext =conttext.replace(i,"http://imgs.ipedg.com/mcimg/"+hash+'.jpg')
                        w_file("./mcimg/"+hash+'.jpg',responseimg.content)
                    elif i.endswith('.png'):
                        responseimg = Sessionrequests('get',session,i,"","")
                        md5obj = hashlib.md5()
                        md5obj.update(responseimg.content)
                        hash = md5obj.hexdigest()
                        conttext =conttext.replace(i,"http://imgs.ipedg.com/mcimg/"+hash+'.png')
                        w_file("./mcimg/"+hash+'.png',responseimg.content)
                params={
                    'action':'save',
                    'secret':'asd59541511'
                }
                data={
                    'post_title':resulttitle,
                    'post_category':"2",
                    'tag':"",
                    'post_content':conttext
                }
                response = Sessionrequests('post',session,host,params,data)
                os.system("echo ok")
            except Exception as e:
                pass
    pass