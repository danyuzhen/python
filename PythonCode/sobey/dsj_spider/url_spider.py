import re
from bs4 import BeautifulSoup as bs4
import requests as req
import lxml
import pymysql
import os
import sys
import datetime
import multiprocessing

def get_newsUrl():
    titleUrlList=['http://www.dsj365.cn/day.html','http://www.dsj365.cn/month.html','http://www.dsj365.cn/year.html',
                 'http://www.dsj365.cn/timeline.html','http://www.dsj365.cn/history.html']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    for i in titleUrlList:
        html = req.get(i, headers=headers).content.decode('utf8')
        page_re=re.compile('<li class="page[\S\s]{0,2}">[\S\s]*?</li>')
        lastUrlurl_re=re.compile('http://[\s\S]*?pageNo=[0-9]{1,2}')
        temp=page_re.findall(html)
        lastUrl=lastUrlurl_re.findall(temp[-1])[-1]
        temp=lastUrl.split('pageNo=')
        pageUrlList=[]
        newsUrlList=[]
        for i1 in range(1,int(temp[-1])+1):
            pageUrlList.append("%s%s%s"%(temp[0],'pageNo=',i1))
        for i1 in pageUrlList:
            html = req.get(i1, headers=headers).content.decode('utf8')
            soup=bs4(html,'lxml')
            newsUrl = soup.find_all(class_="news-info")
            for i2 in newsUrl:
                url=i2.find('a').get('href')
                if url not in newsUrlList:
                    newsUrlList.append(url)
            for i2 in newsUrlList:
                try:
                    sql='INSERT INTO dsj_url(url) select "'+i2+'" from dual ' \
                                                                    'WHERE not exists (select id from dsj_url where url = "'+i2+'")'
                    cursor.execute(sql)
                    db.commit()
                    print(i2)
                except:
                    print(sql)




if __name__ == '__main__':
    db = pymysql.connect("localhost", "root", "123456", "sobey")
    cursor = db.cursor()