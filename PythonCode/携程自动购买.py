import re
import smtplib
import time
from email.mime.text import MIMEText
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import cv2
import pyzbar.pyzbar as pyzbar
import sys
import numpy as np
import math
import os

name = '梅向南'
idnumber = '460001199811171018'
phonenumber = '13208100273'
start_city = "成都"
end_city = "深圳"
start_time = "2020-05-29"
price_max = 800
fileName = "E:/yzm"


def login():
    # 等待登陆按钮加载点击
    login_load = WebDriverWait(driver, 20, 1).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[class="member-name"]')))
    if login_load:
        driver.find_element_by_css_selector('[class="member-name"]').click()
    # 等待扫码按钮加载点击
    login_load = WebDriverWait(driver, 20, 1).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[id="scanLogin"]')))
    if login_load:
        driver.find_element_by_id('scanLogin').click()

    # 登陆界面url
    nowurl = driver.current_url
    # 二维码显示
    qrload = re.compile('<div class="form_wrap" id="normalview" style="display: none;">')
    # 二维码过期
    qroverdue = re.compile('<div class="er_void" style="" id="erCodeExpire">')
    while 1:
        # 等待二维码加载完成截图
        for i in range(6):
            if len(qrload.findall(driver.page_source)) > 0:
                print("haveqr")
                # 二维码开始显示时间
                qr_start = time.time()
                # 截图文件名
                imgName = f"{time.strftime('%Y%m%d%H%M%S', time.localtime())}_{random.randint(1, 999)}"
                imgPath = f"{fileName}/{imgName}.png"
                if not os.path.exists(fileName):
                    os.makedirs(fileName)
                # 截图
                driver.get_screenshot_as_file(imgPath)
                if not os.path.exists(imgPath):
                    continue
                break
            else:
                print("二维码未加载完成")
                time.sleep(0.5)
        # 验证码还没超时
        if len(qroverdue.findall(driver.page_source)) == 0:
            # 读取截图
            img = cv2.imread(imgPath)
            # 获取二维码坐标
            barcodes = pyzbar.decode(img)
            if len(barcodes) >= 2:
                x, y, w, h = barcodes[0].rect
                x1, y1, w1, h1 = barcodes[1].rect
                if w > w1:
                    x, y, w, h = barcodes[1].rect
            else:
                x, y, w, h = barcodes[0].rect
            # 显示二维码
            cv2.imshow("im", img[y:y + h, x:x + w])
            # 二维码显示时间
            qr_showtime = int(qr_start + 61 - time.time())
            # 是否扫码
            for i in range(qr_showtime):
                if nowurl != driver.current_url:
                    cv2.destroyAllWindows()
                    return
                else:
                    cv2.waitKey(1000)
            continue
        # 验证码超时
        else:
            driver.find_element_by_id('refresh').click()
            continue


# 首页
def mian_web():
    DepartCityTextBox = 'DepartCity1TextBox'
    ArriveCityTextBox = 'ArriveCity1TextBox'
    DepartDateTextBox = 'DepartDate1TextBox'

    main_web = WebDriverWait(driver, 20, 1).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f"[id='{DepartCityTextBox}']")))
    if main_web:
        # 起飞城市
        while 1:
            if driver.find_element_by_id(DepartCityTextBox).get_attribute('value') != start_city:
                driver.find_element_by_id(DepartCityTextBox).click()
                driver.find_element_by_id(DepartCityTextBox).clear()
                driver.find_element_by_id(DepartCityTextBox).send_keys(start_city)
            else:
                driver.find_element_by_id(DepartCityTextBox).send_keys(Keys.ENTER)
                break
        time.sleep(1)
        # 到达城市
        while 1:
            if driver.find_element_by_id(ArriveCityTextBox).get_attribute('value') != end_city:
                driver.find_element_by_id(ArriveCityTextBox).click()
                driver.find_element_by_id(ArriveCityTextBox).clear()
                driver.find_element_by_id(ArriveCityTextBox).send_keys(end_city)
            else:
                driver.find_element_by_id(ArriveCityTextBox).send_keys(Keys.ENTER)
                break
        # ---------------------------判断时间是否输入缺失
        while 1:
            if driver.find_element_by_id(DepartDateTextBox).get_attribute('value') != start_time:
                driver.find_element_by_id(DepartDateTextBox).clear()
                driver.find_element_by_id(DepartDateTextBox).send_keys(start_time)

            else:
                driver.find_element_by_id(DepartDateTextBox).send_keys(Keys.ENTER)
                break


