import re
from bs4 import BeautifulSoup as bs4
import requests as req
import lxml
import pymysql
import os
import sys
import datetime
import multiprocessing


class quick_actions:
    def get_maxpage(self,url):
        html = req.get(url, headers=headers).content.decode('utf8')
        soup = bs4(html, 'lxml')
        pagemax = int(soup.find('span', {'class': 'zys'}).get_text())
        return pagemax

    def get_schoolDesUrl(self,url):
        urlList=[]
        html = req.get(url, headers=headers).content.decode('utf8')
        soup = bs4(html, 'lxml')
        temp = soup.find_all(class_="sk")
        schoolUrl_re = re.compile('"[\S]{1,10}www.ruyile.com/school/[\S]{1,20}"')
        # 每页所有学校信息的div列表
        for k in temp:
            try:
                res = schoolUrl_re.findall(str(k))
                if len(res) > 0:
                    urlList.append(res[0][1:-1])
                else:
                    continue
            except:
                return []
        return urlList

    def get_schoolDes(self,url):
        html = req.get(url, headers=headers).content.decode('utf8')
        soup = bs4(html, 'lxml')
        schoolInfo_div=soup.find('div', {'class': 'xxsx'})
        schoolDes=soup.find('div', {'class': 'jj'}).get_text()\
            .replace('"','').replace("'",'').replace('\u3000','').replace('\xa0','')
        schoolName=soup.find('div', {'class': 'stk'}).find('h1').get_text()
        info=['']*12
        title=[schoolName,schoolDes,'所属地区','学校性质','学校级别','学校类型','招生电话','学校邮箱','班级人数',
               '学校网址','学校地址','邮政编码']
        info[0]=schoolName
        info[1]=schoolDes
        for i in schoolInfo_div:
            text = i.get_text().split('：')
            if text[0] in title:
                num = title.index(text[0])
                info[num] = text[1]
        today=datetime.datetime.now().strftime('%Y-%m-%d')
        info.append(url)
        info.append(today)
        return info,schoolName

    def easysql_wherenot(self,tablename,tag,info,field,condition):
        if isinstance(tablename,str) and isinstance(tag,list) and isinstance(info,list):
            condition="'"+condition.replace('"','').replace("'",'')+"'"
            tag = '('+','.join(tag)+')'
            insertInfo=' select '+str(tuple(info)).replace('"',"'")[1:-1]+' from dual '
            wherenot='WHERE not exists (select id from '+tablename+' where '+field+' = '+condition+')'
            sql='INSERT INTO '+tablename+tag+insertInfo+wherenot
            return sql
        else:
            return None

    def schoolINdb(self,url):
        sql='select id from '+tableName+' where source="'+url+'"'
        try:
            cursor.execute(sql)
            res=cursor.fetchall()
            if isinstance(res[0][0],int) and res[0][0]>0:
                return True
            else:
                return False
        except:
            return False

class spider:
    def get_pchool(self,i):
        # 小学
        pageurl="%s%s%s"%('https://www.ruyile.com/xuexiao/?a=',i,'&t=2')
        pagemax_ps=quick_actions().get_maxpage(pageurl)
        for j in range(1,pagemax_ps+1):
            url = "%s%s%s%s" % ('https://www.ruyile.com/xuexiao/?a=', i, '&t=2&p=',j)
            schoolDesUrl=quick_actions().get_schoolDesUrl(url)
            for url in schoolDesUrl:
                if quick_actions().schoolINdb(url)==False:
                    info,schoolName=quick_actions().get_schoolDes(url)
                    sql=quick_actions().easysql_wherenot(tableName,tabletag,info,'name',schoolName)
                    self.save2db(sql)
                    print('完成：'+url)
                else:
                    print('已在表中：' + url)
                    continue
        print(pageurl)
        print(errsql)

    def get_hschool(self,i):
        # 中学
        pageurl = "%s%s%s" % ('https://www.ruyile.com/xuexiao/?a=', i, '&t=3')
        pagemax_hs = quick_actions().get_maxpage(pageurl)
        for j in range(1, pagemax_hs + 1):
            url = "%s%s%s%s" % ('https://www.ruyile.com/xuexiao/?a=', i, '&t=3&p=', j)
            schoolDesUrl = quick_actions().get_schoolDesUrl(url)
            for url in schoolDesUrl:
                if quick_actions().schoolINdb(url) == False:
                    info, schoolName = quick_actions().get_schoolDes(url)
                    sql = quick_actions().easysql_wherenot(tableName, tabletag, info, 'name', schoolName)
                    self.save2db(sql)
                    print('完成：' + url)
                else:
                    print('已在表中：' + url)
                    continue
        print(pageurl)
        print(errsql)

    def save2db(self,sql):
        try:
            cursor.execute(sql)
            db.commit()
        except:
            print(sql)
            errsql.append(sql)

if __name__ == '__main__':
    db = pymysql.connect("47.102.141.184", "root", "123456", "sobey")
    # db = pymysql.connect("localhost", "root", "123456", "sobey")
    cursor = db.cursor()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    tableName = 't_school'
    tabletag = ['name', 'description', 'city', 'nature', 'level', 'type', 'number', 'email', 'class_size', 'url',
                'address', 'postal_code', 'source', 'createtime']
    errsql=[]
    for i in range(1,34):
        p = multiprocessing.Process(target=spider().get_pchool(i), args=(i,))
        p1 = multiprocessing.Process(target=spider().get_hschool(i), args=(i,))
        p.start()
        p1.start()
