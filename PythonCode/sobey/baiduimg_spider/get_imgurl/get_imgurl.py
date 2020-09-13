import re
import requests as req
import datetime
import time
import json
import uuid
import os
import multiprocessing
import threading

#图片路径改为docker下，中文名文件夹，返回相对路径
class get_baidu:
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        self.legal_re = re.compile('[\u4e00-\u9fa5_a-zA-Z0-9]')
        self.imgurl_re = re.compile('data-imgurl="http[\s\S]*?"')
        self.picurl_re = re.compile('"pic_url":"[\S]*?"')

    # 百度微缩图
    def get_baidu(self, word):
        pass

#搜狗原图
class get_sogou:

    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        self.legal_re = re.compile('[\u4e00-\u9fa5_a-zA-Z0-9]')
        self.imgurl_re = re.compile('data-imgurl="http[\s\S]*?"')
        self.picurl_re = re.compile('"pic_url":"[\S]*?"')
        self.imgdir='./ext_file_root/bucket-k/tempimage/'
        self.linuxImgDir='/ext_file_root/bucket-k/tempimage/'
        self.imgpath=[]

    def get_imgurl(self,word):
        urls=[]
        word = ''.join(self.legal_re.findall(str(word)))
        url='https://pic.sogou.com/pics?query='+word
        html = req.get(url, headers=self.headers).text
        picurl_list=self.picurl_re.findall(html)
        for i in picurl_list:
            urls.append(i[11:-1])
        return urls

    def downImg(self,url,word,num):
        try:
            imgdir=self.imgdir+word
            r = req.get(url).content
            filename = str(num) + '.jpg'
            filePath = '%s%s%s' % (imgdir,'/', filename)
            with open(filePath, 'wb') as f:
                f.write(r)
            fileSize=int(os.path.getsize(filePath)/1024)
            if fileSize<10:
                os.remove(filePath)
        except:
            pass

    def downFinish(self,imgdir,urls):
        fileList = os.listdir(imgdir)
        for i in range(0,len(urls)):
            fileList = os.listdir(imgdir)
            if len(fileList) == 10:
                for i in range(len(fileList)):
                    fileList[i]=self.linuxImgDir+fileList[i]
                return {"status": True, "data": fileList}
            try:
                r = req.get(urls[i]).content
                filename = str(i) + '.jpg'
                filePath = '%s%s%s' % (imgdir, '/', filename)
                with open(filePath, 'wb') as f:
                    f.write(r)
                fileSize = int(os.path.getsize(filePath) / 1024)
                if fileSize < 10:
                    os.remove(filePath)
            except:
                pass


    def start_spider(self,word):
        st=time.time()
        urls=self.get_imgurl(word)
        imgdir = self.imgdir + word
        if os.path.exists(imgdir) is False:
            os.makedirs(imgdir)
        # 先开10进程下载一次，再扫描文件夹下是否有10个文件，不足再调用单进程补充到10为止
        thread = []
        for i in range(10):
            p = threading.Thread(target=get_sogou().downImg, args=(urls[i],word,i,))
        for i in range(10):
            p.start()
        for i in range(10):
            p.join()
        res=self.downFinish(imgdir, urls)
        return res


# if __name__ == '__main__':
    # for i in range(5):
    #     p = multiprocessing.Process(target=get_sogou().start_spider)
    #     p.start()
# get_sogou().start_spider('成都')
# else:
#     pass
    # print(get_imgurl().get_sogou('重庆'))