# 详情页
def fly_page():
    # ------------------------------------------------机票详情页------------------------------------------------------------
    # 判断机票页面是否加载
    airline_list = WebDriverWait(driver, 10, 1).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[class='search_table_header']")))
    # 判断价格排序，降序则点击排序按钮
    if airline_list:
        price_sort = driver.find_element_by_css_selector("[class='price-sort current']").get_attribute("data-ubt")
        if price_sort == 'c_sort_price_up':
            driver.find_element_by_css_selector("[class='price-sort current']").click()
    while 1:
        # 加载完成把页面拉到底部
        airline_info = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[class='search_box search_box_tag search_box_light Label_Flight']")))
        if airline_info:
            bottom_next_day = driver.find_element_by_css_selector('[class="page_neighbor"]')
            driver.execute_script("arguments[0].scrollIntoView();", bottom_next_day)
            time.sleep(1)
            # 把页面拉到顶部
            top_ctrip_logo = driver.find_element_by_css_selector('[class="ctriplogo"]')
            driver.execute_script("arguments[0].scrollIntoView();", top_ctrip_logo)
        # ---------------------------------------------------直飞航班信息--------------------------------------------------
        # 等待加载完成获取源码
        # airline_info = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='search_box search_box_tag search_box_light Label_Flight']")))
        # if airline_info:
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        # 航班列表
        direct_flight_list = list(soup.find_all('div', {'class': 'search_table_header'}))
        # ----------------------------------航班号规则------------------------
        aircode = []
        aircode_rule = re.compile("<span>[A-Z/0-9]{5,6}</span>")
        aircode_rule1 = re.compile("[A-Z/0-9]{5,6}")
        # ---------------------------------价格规则--------------------------------------
        air_price = []
        price_rule = re.compile(">[0-9]{3,4}<")
        price_rule1 = re.compile("[0-9]{3,4}")
        # -------------------------------时间规则---------------------------------------
        air_take_off_time = []
        air_take_off_time_min = []
        time_rule = re.compile('<div class="inb right">(.*?)</div>')
        time_rule1 = re.compile('[0-9]{2}:[0-9]{2}')
        # ------------------------机型规则（大航线不完全）-------------------------------------
        air_type = []
        air_size = []
        air_type_rule = re.compile("([\u4e00-\u9fa5]{2})")
        type_rule = re.compile('<span class="direction_black_border low_text" id=".*?">(.*?)</span>')
        type_rule1 = re.compile('<span class="direction_black_border low_text special_text" id=".*?">(.*?)</span>')
        # --------------------------------经停判断--------------------------------------------
        air_stopover = []
        stopover_rule = re.compile('<span class="stopover no-help">.*?</span>')
        # -----------------------------正则筛选数据-------------------------------------------
        for i in direct_flight_list:
            aircode.append(aircode_rule1.findall(str(aircode_rule.findall(str(i))))[0])
            air_price.append(price_rule1.findall(str(price_rule.findall(str(i))))[0])
            air_take_off_time.append(time_rule1.findall(str(time_rule.findall(str(i))))[0])
            # 获取机型
            if len(type_rule.findall(str(i))) == 1:
                air_type.append(type_rule.findall(str(i))[0])
            else:
                air_type.append(type_rule1.findall(str(i))[0])
            # 获取经停
            if len(stopover_rule.findall(str(i))) > 0:
                air_stopover.append(1)
            else:
                air_stopover.append(0)

        for i in range(len(air_type) - 1):
            j = air_take_off_time[i].split(":")
            air_take_off_time_min.append(int(j[0]) * 60 + int(j[1]))
            air_size.append(air_type_rule.findall(str(air_type[i]))[-1])
        # ----------------------------航班数大于1----------------------------------------------
        air_score = []
        if price_max > int(air_price[0]):
            # if len(aircode) > 1:
            # 列表变成int
            air_price = list(map(int, air_price))
            air_take_off_time_min = list(map(int, air_take_off_time_min))
            # 传入函数计算得分
            for i in range(len(air_type) - 1):
                output_score(air_price[i], air_size[i], air_take_off_time_min[i], aircode[i], air_stopover[i],
                             min(air_price), max(air_price), air_score)
            # 判断最高得分有多个
            re_element = []
            for i in enumerate(air_score):
                if i[1] == max(air_score):
                    re_element.append(i[0])
            # ----------输出最高得分航班
            # air_score_result = air_score.index(max(air_score))
            # print(aircode[air_score_result])
            # sys.exit()
            # 多个最高分
            if len(re_element) > 1:
                re_start_time = {}  # 重复得分时间
                re_abs14_time = {}  # 离14点的距离
                re_price = {}  # 重复得分价格
                for i in re_element:
                    re_start_time[i] = air_take_off_time_min[i]
                    re_abs14_time[i] = abs(14 * 60 - air_take_off_time_min[i])
                    re_price[i] = air_price[i]
                # 最靠近14点的航班
                print(aircode[min(re_abs14_time, key=re_abs14_time.get)])
                buy(aircode[min(re_abs14_time, key=re_abs14_time.get)],
                    air_price[min(re_abs14_time, key=re_abs14_time.get)])
            # 单个最高分
            else:
                # 权重值最大值索引
                air_score_result = air_score.index(max(air_score))
                print(aircode[air_score_result])
                buy(aircode[air_score_result], air_price[air_score_result])
                # break
        # ---------无航班
        else:
            print("无目标票价航班，等待60秒后再次刷新")
            time.sleep(60)
            continue


