import requests as req
import re
import time
import sys
urls_file = open("urls/china.txt", 'r', encoding='utf-8')
urls = eval(urls_file.read())
urls_file.close()
headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "Hm_lvt_fcda14e8d9fc166be9cf6caef393ad0e=1555595773; wdcid=31a4ffa8f8a8d5d2; __asc=2f905f6c16a30bbcebb828635a7; __auc=2f905f6c16a30bbcebb828635a7; LBN=node5; wdses=516ffa72ad0d321f; wdlast="+str(int(time.time()))+"; Hm_lpvt_fcda14e8d9fc166be9cf6caef393ad0e="+str(int(time.time())),
            "Host": "news.southcn.com",

            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
            }
title_list=[]
time_list=[]
news_list=[]
title_rule=re.compile('<title>.*?</title>')
time_rule=re.compile('<span class="pub_time" id="pubtime_baidu">.{10,30}</span>')
news_rule=re.compile('<!--enpcontent-->[\s\S]*?<!--/enpcontent-->')
newsp_rule=re.compile('<p>[\s\S]*?</p>')
for i in urls:
    html = req.get(i[:-1], data=headers).content.decode('utf8')
    print(i[:-1])
    for j in news_rule.findall(html):
        temp_str=""
        for k in newsp_rule.findall(j):
            temp_str=temp_str+re.sub('<[a-z/A-Z]+>|\\u3000|<.*?>|[.\n]+<!--[.\n][\s].*?[.\n]+-->','',k)+"[line]"
    news_list.append(temp_str)
    title_list.append(title_rule.findall(html)[1][7:-8])
    time_list.append(time_rule.findall(html)[0][42:-7])
    # time.sleep(1)

f=open('news/china_news.txt','a+',encoding='utf-8')
data=f.write(str(news_list))
f.close()

f=open('news/china_title.txt','a+',encoding='utf-8')
data=f.write(str(title_list))
f.close()

f=open('news/china_time.txt','a+',encoding='utf-8')
data=f.write(str(time_list))
f.close()
