import requests as req
import re
from bs4 import BeautifulSoup as bs4
import pymysql
import time
import sys
import lxml
import datetime
import time

def get_hospital_list():
    sql='SELECT name from hospital where description is null order by id'
    cursor.execute(sql)
    temp=cursor.fetchall()
    hospital_list=[]
    urls=[]
    for i in temp:
        hospital_list.append(i[0])
        urls.append('https://baike.baidu.com/item/'+i[0])
    get_baike_text(hospital_list,urls)

def get_baike_text(hospital_list,urls):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'baike.baidu.com',
        "Referer": "https://baike.baidu.com/",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    for i in range(len(urls)):
        html = req.get(urls[i], headers=headers).content.decode('utf8')
        soup=bs4(html,'lxml')
        des = soup.find('div', {'class': 'lemma-summary'})
        if not des is None:
            des=re.sub('\[[0-9]{1,2}\]', "", des.get_text()).replace('\n','').replace('\xa0','')\
                .replace('"','“').replace("'","‘")
            sql='update hospital set description="'+des+'" where name="'+hospital_list[i]+'"'
            print('剩余'+str(len(urls)-i)+':'+urls[i])
            cursor.execute(sql)
            db.commit()
        else:
            print('未收录：'+urls[i])
            continue



if __name__ == '__main__':
    db = pymysql.connect("47.102.141.184", "root", "123456", "sobey")
    # db = pymysql.connect("localhost", "root", "123456", "sobey")
    cursor = db.cursor()
    get_hospital_list()