def output_score(air_price, air_type, air_time, air_code, air_stopover, min_price, max_price, air_score):
    type_score = 0
    time_score = 0
    com_score = 0
    top_aircom = ['CA', 'MU', 'CZ', 'HU', 'ZH', '3U', 'MF', 'SC', 'FM']
    cheap_aircom = ['AQ', 'PN', '8L', 'KN', 'GX', '9C']

    # 基础价格分
    if air_code[0:2] in cheap_aircom:
        # price_score = int(min_price) / int(air_price+80)
        price_score = 1 - ((150 + air_price - min_price) / (max_price - min_price))
    else:
        # price_score=int(min_price)/int(air_price)
        price_score = 1 - ((air_price - min_price) / (max_price - min_price))
    # 机型分
    if air_type == '大型':
        type_score = 1
    else:
        type_score = 0

    # 期望值u,最高点
    u = 14
    sig = math.sqrt(30)
    x = np.linspace(0, 23, 1440)
    y = np.exp(-(x - u) ** 2 / (2 * sig ** 2)) / (math.sqrt(2 * math.pi) * sig)
    time_score = y[air_time] * (1 / max(y))
    if air_time < 500 or air_time > 1260:
        price_score = price_score - (1 - ((air_price - min_price + 100) / (max_price - min_price)))

    # 航司分
    if air_code[0:2] in top_aircom:
        com_score = 1
    if air_code[0:2] in cheap_aircom:
        com_score = 0
    if air_code[0:2] not in top_aircom and air_code[0:2] not in cheap_aircom:
        com_score = 0.8

    # 经停分
    if air_stopover == 1:
        price_score = price_score * 0.98

    # 总分
    score = price_score * 0.75 + type_score * 0.05 + time_score * 0.1 + com_score * 0.1

    print(air_code + ':' + str(round(price_score, 4)) + '--' + str(round(time_score, 4)) + '--' + str(
        round(com_score, 4)) + ':' + str(round(score, 4)))
    air_score.append(round(score, 4))


