import re
from bs4 import BeautifulSoup as bs4
import requests as req
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
        self.page_re = re.compile('<li class="page[\S\s]{0,2}">[\S\s]*?</li>')
        self.newsYear_re = re.compile('[0-9]{4}年')
        self.time_re = re.compile('昨日|今日|[0-9]{2}-[0-9]{2}')

    '''
    获取一个没爬过的url
    '''
    def get_newsUrl(self):
        sql = 'SELECT url FROM dsj_url WHERE type=0 LIMIT 1'
        cursor.execute(sql)
        try:
            res = cursor.fetchall()
            if len(res) > 0:
                return res[0][0]
            else:
                sys.exit()
        except:
            return None

    '''
    获取新闻页面中其他页url
    '''
    def get_newsurlINpage(self,soup):
        urls = []
        for i in soup.find(class_="pagination").find_all('a'):
            if i.get('href') not in urls:
                urls.append(i.get('href'))
        return urls

    '''
    天天大事新闻内容
    '''
    def get_dayNewsDes(self,section,soup):
        temp = section.find(class_="content-list").find('div')
        temp1 = soup.find('title')
        newsYear_re = re.compile('[0-9]{4}年')
        time_re = re.compile('昨日|今日|[0-9]{2}-[0-9]{2}')
        title = section.find('strong').get_text()[3:]
        address = re.sub('\s', '', temp.find('a').get_text())
        newsYear = newsYear_re.findall(temp1.get_text())[0]
        if time_re.findall(temp.get_text())[0].find('今') != -1:
            date = datetime.date.today().strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
        elif time_re.findall(temp.get_text())[0].find('昨') != -1:
            date = (datetime.date.today() + datetime.timedelta(-1)).strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月',
                                                                                                       d='日')
        else:
            md = time_re.findall(temp.get_text())[0].replace('-', '月') + '日'
            date = newsYear + md
        temp = str(section.find(class_="content-list"))
        temp = re.sub('<a [\s\S]*?>[\s\S]*?</a>', '', temp)
        temp = re.sub('<div[\s\S]*?>[\s\S]*?</div>', '', temp)
        temp = re.sub('<p[\s\S]*?>[\s\S]*?</p>', '', temp)
        temp = re.sub('<ul[\s\S]*?>[\s\S]*?</ul>', '', temp)
        temp = re.sub('<input name="reply_comment_id" type="hidden"/>', '', temp)
        temp = re.sub('[<strong>|</strong>|</div>|<br/>|-]', '', temp).strip()
        newsinfo_re = re.compile('^[事件介绍|摘要][\S]{1,200}')
        newsinfo = newsinfo_re.findall(temp)[0].split('：')[-1]
        return [title, newsinfo, address, date]

    '''
    月度、年度新闻内容
    '''
    def get_monthYearNewsDes(self,section,soup):
        title = section.find(class_='wxqq-borderBottomColor').get_text().split('.')[1]
        address = section.find(class_='area').find('a').get_text().strip()
        newsYear = self.newsYear_re.findall(soup.find('title').get_text())[0]
        temp = section.find(class_="area")
        if self.time_re.findall(temp.get_text())[0].find('今') != -1:
            date = datetime.date.today().strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
        elif self.time_re.findall(temp.get_text())[0].find('昨') != -1:
            date = (datetime.date.today() + datetime.timedelta(-1)).strftime('%Y{y}%m{m}%d{d}').format(
                y='年', m='月', d='日')
        else:
            md = self.time_re.findall(temp.get_text())[0].replace('-', '月') + '日'
            date = newsYear + md
        newsinfo = section.find('p').get_text().replace('原文链接', '').strip()
        return [title, newsinfo, address, date]

    '''
    时间轴新闻
    '''
    def get_timelineNewsDes(self,section,soup):
        title = section.find(class_='wxqq-borderBottomColor').get_text().split('\xa0')[-1]
        address = ''
        try:
            newsYear = self.newsYear_re.findall(soup.find('title').get_text())[0]
        except:
            newsYear=datetime.date.today().strftime('%Y{y}').format(y='年')

        temp = section.find(class_="date")
        if self.time_re.findall(temp.get_text())[0].find('今') != -1:
            date = datetime.date.today().strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
        elif self.time_re.findall(temp.get_text())[0].find('昨') != -1:
            date = (datetime.date.today() + datetime.timedelta(-1)).strftime('%Y{y}%m{m}%d{d}').format(
                y='年', m='月', d='日')
        else:
            md = self.time_re.findall(temp.get_text())[0].replace('-', '月') + '日'
            date = newsYear + md
        newsinfo = section.find(class_='content_item').get_text()\
            .replace('原文链接', '').replace('事件介绍：', '').replace('延伸阅读：', '').strip()
        return [title, newsinfo, address, date]

    '''
    历史事件新闻
    '''
    def get_HistoryNewsDes(self,section,soup):
        title = section.find(class_='content').find('p').get_text()
        try:
            newsYear = self.newsYear_re.findall(soup.find('title').get_text())[0]
        except:
            newsYear=datetime.date.today().strftime('%Y{y}').format(y='年')
        date=section.find(class_="date").find('p').get_text()
        if len(date.split('月')[0])==1:
            date='0'+date
        if len(date.split('月')[1])==2:
            date=date.split('月')[0]+'月'+'0'+date.split('月')[1]
        date = newsYear + date
        address=''
        newsinfo=section.find(class_='content_item').get_text()\
            .replace('原文链接','').replace('历史上的今天','').strip()
        if len(address) == 0 or address is None:
            newsinfo=''
        return [title, newsinfo, address, date]

    '''
    存到表中
    '''
    def save2db(self,sql):
        try:
            cursor.execute(sql)
            db.commit()
        except:
            print(sql)

    '''
    改变爬过的url状态
    '''
    def changeUrlType(self,url):
        sql='update '+tablename+' set type=1 where url="'+url+'"'
        try:
            cursor.execute(sql)
        except:
            print(sql)

    def start_spider(self):
        url=self.get_newsUrl()
        if url is None:
            sys.exit()
        html = req.get(url, headers=headers).content.decode('utf8')
        soup = bs4(html, 'lxml')
        section_day = soup.find_all('section', id=re.compile("[0-9]*?"))
        section_monthYear = soup.find_all('section', class_="item_content")
        section_timelineHistory = soup.find_all('section', class_="tl_content_item")
        pageType=soup.find(class_="listview2").get_text()

        if pageType=='大事记365':
            # 多页
            if len(self.page_re.findall(html))>0:
                pass
            else:
                for i in section_day:
                    info =self.get_dayNewsDes(i, soup)
                    info.append(url)
                    info.append(datetime.datetime.now().strftime('%Y-%m-%d'))
                    sql = whereNotInsert.main(tablename, t_eventField, info, 'name', info[0])
                    self.save2db(sql)

        if pageType == '月度事件' or pageType == '年度事件':
            # 多页
            if len(self.page_re.findall(html)) > 0:
                urls=self.get_newsurlINpage(soup)
                for i in urls:
                    html = req.get(i, headers=headers).content.decode('utf8')
                    soup = bs4(html, 'lxml')
                    section_monthYear = soup.find_all('section', class_="item_content")
                    # 循环每一条新闻
                    for i in section_monthYear:
                        info=self.get_monthYearNewsDes(i, soup)
                        info.append(url)
                        info.append(datetime.datetime.now().strftime('%Y-%m-%d'))
                        sql = whereNotInsert.main(tablename, t_eventField, info, 'name', info[0])
                        self.save2db(sql)
                    self.changeUrlType(i)
            else:
                for i in section_monthYear:
                    info = self.get_monthYearNewsDes(i, soup)
                    info.append(url)
                    info.append(datetime.datetime.now().strftime('%Y-%m-%d'))
                    sql = whereNotInsert.main(tablename, t_eventField, info, 'name', info[0])
                    self.save2db(sql)

        if pageType == '时间轴':
            # 多页
            if len(self.page_re.findall(html)) > 0:
                urls = self.get_newsurlINpage(soup)
                for i in urls:
                    html = req.get(i, headers=headers).content.decode('utf8')
                    soup = bs4(html, 'lxml')
                    section_timelineHistory = soup.find_all('section', class_="tl_content_item")
                    # 循环每一条新闻
                    for i in section_timelineHistory:
                        info = self.get_timelineNewsDes(i, soup)
                        info.append(url)
                        info.append(datetime.datetime.now().strftime('%Y-%m-%d'))
                        sql = whereNotInsert.main(tablename, t_eventField, info, 'name', info[0])
                    self.changeUrlType(i)
            else:
                for i in section_timelineHistory:
                    info = self.get_timelineNewsDes(i, soup)
                    info.append(url)
                    info.append(datetime.datetime.now().strftime('%Y-%m-%d'))
                    sql = whereNotInsert.main(tablename, t_eventField, info, 'name', info[0])

        if pageType == '历史事件':
            # 多页
            if len(self.page_re.findall(html)) > 0:
                urls = self.get_newsurlINpage(soup)
                for i in urls:
                    html = req.get(i, headers=headers).content.decode('utf8')
                    soup = bs4(html, 'lxml')
                    section_timelineHistory = soup.find_all('section', class_="tl_content_item")
                    for i in section_timelineHistory:
                        info=self.get_HistoryNewsDes(i, soup)
                        info.append(url)
                        info.append(datetime.datetime.now().strftime('%Y-%m-%d'))
                        sql = whereNotInsert.main(tablename, t_eventField, info, 'name', info[0])
                        self.save2db(sql)
                    self.changeUrlType(i)
            else:
                for i in section_timelineHistory:
                    info=self.get_HistoryNewsDes(i, soup)
                    info.append(url)
                    info.append(datetime.datetime.now().strftime('%Y-%m-%d'))
                    sql = whereNotInsert.main(tablename, t_eventField, info, 'name', info[0])
                    self.save2db(sql)
        self.changeUrlType(url)


if __name__ == '__main__':
    # db = pymysql.connect("localhost", "root", "123456", "sobey")
    db = pymysql.connect("47.102.141.184", "root", "123456", "sobey")
    tablename='t_bigevent'
    t_eventField=['name','description','eventdate','eventaddress','source','createtime']
    cursor = db.cursor()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    spider().start_spider()

