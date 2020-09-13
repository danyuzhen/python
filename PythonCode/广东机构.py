# -*- coding: utf-8 -*-
#coding:utf-8
"""
Created on Fri May 17 12:27:11 2019

@author: admin
"""

import requests as req
import re
import pymysql
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs4
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import sys
urls={
      '梅州':'https://www.meizhou.gov.cn/organization/list?area=441400',
      '惠州':'http://zwgk.huizhou.gov.cn/0000/0102/201608/ada0d36483204e7ab67d74c9aa353051.shtml',
      '汕尾':'http://www.shanwei.gov.cn/shanwei/zzjg/zzjg.shtml',
      '东莞':'http://www.dongguan.gov.cn/cndg/branch/departments.shtml',
      '广州':'http://www.gz.gov.cn/gzgov/s2791/common_tt.shtml',
      # '中山':'http://zwgk.zs.gov.cn/main/zwgk/open/index.action',
      # '江门':'http://www.jiangmen.gov.cn/zwgk/zfjg/',
      '阳江':'http://zwgk.yangjiang.gov.cn/jgzn/',
      #'湛江': 'http://www.zhanjiang.gov.cn/_Layouts/Applicationpages/Zjgov2015/Institutions/GovInstitutions.aspx',
      '茂名':'http://zwgk.maoming.gov.cn/',
      '肇庆':'http://www.zhaoqing.gov.cn/xxgk/zzjg/',
      # '清远':'http://www.gdqy.gov.cn/gdqy/103/qy_list1.shtml',
      '潮州':'http://www.chaozhou.gov.cn/jgsz/index.jhtml',
      '云浮':'http://www.yunfu.gov.cn/web/yfmh/orgInfo/index.ptl',
      '河源':'http://www.heyuan.gov.cn/zw/xxgk.action',
      # '韶关':'http://www.gdzwfw.gov.cn/portal/affairs-public-index?region=440200',
      # '佛山':'http://www.foshan.gov.cn/zwgk/zfjg/',
      '汕头':'http://www.shantou.gov.cn/',
      # '珠海':'http://www.zhuhai.gov.cn/zw/zfjg_44492/',
      '深圳':'http://www.sz.gov.cn/cn/xxgk/zfxxgj/jgsz/'
    }
header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
    }
zs_header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie':'JSESSIONID=004E8C5A6258E82C1C73C864D7ED5F4C',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'Host': 'zwgk.zs.gov.cn'
        }
end_str_list=['局','厅','室','会','处','院','心','所']
news_str_list=['发布','我市','季度','座谈','国家','国务院','年度','中国','建成']

info_table_link_rule = re.compile('<ul class="clearfix">.*?</ul>')
info_link_rule = re.compile('<a[\d\D]*?>[\d\D]*?</a>')
chinese_rule = re.compile('[\u4e00-\u9fa5]{2,35}')
link_rule=re.compile('href="[\d\D]{20,30}html"')
#requests爬取
def get_info(city,url):
    label={}
    html=req.get(url,data=header)
    html=html.content
    if url=='http://www.sz.gov.cn/cn/xxgk/zfxxgj/jgsz/':
        html=str(html,'gbk')
    else:
        html = str(html, 'utf8')
    html=re.sub('\n', '', html, count=0, flags=0)
    info_table=info_table_link_rule.findall(html)
    info_link_list=info_link_rule.findall(str(info_table))
    for i in info_link_list:
        label[chinese_rule.findall(i)[0]]=link_rule.findall(i)[0][6:-1]
    #单位名称key，介绍网站value
    print(label)
    # print(len(services_name))
    # print(services_name)
    # print(len(info_link_list))
    # if len(services_name)<10:
    #     print(url)
    #     print(html)
    # for i in services_name:
    #     sql_insert(city,i)

