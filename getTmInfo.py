#-*- coding: UTF-8 -*-
import sys,os,time
import json
import codecs
import json
import re
import requests
import pyodbc
from xml.dom.minidom import parse, parseString
import codecs
from selenium import webdriver
from tkinter import *
from tkinter import messagebox
import tkinter.messagebox
import importlib
import datetime
import random
from selenium.webdriver.common.keys import Keys
importlib.reload(sys)

#reload(sys)
#sys.setdefaultencoding('utf8')


def GetFileNameAndExt(filename):
    (filepath,tempfilename) = os.path.split(filename);
    (shotname,extension) = os.path.splitext(tempfilename);
    return shotname,extension
def getGuid():
    nowTime=datetime.datetime.now().strftime("%Y%m%d%H%M%S");#生成当前时间
    randomNum=random.randint(0,100);#生成的随机整数n，其中0<=n<=100
    if randomNum<=10:
      randomNum=str(0)+str(randomNum);
    uniqueNum=str(nowTime)+str(randomNum);
    return uniqueNum;
def cur_file_dir():
    path = sys.path[0]
    #pyinstaller打包解决方案   
    if getattr(sys, 'frozen', False):
        path = os.path.dirname(sys.executable)
    elif __file__:
        path = os.path.dirname(__file__)
    return path
    
def cur_file_dirxml():
    path = sys.path[0]
    #pyinstaller打包解决方案   
    if getattr(sys, 'frozen', False):
        path = os.path.dirname(sys.executable)
    elif __file__:
        path = os.path.dirname(__file__)
    path = path +  '\\config.xml'  
    return path
    
datasource = open(cur_file_dirxml(),'rb')
dom = parse(datasource)
root = dom.documentElement
# 数据库连接配置
defaultobj = root.getElementsByTagName('default')
datesource = defaultobj[0].getAttribute("value")
# 起始数据
jsonpathobj = root.getElementsByTagName('jsonpath')
start = jsonpathobj[0].getAttribute("value")

print(start)
print(strat+1000)

constr = datesource
conn = pyodbc.connect(constr, autocommit=True)
cur = conn.cursor()
url = 'http://tmsearch.uspto.gov/'
#模拟浏览器请求网站
driver = webdriver.Chrome()
res = driver.get(url)

str1=driver.current_url
str2=str1.replace("gate.exe?f=tess", "showfield?f=doc");
str2=str2.replace("1.1.1", "1.2.1");
str2=str2.replace("1.1", "2.1");
driver.find_element_by_link_text("Word and/or Design Mark Search (Structured)").click();
time.sleep(2)
driver.find_element_by_name("p_s_PARA1").send_keys("28.01.03")
driver.find_element_by_name("p_tagrepl~:").send_keys("Design Code")
time.sleep(2)
driver.find_element_by_name("a_search").click()
time.sleep(2)
print(str2)
urlnew=str2[ 0:str2.rindex( '.' ) + 1]

for i in  range(1,40000):
   print(i)
   try:
       guidStr=getGuid()
       js1="window.location.href='"+urlnew+str(i)+"'"
       driver.execute_script(js1)
       time.sleep(1)
       info=driver.find_element_by_xpath('/html/body/table[5]').get_attribute('innerHTML').replace('\n', '').replace('\r', '').replace('\'','\'\'')
       sql = "insert into [US].[dbo].[info](guid,info,i) values('"+guidStr+"','"+info+"','"+str(i)+"')"
       cur.execute(sql)
   except Exception as e:
       i=i+1
