import pymysql
import jieba
import jieba.analyse
import sys
import os

#返回所有id和标题
def search_sql():
    global db,cursor
    db = pymysql.connect("localhost", "root", "123456", "news")
    cursor = db.cursor()
    sql="select title from news"
    sql1="select news_id from news"
    cursor.execute(sql)
    res = cursor.fetchall()
    cursor.execute(sql1)
    res1 = cursor.fetchall()
    res_dict={}
    for i in  range(len(res)):
        res_dict[res1[i][0]]=res[i][0]
    return res_dict

def words2vec(words1=None, words2=None):
    v1 = []
    v2 = []
    tag1 = jieba.analyse.extract_tags(words1, withWeight=True)
    tag2 = jieba.analyse.extract_tags(words2, withWeight=True)
    tag_dict1 = {i[0]: i[1] for i in tag1}
    tag_dict2 = {i[0]: i[1] for i in tag2}
    merged_tag = set(tag_dict1.keys()) | set(tag_dict2.keys()) #两个标题的关键词
    for i in merged_tag:
        if i in tag_dict1:
            v1.append(tag_dict1[i])
        else:
            v1.append(0)
        if i in tag_dict2:
            v2.append(tag_dict2[i])
        else:
            v2.append(0)
    return v1, v2

def cosine_similarity(vector1, vector2):
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a, b in zip(vector1, vector2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return 0
    else:
        return round(dot_product / ((normA ** 0.5) * (normB ** 0.5)) * 100, 2)

def cosine(str1, str2):
    vec1, vec2 = words2vec(str1, str2)
    return cosine_similarity(vec1, vec2)


if __name__ == '__main__':
    user_id = sys.argv[1]
    receive_title = sys.argv[2]
    # user_id = 112
    # receive_title = "习近平情满扶贫路 和总书记一起共话脱贫攻坚"
    res_dict=search_sql()
    #删除原有推荐
    cursor.execute("DELETE FROM recommend WHERE user_id ="+str(user_id))
    db.commit()
    score_dict_all={}
    score_top10=[]
    for i in res_dict:
        score = cosine(receive_title, res_dict[i])
        if score > 0:
            score_dict_all[i]=score
    #vavlue值排序，返回元组
    for i in sorted(score_dict_all.items(), key=lambda x: x[1], reverse=True)[1:11]:
        score_top10.append(i[0])
    top10_sql=" SELECT * FROM	news WHERE news_id in ("
    for i in score_top10:
        if i!=score_top10[-1]:
            top10_sql=top10_sql+str(i)+','
        else:
            top10_sql = top10_sql + str(i) + ')'
    print(top10_sql)
    #存储推荐新闻
    cursor.execute(top10_sql)
    res = cursor.fetchall()
    for i in res:
        sql="insert into recommend(user_id,news_id,type,title,time,news,keyword) values('"+str(user_id)+"','"+str(i[0])+"','"+str(i[1])+"','"+str(i[2])+"','"+str(i[3])+"','"+str(i[4])+"','"+str(i[5])+"')"
        cursor.execute(sql)
        db.commit()
        # print(sql)



    