#插入数据库
def sql_insert(city,services_name):
    db = pymysql.connect("localhost", "root", "123456", "mysql")
    cursor = db.cursor()
    sql = "INSERT INTO gd_services(city,services_name) VALUES('"+city+"','"+services_name+"')"
    # print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        # print('0')
    except:
        # 如果发生错误则回滚
        db.rollback()
        print(sql)
        print('1')

#对id重新排序
def sql_sort():
    sql = "SELECT * FROM gd_services"
    try:
        cursor.execute(sql)
        db.commit()
        results = cursor.fetchall()
        # print('0')
    except:
        db.rollback()
        print('1')

    for i in range(len(results)):
        sql="update gd_services set id="+str(i+1)+" where city='"+results[i][1]+"' and services_name='"+results[i][2]+"'"
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print('1')

def sql_check():
    db = pymysql.connect("localhost", "root", "123456", "mysql")
    cursor = db.cursor()
    sql='select id,city,services_name from gd_services'
    try:
        cursor.execute(sql)
        db.commit()
        results = cursor.fetchall()
    except:
        db.rollback()
        print('1')

    # for i in range(len(results)):
    #     sql="update gd_services set id="+str(i+1)+" where city='"+results[i][0]+"' and services_name='"+results[i][1]+"'"
    #     print(sql)
    #     try:
    #         # 执行sql语句
    #         cursor.execute(sql)
    #         # 提交到数据库执行
    #         db.commit()
    #         # results = cursor.fetchall()
    #         # print('0')
    #     except:
    #         # 如果发生错误则回滚
    #         db.rollback()
    #         print('1')

    # for i in results:
    #     if i[1] not in i[2]:
    #         new_name=i[1]+i[2]
    #         print(new_name)
    #         sql = "update gd_services set services_name='"+new_name+"'where id="+str(i[0])
    #         try:
    #             # 执行sql语句
    #             cursor.execute(sql)
    #             # 提交到数据库执行
    #             db.commit()
    #             # results = cursor.fetchall()
    #             # print('0')
    #         except:
    #             # 如果发生错误则回滚
    #             db.rollback()
    #             print('1')

    # driver = webdriver.Chrome()

    url = "https://map.baidu.com"
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.maximize_window()
    driver.get(url)
    seach_res_rule=re.compile('<div class="cf">[\D\d]*?<div class="l-row">')
    services_name_rule = re.compile('<div class="row">[\D\d]*?</div>')
    address_rule=re.compile('<span class="n-grey" title="[\D\d]*?">')
    address_chinese_rule=re.compile('title="[\D\d]*?"')

    number_list_rule=re.compile('<div class="row tel">[\D\d]*?</div>')
    chinese_rule=re.compile('[\u4e00-\u9fa5]{2,20}')
    div_rule=re.compile('<div class="row tel">[\D\d]*?</div>')
    number_rule=re.compile('[0-9-]{3,5}[-][0-9]{4,10}|[0-9]{4,10}')
    # time.sleep(20)
    for i in results[735:]:
        services_city = i[1]
        services_name=i[2]
        search_load = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[id="sole-input"]')))
        if search_load:
            driver.find_element_by_id('sole-input').click()
            driver.find_element_by_id('sole-input').clear()
            driver.find_element_by_id('sole-input').send_keys(services_name)
            driver.find_element_by_id('sole-input').send_keys(Keys.ENTER)

        #结果返回城市列表 render-mode-switch-button
        try:
            city_load=WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class="clarify-list-item"]')))
            if city_load:
                driver.find_elements_by_css_selector('[class="clarify-list-item"]')[0].click()
        except:
            pass
        #相关地址列表框
        res_load=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class="poilist"]')))
        if res_load:
            seach_list_load = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class="cf"]')))
            if seach_list_load:
                time.sleep(2)
                res_name_one=chinese_rule.findall(services_name_rule.findall(driver.page_source)[0])[0]
                eq_str=0
                for i1 in res_name_one:
                    for i2 in services_name:
                        if i1==i2:
                            eq_str=eq_str+1
                            break
                eq_str=eq_str/len(services_name)

                #地址正确
                if eq_str>0.7:
                    #没电话
                    if len(div_rule.findall(seach_res_rule.findall(driver.page_source)[0]))==0:
                        services_address=address_chinese_rule.findall(address_rule.findall(driver.page_source)[0])[0][7:-1]
                        #地址前没有城市名
                        if i[1] not in services_address:
                            services_address=services_city+services_address
                        sql="update gd_services set services_address='"+services_address+"' where id="+str(i[0])
                        print(sql)

                        try:
                            # 执行sql语句
                            cursor.execute(sql)
                            # 提交到数据库执行
                            db.commit()
                            # print('0')
                        except:
                            # 如果发生错误则回滚
                            db.rollback()
                            print('1')
                        continue
                    #有电话
                    else:
                        services_address = address_chinese_rule.findall(address_rule.findall(driver.page_source)[0])[0][7:-1]
                        services_number = number_rule.findall(number_list_rule.findall(driver.page_source)[0])[0]
                        # 地址前没有城市名
                        if i[1] not in services_address:
                            services_address = services_city + services_address
                        sql="update gd_services set services_address='"+services_address+"',services_number='"+services_number+"' where id="+str(i[0])
                        print(sql)
                        try:
                            # 执行sql语句
                            cursor.execute(sql)
                            # 提交到数据库执行
                            db.commit()
                            # print('0')
                        except:
                            # 如果发生错误则回滚
                            db.rollback()
                            print('1')
                #地址错误
                else:
                    continue
        # driver.quit()
        # break

