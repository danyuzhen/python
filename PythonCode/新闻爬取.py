import requests as req
import re
import time
get_url_list=["http://news.southcn.com/gd/default.htm","http://news.southcn.com/china/default.htm","http://news.southcn.com/international/default.htm","http://news.southcn.com/community/default.htm"]
headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "Hm_lvt_fcda14e8d9fc166be9cf6caef393ad0e=1555595773; wdcid=31a4ffa8f8a8d5d2; __asc=2f905f6c16a30bbcebb828635a7; __auc=2f905f6c16a30bbcebb828635a7; LBN=node5; wdses=516ffa72ad0d321f; wdlast="+str(int(time.time()))+"; Hm_lpvt_fcda14e8d9fc166be9cf6caef393ad0e="+str(int(time.time())),
            "Host": "news.southcn.com",
            "Referer": "http://news.southcn.com/gd/default_3.htm",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
            }
news_list=re.compile('<div class="pw">.*?</div>')
http_list=re.compile('[a-zA-z]+://[^\s]*')
news_link_list=[]

for i in get_url_list:
    for j in range(1,7):
        if j==1:
            html=req.get(i,data=headers).content.decode('utf8')
            print(i)
            time.sleep(1)

        else:
            html = req.get(i[0:-4]+"_"+str(j)+".htm", data=headers).content.decode('utf8')
            print(i[0:-4]+"_"+str(j)+".htm")
            time.sleep(1)

        for k in news_list.findall(html):
            news_link_list.append(http_list.findall(str(k))[0])
    f=open(i.split("/")[-2]+'.txt','a+',encoding='utf-8')
    data=f.write(str(news_link_list))
    f.close()
    news_link_list = []