def buy(code, price):
    time.sleep(1)
    # 点击订票按钮展开详情
    zz = re.compile(str(code) + '.[0-9]{5,15}.hide')
    rule = zz.findall(str(driver.page_source))
    target = driver.find_element_by_css_selector('[data-mark="' + rule[0] + '"]')
    # 聚焦订票按钮
    driver.execute_script("arguments[0].scrollIntoView();", target)
    driver.execute_script("window.scrollBy (0,-300)")
    button_load = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-mark="' + rule[0] + '"]')))
    if button_load:
        driver.find_element_by_css_selector('[data-mark="' + rule[0] + '"]').click()
    time.sleep(1)
    # 点击预订
    buybutton_rule1 = re.compile(
        'data-mark="' + code + '.{1,5}Normal.{1,10}' + str(price) + '.{20,30}=="')  # 预定按钮规则1，点击预定无二级选项（0416）
    buybutton_rule2 = re.compile('data-mark="' + code + '.*?hide"')  # 预定按钮规则2，点击预定有二级选项（0417）
    unbind_rule = re.compile('data-ubt="c_cabin_goBook_x_unbind"')  # 无捆绑优惠券销售
    # 判断预定按钮规则
    buybutton_path1 = buybutton_rule1.findall(str(driver.page_source))
    buybutton_path2 = buybutton_rule2.findall(str(driver.page_source))
    # 规则1，无二级预订按钮
    if len(buybutton_path1) > 0:
        driver.find_element_by_css_selector('[' + buybutton_path1[0] + ']').click()
        # print(buybutton_path1[0])
        # print(driver.find_element_by_css_selector('['+buybutton_path1[0]+']'))
    # 规则2，有二级预订按钮
    else:
        driver.find_element_by_css_selector('[' + buybutton_path2[0] + ']').click()
        # 二级预定按钮等待
        unbind_load = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-ubt="c_cabin_goBook_x_unbind"]')))
        if unbind_load:
            unbind_path = unbind_rule.findall(str(driver.page_source))
            driver.find_element_by_css_selector('[' + unbind_path[0] + ']').click()

    # 弹出重新搜索
    research = re.compile('<div .*? class="ui-popup ui-popup-modal ui-popup-show ui-popup-focus" .*?>')
    if len(research.findall(str(driver.page_source))) > 0:
        driver.back()
        fly_page()
    else:
        # 乘客姓名
        while 1:
            if driver.find_element_by_id('p_name_0').get_attribute('value') != name:
                driver.find_element_by_id('p_name_0').click()
                driver.find_element_by_id('p_name_0').clear()
                driver.find_element_by_id('p_name_0').send_keys(name)
            else:
                break
        # 乘客身份证
        while 1:
            if driver.find_element_by_id('p_card_no_0').get_attribute('value') != idnumber:
                driver.find_element_by_id('p_card_no_0').click()
                driver.find_element_by_id('p_card_no_0').clear()
                for i in idnumber:
                    driver.find_element_by_id('p_card_no_0').send_keys(i)
                    time.sleep(0.1)
            else:
                break
        # 乘客手机号
        while 1:
            if driver.find_element_by_id('p_cellphone_0').get_attribute('value') != phonenumber:
                driver.find_element_by_id('p_cellphone_0').click()
                driver.find_element_by_id('p_cellphone_0').clear()
                driver.find_element_by_id('p_cellphone_0').send_keys(phonenumber)
            else:
                break
        # 联系人手机号
        while 1:
            if driver.find_element_by_id('I_contact_phone').get_attribute('value') != phonenumber:
                driver.find_element_by_id('I_contact_phone').click()
                driver.find_element_by_id('I_contact_phone').clear()
                driver.find_element_by_id('I_contact_phone').send_keys(phonenumber)
            else:
                break
        # 点击下一步
        driver.execute_script("arguments[0].scrollIntoView();",
                              driver.find_element_by_css_selector('[class="copyright"]'))
        driver.find_element_by_css_selector('[id="J_saveOrder"]').click()
        # 不购买保险
        noinsurance_load = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[c-bind-change="onCancelInsurances()"]')))
        if noinsurance_load:
            driver.find_element_by_css_selector('[c-bind-change="onCancelInsurances()"]').click()
        # 点击同意下单
        driver.execute_script("arguments[0].scrollIntoView();",
                              driver.find_element_by_css_selector('[class="copyright"]'))
        driver.find_element_by_css_selector('[id="J_payment"]').click()
        email(price, code)
        driver.quit()
        sys.exit()
        return 0


def email(price, aircode):
    mailto_list = ['1079841211@qq.com']  # 收件人(列表)
    mail_host = "smtp.163.com"  # 使用的邮箱的smtp服务器地址
    mail_user = "13208100273"  # 用户名
    mail_pass = "123456sq"  # 授权码
    mail_postfix = "163.com"  # 邮箱的后缀，网易就是163.com
    me = "hello" + "<" + mail_user + "@" + mail_postfix + ">"  # 发件人
    msg = MIMEText(str(aircode) + ":" + str(price), _subtype='plain')  # 第一个为文本内容，第二个 plain 设置文本格式
    msg['Subject'] = "下单成功"  # 标题
    msg['From'] = me  # 发件人
    msg['To'] = ";".join(mailto_list)  # 将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)  # 连接服务器
        server.login(mail_user, mail_pass)  # 登录操作
        server.sendmail(me, mailto_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(e)
        return False


def display_mode(num):
    global driver
    if num == 0:
        driver = webdriver.Chrome()
    else:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.maximize_window()
    driver.get("http://flights.ctrip.com/")


# ------------------------------------------------携程首页-------------------------------------------------------------
display_mode(0)
# 登录
login()
# 判断首页是否打开
mian_web()
# 详情页
fly_page()
