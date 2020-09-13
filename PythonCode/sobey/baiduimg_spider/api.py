from flask import Flask, request
import time
import re
import sys
import os
import json
from get_imgurl import get_imgurl
from get_imgurl import t

app = Flask(__name__)


@app.route('/imgpath', methods=['GET'])
def imgurl():
    word=request.args.get('word')
    legal_re = re.compile('[\u4e00-\u9fa5_a-zA-Z0-9]')
    word = ''.join(legal_re.findall(str(word)))
    imgdir = './ext_file_root/bucket-k/tempimage/' + word
    linuxdir = '/bucket-k/tempimage/' + word
    if word is  None or len(word)==0:
        return {"status": False, "word": "未传参"}

    if os.path.exists(imgdir) is True and len(os.listdir(imgdir))>0:
        imgpath=[]
        for i in os.listdir(imgdir):
            imgpath.append(linuxdir+'/'+i)
        res={"status": True, "data": imgpath}
        return json.dumps({"status": True, "data": imgpath})
    else:
        res=get_imgurl.get_sogou().start_spider(word)
        return json.dumps(res)

@app.route('/t', methods=['GET'])
def test():
    return str(t.b())

if __name__ == '__main__':
    app.run(debug=True,threaded=True)
else:
    app.run(debug=False)
