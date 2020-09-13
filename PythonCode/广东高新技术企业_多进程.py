import requests as req
import time
import re
import pymysql
import multiprocessing
from multiprocessing import Pool

def header_info(now_date,value):
    data={
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': '',
        'Host': 'gddata.gd.gov.cn',
        'Referer': 'http://gddata.gd.gov.cn/index.php/data/grid/id/279/exchange/1.html?field=21&condition=like&value=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
        }

    header={
        'field': '21',
        'condition': 'like',
        'value': str(value),
        '_search': 'false',
        'nd': now_date,
        'rows': '50',
        'page': '1',
        'sidx': 'id',
        'sord': 'desc'
        }
    return data,header

def sql_create(start,end):
    for i in range(start*100, end*100):
        sttime=time.time()
        try:
            now_date = str(time.time() * 1000)[0:13]
            data, header = header_info(now_date, i)
            html = req.get(url, params=header, headers=data).text
        except:
            now_date = str(time.time() * 1000)[0:13]
            data, header = header_info(now_date, i)
            html = req.get(url, params=header, headers=data).text

        for i1 in info_list_rule.findall(html):
            info_spi = i1[9:-1].split(',')
            if len(info_spi)>3:
                organizational_code.append(info_spi[1][1:-1])
                company_name.append(eval(repr(info_spi[2]).replace('\\\\', '\\'))[1:-1])
                company_number.append(info_spi[3][1:-1])
                level.append(eval(repr(info_spi[4]).replace('\\\\', '\\'))[1:-1])
                certification_unit.append(eval(repr(info_spi[5]).replace('\\\\', '\\'))[1:-1])
                issue_date.append(eval(repr(info_spi[6]).replace('\\\\', ''))[1:-1])
                term_validity.append(eval(repr(info_spi[7]).replace('\\\\', '\\'))[1:-1])
                logout_date.append(eval(repr(info_spi[8]).replace('\\\\', ''))[1:-1])
                new_date.append(eval(repr(info_spi[9]).replace('\\\\', ''))[1:-1])
                update_date.append(eval(repr(info_spi[10]).replace('\\\\', ''))[1:-1])
            else:
                continue
        print("第"+str(i)+"次执行，用时："+str(time.time()-sttime))
    #不重复的数据
    label = {}
    for i in range(len(organizational_code)):
        if organizational_code[i] not in label.keys():
            label[organizational_code[i]] = i
    #生成插入sql命令
    for i in label.values():
        sql = 'insert into guangdong_company values("' + str(organizational_code[i]) + '","' \
              + str(company_name[i]) + '","' + str(company_number[i]) + '","' \
              + str(level[i]) + '","' + str(certification_unit[i]) + '","' \
              + str(issue_date[i]) + '","' + str(term_validity[i]) + '","' \
              + str(logout_date[i]) + '","' + str(new_date[i]) + '","' + str(update_date[i]) + '")'
        sql_list.append(sql)
    return sql_list

def mian(s):
    global sql_list,url,info_list_rule,id_list_rule,organizational_code,company_name
    global company_number,level,certification_unit,issue_date,term_validity
    global logout_date,new_date,update_date,db,cursor
    db = pymysql.connect("localhost", "root", "123456", "sobey")
    cursor = db.cursor()
    url = 'http://gddata.gd.gov.cn/index.php/data/grid/id/279/exchange/1.html?'
    info_list_rule = re.compile('cell":["[\D\d]*?]')
    id_list_rule = re.compile('[0-9]{8,12}')
    organizational_code = []
    company_name = []
    company_number = []
    level = []
    certification_unit = []
    issue_date = []
    term_validity = []
    logout_date = []
    new_date = []
    update_date = []

    for i in range(s,s+1):
        sql_list = []
        sql_list=sql_create(i,i+1)
        sql_list = list(set(sql_list))
        for i in sql_list:
            try:
                cursor.execute(i)
                db.commit()
            except:
                db.rollback()
                print(i)
    print(s*100,'-',(s+1)*100,"次执行完成")
    time.sleep(10)

if __name__=='__main__':
    for i in range(350, 400):
        p = multiprocessing.Process(target=mian, args=(i,))
        p.start()
