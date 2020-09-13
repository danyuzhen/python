from pymongo import *
import datetime
import time
import math
import json
import pymysql
from dateutil.relativedelta import relativedelta
import rest


class test:
    def __init__(self):
        self.client = MongoClient('mongodb://sobeyhive:$0bEyHive*2o1Six@172.16.149.73:27017')
        self.db = self.client['hivedb']
        self.sh_d_entitydata = self.db['SH_D_ENTITYDATA']
        self.db73 = pymysql.connect('172.16.149.73', 'sdba', 'sdba', '83f98246')
        self.cursor = self.db73.cursor()
        self.today = datetime.date.today()
        self.weekStart = self.today - datetime.timedelta(days=self.today.weekday())
        self.weekEnd = self.today + datetime.timedelta(days=6 - self.today.weekday())
        self.monthStart = self.today - datetime.timedelta(days=self.today.day - 1)
        self.monthEnd = (self.today + datetime.timedelta(days=-self.today.day + 1)) + relativedelta(months=1, days=-1)
        self.today = self.today.isoformat()
        self.weekStart = self.weekStart.isoformat()
        self.weekEnd = self.weekEnd.isoformat()
        self.monthStart = self.monthStart.isoformat()
        self.monthEnd = self.monthEnd.isoformat()
        self.dataWeek = {
            "queryCondition": {
                "fieldConditionGroup": {
                    "fieldConditions": [
                        {
                            "field": "createDate_",
                            "value": "[{0} TO {1}]".format(self.weekStart, self.weekEnd),
                            "searchRelation": "and"
                        }
                    ]
                },
                "page": 1,
                "size": 0,
                "sortBys": []
            },
            "resourceName": "meta_smart"
        }
        self.dataMonth = {
            "queryCondition": {
                "fieldConditionGroup": {
                    "fieldConditions": [
                        {
                            "field": "createDate_",
                            "value": "[{0} TO {1}]".format(self.monthStart, self.monthEnd),
                            "searchRelation": "and"
                        }
                    ]
                },
                "page": 1,
                "size": 0,
                "sortBys": []
            },
            "resourceName": "meta_smart"
        }

    def start(self):
        resourcesNum = self.resources_num()
        resourceDuration = self.resource_duration()
        newResourcesToday = self.new_resources_today()
        analysisResourcesToday = self.analysis_resources_today()
        proofreadingResourcesToday = self.proofreading_resources_today()
        orgWeek, orgMonth = self.hot_organization()
        segmentsDurationDuration, segmentsDurationNum = self.segments_duration()
        keywordWeek, keywordMonth = self.key_word()
        locationsWeek, locationsMonth = self.locations_number()
        videoTopWeek, videoTopMonth, audioTopWeek, audioTopMonth = self.popular_classification()
        hotPeopleWeek, hotPeopleMonth = self.popular_person()
        saveToyear, saveTomonth, saveToweek, saveToday = self.savedata_quantity()
        readToyear, readTomonth, readToweek, readToday = self.readdata_quantity()
        res = {'resourcesNum': resourcesNum,
               'resourceDuration': resourceDuration,
               'newResourcesToday': newResourcesToday,
               'analysisResourcesToday': analysisResourcesToday,
               'proofreadingResourcesToday': proofreadingResourcesToday,
               'hotOrganization': {'week': orgWeek, 'month': orgMonth},
               'segmentsDuration': {'duration': segmentsDurationDuration, 'num': segmentsDurationNum},
               'keyword': {'week': keywordWeek, 'month': keywordMonth},
               'locationsNumber': {'week': locationsWeek, 'month': locationsMonth},
               'popularClassification': {'videoTopWeek': videoTopWeek, 'videoTopMonth': videoTopMonth,
                                         'audioTopWeek': audioTopWeek, 'audioTopMonth': audioTopMonth},
               'popularPerson': {'week': hotPeopleWeek, 'month': hotPeopleMonth},
               'savedataQuantity': {'year': saveToyear, 'month': saveTomonth, 'week': saveToweek, 'day': saveToday},
               'readdataQuantity': {'year': readToyear, 'month': readTomonth, 'week': readToweek, 'day': readToday}
               }
        print(rest.get_entityinfo_url(self.dataMonth))
        print(json.dumps(res, ensure_ascii=False))

    """
    资源总数
    """

    def resources_num(self):
        try:
            dataCount = self.sh_d_entitydata.count()
        except:
            dataCount = 0
        return dataCount

    """
    资源总时长
    """

    def resource_duration(self):
        duration = 0
        for x in self.sh_d_entitydata.find({}, {"dataregion": 1}):
            try:
                duration = duration + (x['dataregion']['duration'])
            except:
                pass
        duration = round(duration / 10000000 / 3600)
        return duration

    """
    今日新增
    """

    def new_resources_today(self):
        todayAdd = 0
        try:
            for x in self.sh_d_entitydata.find({}, {"dataregion": 1}):
                createDate = x['dataregion']['createDate_']
                if str(createDate).split(' ')[0] == self.today:
                    todayAdd = todayAdd + 1
        except:
            pass
        return todayAdd

    """
    今日分析
    """

    def analysis_resources_today(self):
        todayAnalysis = 0
        for x in self.sh_d_entitydata.find({}, {"dataregion": 1}):
            try:
                smart_endtime = x['dataregion']['smart_endtime']
                if str(smart_endtime).split(' ')[0] == self.today:
                    todayAnalysis = todayAnalysis + 1
            except:
                pass
        return todayAnalysis

    """
    今日审校
    """

    def proofreading_resources_today(self):
        todayProofreading = 0
        try:
            for x in self.sh_d_entitydata.find({}, {"dataregion": 1}):
                catalogue_time = x['dataregion']['catalogue_time']
                if str(catalogue_time).split(' ')[0] == self.today:
                    todayProofreading = todayProofreading + 1
        except:
            pass
        return todayProofreading

    """
    热门机构(本周  本月)
    """

    def hot_organization(self):
        orgWeek = {}
        orgMonth = {}
        try:
            res = rest.get_entityinfo_url(self.dataWeek)
            for i in res['extensionResults'][0]['values']:
                if i['facetShowName'] == '机构':
                    for i1 in i['facetValue'][:5]:
                        orgWeek[i1['value']] = i1['count']
            res = rest.get_entityinfo_url(self.dataMonth)
            for i in res['extensionResults'][0]['values']:
                if i['facetShowName'] == '机构':
                    for i1 in i['facetValue'][:5]:
                        orgMonth[i1['value']] = i1['count']
        except:
            pass
        return orgWeek, orgMonth

    """
    栏目片段时长
    """

    def segments_duration(self):
        duration = {}
        num = {}
        for x in self.sh_d_entitydata.find({}, {"dataregion": 1}):
            try:
                k = x['dataregion']['column']
                v = x['dataregion']['duration'] / 10000000 / 3600
                if k == 'None' or k is None:
                    k = '其他栏目'

                if k in duration.keys():
                    duration[k] = duration[k] + v
                else:
                    duration[k] = v
                if k in num.keys():
                    num[k] = num[k] + 1
                else:
                    num[k] = 1
            except:
                pass
        if len(duration) > 0:
            for k, v in duration.items():
                duration[k] = math.ceil(v)
        return duration, num

    """
    词云关键词(周，月)
    """

    def key_word(self):
        keywordWeek = {}
        keywordMonth = {}
        try:
            res = rest.get_entityinfo_url(self.dataWeek)
            for i in res['extensionResults'][0]['values']:
                if i['facetShowName'] == '关键词':
                    for i1 in i['facetValue'][:100]:
                        keywordWeek[i1['value']] = i1['count']
            res = rest.get_entityinfo_url(self.dataMonth)
            for i in res['extensionResults'][0]['values']:
                if i['facetShowName'] == '关键词':
                    for i1 in i['facetValue'][:100]:
                        keywordMonth[i1['value']] = i1['count']
        except:
            pass
        return keywordWeek, keywordMonth

    """
    地点标签热力图(本周，本月)
    """

    def locations_number(self):
        addressWeek = {}
        addressMonth = {}
        try:
            res = rest.get_entityinfo_url(self.dataWeek)
            for i in res['extensionResults'][0]['values']:
                if i['facetShowName'] == '地点':
                    for i1 in i['facetValue'][:100]:
                        if i1['value'] not in \
                                ['筛选过的地点词列表1', '筛选过的地点词列表2']:
                            addressWeek[i1['value']] = i1['count']
            res = rest.get_entityinfo_url(self.dataMonth)
            for i in res['extensionResults'][0]['values']:
                if i['facetShowName'] == '地点':
                    for i1 in i['facetValue'][:100]:
                        if i1['value'] not in \
                                ['筛选过的地点词列表1', '筛选过的地点词列表2']:
                            addressMonth[i1['value']] = i1['count']
        except:
            pass
        return addressWeek, addressMonth

    """
    热门分类(只有视频，音频未提供分类|周，月)
    """

    def popular_classification(self):
        dataWeek = self.dataWeek
        dataMonth = self.dataMonth
        dataWeek['queryCondition']['fieldConditionGroup']['fieldConditions'] \
            .append({"field": "type_",
                     "value": "model_sobey_smart_story",
                     "searchRelation": "and"})
        dataMonth['queryCondition']['fieldConditionGroup']['fieldConditions'] \
            .append({"field": "type_",
                     "value": "model_sobey_smart_story",
                     "searchRelation": "and"})
        videoTopWeek = {}
        videoTopMonth = {}
        audioTopWeek = {}
        audioTopMonth = {}
        try:
            res = rest.get_entityinfo_url(dataWeek)
            for i in res['extensionResults'][0]['values']:
                if i['facetShowName'] == '分类':
                    for i1 in i['facetValue'][:5]:
                        videoTopWeek[i1['value']] = i1['count']
            res = rest.get_entityinfo_url(dataMonth)
            for i in res['extensionResults'][0]['values']:
                if i['facetShowName'] == '分类':
                    for i1 in i['facetValue'][:5]:
                        videoTopMonth[i1['value']] = i1['count']
        except:
            pass
        return videoTopWeek, videoTopMonth, audioTopWeek, audioTopMonth

    """
    热门人物(周、月)
    """

    def popular_person(self):
        hotPeopleWeek = {}
        hotPeopleMonth = {}
        try:
            tempDict = {}
            res = rest.get_entityinfo_url(self.dataWeek)
            for i in res['extensionResults'][0]['values']:
                if i['facetShowName'] == '人物':
                    for i1 in i['facetValue']:
                        k = i1['value']
                        if len(k.split("(")) > 0:
                            k = k.split("(")[0]
                        v = i1['count']
                        if k in tempDict.keys():
                            tempDict[k] = tempDict[k] + v
                        else:
                            tempDict[k] = v
            tempDict = sorted(tempDict.items(), key=lambda x: x[1], reverse=True)
            if len(tempDict) >= 10:
                for i in range(10):
                    hotPeopleWeek[tempDict[i][0]] = tempDict[i][1]
            else:
                for i in range(len(tempDict)):
                    hotPeopleWeek[tempDict[i][0]] = tempDict[i][1]

            tempDict = {}
            res = rest.get_entityinfo_url(self.dataMonth)
            for i in res['extensionResults'][0]['values']:
                if i['facetShowName'] == '人物':
                    for i1 in i['facetValue']:
                        k = i1['value']
                        if len(k.split("(")) > 0:
                            k = k.split("(")[0]
                        v = i1['count']
                        if k in tempDict.keys():
                            tempDict[k] = tempDict[k] + v
                        else:
                            tempDict[k] = v
            tempDict = sorted(tempDict.items(), key=lambda x: x[1], reverse=True)
            if len(tempDict) >= 10:
                for i in range(10):
                    hotPeopleMonth[tempDict[i][0]] = tempDict[i][1]
            else:
                for i in range(len(tempDict)):
                    hotPeopleMonth[tempDict[i][0]] = tempDict[i][1]
        except:
            pass
        return hotPeopleWeek, hotPeopleMonth

    """
    入库数量(天、周、月、年)
    """

    def savedata_quantity(self):
        toyear = {}
        tomonth = {}
        toweek = {}
        today = {}
        for i in range(1, 13):
            toyear[i] = 0
        for i in range(1, int(self.monthEnd.split('-')[-1]) + 1):
            tomonth[i] = 0
        for i in range(1, 8):
            toweek[i] = 0
        for i in range(1, 25):
            today[i] = 0
        for x in self.sh_d_entitydata.find({}, {"dataregion": 1}):
            try:
                createDate = x['dataregion']['createDate_'].split(' ')[0]
                createDateTime = x['dataregion']['createDate_']
                createDateMonth = int(createDate.split('-')[1])
                createDateDay = int(createDate.split('-')[-1])
                createDateTimeStamp = int(time.mktime(time.strptime(createDateTime, "%Y-%m-%d %H:%M:%S")))
                weekStartTimeStamp = int(time.mktime(time.strptime(self.weekStart, "%Y-%m-%d")))
                weekEndTimeStamp = int(time.mktime(time.strptime(self.weekEnd + ' 23:59:59', "%Y-%m-%d %H:%M:%S")))

                if createDateMonth in toyear.keys():
                    toyear[createDateMonth] = toyear[createDateMonth] + 1
                if createDateMonth == int(self.today.split('-')[1]):
                    tomonth[createDateDay] = tomonth[createDateDay] + 1
                if weekEndTimeStamp > createDateTimeStamp > weekStartTimeStamp:
                    days = (createDateTimeStamp - weekStartTimeStamp) / 86400
                    days = math.ceil(days)
                    toweek[days] = toweek[days] + 1
                if self.today == createDate:
                    hour = int(createDateTime.split(' ')[1].split(':')[0])
                    today[hour] = today[hour] + 1
            except:
                pass
        return toyear, tomonth, toweek, today

    """
    出库数量(天、周、月、年)
    """

    def readdata_quantity(self):
        toyear = {}
        tomonth = {}
        toweek = {}
        today = {}
        for i in range(1, 13):
            toyear[i] = 0
        for i in range(1, int(self.monthEnd.split('-')[-1]) + 1):
            tomonth[i] = 0
        for i in range(1, 8):
            toweek[i] = 0
        for i in range(1, 25):
            today[i] = 0
        sql = 'select create_task_time from export_task'
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        for i in res:
            try:
                createDate = str(i[0]).split(' ')[0]
                createDateTime = str(i[0])
                createDateMonth = int(createDate.split('-')[1])
                createDateDay = int(createDate.split('-')[-1])
                createDateTimeStamp = int(time.mktime(time.strptime(createDateTime, "%Y-%m-%d %H:%M:%S")))
                weekStartTimeStamp = int(time.mktime(time.strptime(self.weekStart, "%Y-%m-%d")))
                weekEndTimeStamp = int(time.mktime(time.strptime(self.weekEnd + ' 23:59:59', "%Y-%m-%d %H:%M:%S")))
                if createDateMonth in toyear.keys():
                    toyear[createDateMonth] = toyear[createDateMonth] + 1
                if createDateMonth == int(self.today.split('-')[1]):
                    tomonth[createDateDay] = tomonth[createDateDay] + 1
                if weekEndTimeStamp > createDateTimeStamp > weekStartTimeStamp:
                    days = (createDateTimeStamp - weekStartTimeStamp) / 86400
                    days = math.ceil(days)
                    toweek[days] = toweek[days] + 1
                if self.today == createDate:
                    hour = int(createDateTime.split(' ')[1].split(':')[0])
                    today[hour] = today[hour] + 1
            except:
                pass
        return toyear, tomonth, toweek, today


test().start()