def sql_check_nan():
    sql='select * from gd_services'
    cursor.execute(sql)
    db.commit()
    results = cursor.fetchall()
    for i in results:
        # print(i)
        if i[3] is None:
            print(i[2]+'-没有地址')
        if i[4] is None:
            print(i[2] + '-没有电话')
        if i[3] is None and i[4] is None:
            print(i[2]+'-没有地址和电话')
    # print(results[766][4] is None)

def req_spider():
    for key,values in urls.items():
        get_info(key,values)
        time.sleep(20)

def selenium_spider():
    driver = webdriver.Chrome()
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # driver = webdriver.Chrome(chrome_options=chrome_options)
    services_name = []
    ##########type1
    # driver.get("http://zwgk.zs.gov.cn/main/zwgk/open/index.action")
    # services_name=[]
    # html=str(driver.page_source)
    # zs_list=zs_div_rule.findall(html)
    # for i in zs_list:
    #     for j in info_link_rule.findall(i):
    #         for k in chinese_rule.findall(j):
    #             for es in end_str_list:
    #                 if es in k:
    #                     services_name.append(k)
    #                     sql_insert('中山', k)
    #                     break
    # print(services_name)
    ############type2
    info_list = re.compile('<li>[\d\D]*?</li>')
    url = "http://www.zhuhai.gov.cn/zw/zfjg_44492/"
    driver.get(url)
    # time.sleep(2)
    html=str(driver.page_source)
    services_load = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class="r-tit"]')))
    if services_load:
        for i in info_list.findall(html):
            for j in info_link_rule.findall(i):
                for k in chinese_rule.findall(j):
                    for es in end_str_list:
                        if es in k:
                            services_name.append(k)
                            break
        # print(services_name)
        services_name = list(set(services_name))
        print(len(services_name))
        print(services_name)
    for i in services_name:
        if '珠海' not in i:
            services_name[services_name.index(i)]='珠海'+i
            sql_insert('珠海', '珠海'+i)
        else:
            sql_insert("珠海", i)
    driver.quit()

if __name__ == '__main__':
    global db,cursor
    db = pymysql.connect("localhost", "root", "123456", "mysql")
    cursor = db.cursor()
    # sql_sort()
    # selenium_spider()
    # sql_check()
    # get_info('肇庆','http://www.zhaoqing.gov.cn/xxgk/zzjg/')
    sql_check_nan()