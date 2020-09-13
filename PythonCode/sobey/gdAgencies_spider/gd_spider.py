import re
from bs4 import BeautifulSoup as bs4
import requests as req
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import lxml
import pymysql
import os
import sys
import datetime
import multiprocessing
import datetime
import time
from easysql import whereNotInsert

class spider:
    def __init__(self):
        pass

    def guangDong(self):
        url=urls[0]
        driver.get(url)
        if WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='glbox']"))):
            html = driver.page_source
            soup = bs4(html, 'lxml')
            temp=soup.find('div',class_="con LinkList").find_all('li')
        for i in temp:
            info = []
            name = i.get_text()
            info.append(name)
            info.append('广东省')
            info.append('')
            info.append(datetime.datetime.now().strftime('%Y-%m-%d'))
            info.append(url)
            sql = whereNotInsert.main(tablename, t_eventField, info, 'name', info[0])
            save2db().save2db(sql)

    def guangZhou(self):
        url = urls[1]
        driver.get(url)
        if WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='main_border SinglePage']"))):
            html = driver.page_source
            soup = bs4(html, 'lxml')
            temp = soup.find('div', class_="main_border SinglePage").find_all('td')
        print(len(temp))
        for i in temp:
            info=[]
            name = i.get_text().replace('· ','')
            info.append(name)
            info.append('广东省')
            info.append('广州')
            info.append(datetime.datetime.now().strftime('%Y-%m-%d'))
            info.append(url)
            sql = whereNotInsert.main(tablename, t_eventField, info, 'name', info[0])
            save2db().save2db(sql)

    def shenZhen(self):
        url = urls[2]
        driver.get(url)
        if WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='zx_xxgk_ml']"))):
            html = driver.page_source
            soup = bs4(html, 'lxml')
            temp = soup.find('div', class_="zx_xxgk_ml").find_all('li')
        print(len(temp))
        for i in temp:
            info=[]
            name = i.get_text().replace('· ','')
            info.append(name)
            info.append('广东省')
            info.append('深圳')
            info.append(datetime.datetime.now().strftime('%Y-%m-%d'))
            info.append(url)
            sql = whereNotInsert.main(tablename, t_eventField, info, 'name', info[0])
            save2db().save2db(sql)

    def zhuHai(self):
        url = urls[3]
        driver.get(url)
        if WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='gl-con']"))):
            html = driver.page_source
            soup = bs4(html, 'lxml')
            temp = soup.find('div', class_="gl-con").find_all('li')
        print(len(temp))
        for i in temp:
            info=[]
            name = i.get_text().replace('· ','')
            if name[-1]=='区':
                continue
            if name[0] == '市':
                name='珠海'+name
            info.append(name)
            info.append('广东省')
            info.append('珠海')
            info.append(datetime.datetime.now().strftime('%Y-%m-%d'))
            info.append(url)
            sql = whereNotInsert.main(tablename, t_eventField, info, 'name', info[0])
            save2db().save2db(sql)

    def shanTou(self):
        for i in range(1,4):
            url='http://www.shantou.gov.cn/u/zzjg?ajax=&name=&deptType='+str(i)+'&callback=handlerDept&currentPage=1&pageSize=40'
            html = req.get(url, headers=headers).content.decode('utf8')
            res=eval(html[12:-1])
            for i1 in res['data']:
                name=i1['name']
                info = []
                if name[-1] == '区':
                    continue
                if name[0] == '市':
                    name = '汕头' + name
                info.append(name)
                info.append('广东省')
                info.append('汕头')
                info.append(datetime.datetime.now().strftime('%Y-%m-%d'))
                info.append(urls[4])
                sql = whereNotInsert.main(tablename, t_eventField, info, 'name', info[0])
                save2db().save2db(sql)

    def foShan(self):
        url = urls[5]
        driver.get(url)
        if WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='right_nr']"))):
            html = driver.page_source
            soup = bs4(html, 'lxml')
            temp = soup.find('div', class_="right_nr").find_all('li')
        print(len(temp))
        for i in temp:
            info=[]
            name = i.get_text().replace('· ','')
            if name[-1]=='区':
                continue
            if name[0] == '市':
                name='佛山'+name
            info.append(name)
            info.append('广东省')
            info.append('佛山')
            info.append(datetime.datetime.now().strftime('%Y-%m-%d'))
            info.append(url)
            sql = whereNotInsert.main(tablename, t_eventField, info, 'name', info[0])
            save2db().save2db(sql)

    def saoGuan(self):
        url='http://www.gdzwfw.gov.cn/portal/custom-config/gdbsNav/getDetail'
        regCode='440200'
        html = req.get(url, headers=headers).content.decode('utf8')
        soup = bs4(html, 'lxml')
        temp = soup.find('div', id="department").find_all('li')

    def heYuan(self):
        url='http://www.gdzwfw.gov.cn/portal/custom-config/gdbsNav/getDetail'
        regCode='441600'
        html = req.get(url, headers=headers).content.decode('utf8')

    def meiZhou(self):
        url='http://www.gdzwfw.gov.cn/portal/custom-config/gdbsNav/getDetail'
        regCode='441400'
        html = req.get(url, headers=headers).content.decode('utf8')

    def huiZhou(self):
        url='http://www.gdzwfw.gov.cn/portal/custom-config/gdbsNav/getDetail'
        regCode='441300'
        html = req.get(url, headers=headers).content.decode('utf8')

    def sanWei(self):
        url='http://www.gdzwfw.gov.cn/portal/custom-config/gdbsNav/getDetail'
        regCode='441500'
        html = req.get(url, headers=headers).content.decode('utf8')

    def dongGuan(self):
        url='http://www.gdzwfw.gov.cn/portal/custom-config/gdbsNav/getDetail'
        regCode='441900'
        html = req.get(url, headers=headers).content.decode('utf8')

    def zongShan(self):
        url='http://www.gdzwfw.gov.cn/portal/custom-config/gdbsNav/getDetail'
        regCode='442000'
        html = req.get(url, headers=headers).content.decode('utf8')

    def jiangMen(self):
        url='http://www.gdzwfw.gov.cn/portal/custom-config/gdbsNav/getDetail'
        regCode='440700'
        html = req.get(url, headers=headers).content.decode('utf8')

    def yangJiang(self):
        url='http://www.gdzwfw.gov.cn/portal/custom-config/gdbsNav/getDetail'
        regCode='441700'
        html = req.get(url, headers=headers).content.decode('utf8')

    def sanWei(self):
        url='http://www.gdzwfw.gov.cn/portal/custom-config/gdbsNav/getDetail'
        regCode='441500'
        html = req.get(url, headers=headers).content.decode('utf8')

    def sanWei(self):
        url='http://www.gdzwfw.gov.cn/portal/custom-config/gdbsNav/getDetail'
        regCode='441500'
        html = req.get(url, headers=headers).content.decode('utf8')

    def sanWei(self):
        url='http://www.gdzwfw.gov.cn/portal/custom-config/gdbsNav/getDetail'
        regCode='441500'
        html = req.get(url, headers=headers).content.decode('utf8')

    def sanWei(self):
        url='http://www.gdzwfw.gov.cn/portal/custom-config/gdbsNav/getDetail'
        regCode='441500'
        html = req.get(url, headers=headers).content.decode('utf8')

    def sanWei(self):
        url='http://www.gdzwfw.gov.cn/portal/custom-config/gdbsNav/getDetail'
        regCode='441500'
        html = req.get(url, headers=headers).content.decode('utf8')

    def sanWei(self):
        url='http://www.gdzwfw.gov.cn/portal/custom-config/gdbsNav/getDetail'
        regCode='441500'
        html = req.get(url, headers=headers).content.decode('utf8')

    def sanWei(self):
        url='http://www.gdzwfw.gov.cn/portal/custom-config/gdbsNav/getDetail'
        regCode='441500'
        html = req.get(url, headers=headers).content.decode('utf8')

    def sanWei(self):
        url='http://www.gdzwfw.gov.cn/portal/custom-config/gdbsNav/getDetail'
        regCode='441500'
        html = req.get(url, headers=headers).content.decode('utf8')

    def sanWei(self):
        url='http://www.gdzwfw.gov.cn/portal/custom-config/gdbsNav/getDetail'
        regCode='441500'
        html = req.get(url, headers=headers).content.decode('utf8')

class save2db:
    def save2db(self,sql):
        try:
            cursor.execute(sql)
            db.commit()
        except:
            print(sql)

if __name__ == '__main__':
    global driver
    # driver = webdriver.Chrome()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    urls=['http://www.gd.gov.cn/zwgk/szfjg/index.html','http://www.gz.gov.cn/gzgov/s2791/common_tt.shtml'
        ,'http://www.sz.gov.cn/cn/xxgk/zfxxgj/jgsz/','http://www.zhuhai.gov.cn/zw/zfjg_44492/'
          ,'http://www.shantou.gov.cn/cnst/zzjg/zzjg.shtml','http://www.foshan.gov.cn/zwgk/zfjg/'
          ,'saoguan']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    db = pymysql.connect("localhost", "root", "123456", "sobey")
    cursor = db.cursor()
    tablename='t_government'
    t_eventField=['name','province','city','createtime','source']
    spider().foShan()