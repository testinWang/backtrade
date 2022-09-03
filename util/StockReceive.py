#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import random
import pandas as pd
import smtplib
import easyquotation
import datetime
import time
from email.mime.text import MIMEText
from pytdx.hq import TdxHq_API
from email.header import Header
import traceback
api = TdxHq_API(auto_retry=True)
from util.TransBaseData import main
#全局变量
dict_code_ma = dict()
dict_code_last_close = dict()

#刷新本地数据
#main()

#存储已发送过股票的邮件次数
send_email_times = dict()

def get_format_day(numdays=0,sep = "-"):
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=numdays)
    n_days = now + delta
    return n_days.strftime("%Y{}%m{}%d".format(sep, sep))

def send_email(subject, text):
    mail_host = "smtp.qq.com"  # 设置的邮件服务器host必须是发送邮箱的服务器，与接收邮箱无关。
    # mail_user = "535085264@qq.com"  # qq邮箱登陆名
    # mail_pass = "qkjncuveufokcbea"  # 开启stmp服务的时候并设置的授权码，注意！不是QQ密码。
    # sender = '535085264@qq.com'  # 发送方qq邮箱
    # receivers = ['535085264@qq.com']  # 接收方qq邮箱
    qq_mail1 = "535085264@qq.com"
    mail_pass1 = "qkjncuveufokcbea"
    qq_mail2 = "1328660440@qq.com"
    mail_pass2 = "tejexorxzankjgba"
    mail_config_list = [(qq_mail1, mail_pass1, qq_mail1, qq_mail1), (qq_mail2, mail_pass2, qq_mail2, qq_mail2)]
    mail_user, mail_pass, sender, receivers = random.sample(mail_config_list, k=1)[0]
    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = Header("hailong", 'utf-8')  # 设置显示在邮件里的发件人
    message['To'] = Header("wowo", 'utf-8')  # 设置显示在邮件里的收件人
    message['Subject'] = Header(subject, 'utf-8')  # 设置主题和格式
    try_time = 0
    try:
        #最多重试五次
        if try_time > 1:
            return
        smtpobj = smtplib.SMTP_SSL(mail_host, 465)  # 本地如果有本地服务器，则用localhost ,默认端口２５,腾讯的（端口465或587）
        smtpobj.set_debuglevel(1)
        smtpobj.login(mail_user, mail_pass)  # 登陆QQ邮箱服务器
        smtpobj.sendmail(sender, receivers, message.as_string())  # 发送邮件
        print("邮件发送成功")
        smtpobj.quit()  # 退出
    except smtplib.SMTPException as e:
        print("Error:无法发送邮件")
        try_time += 1
        print(e)

def get_history_data_pytdx(code, MA_DAY = 20, start = 1):

    #先查表
    if code in dict_code_ma.keys():
        ma = dict_code_ma[code]
        last_close = dict_code_last_close[code]
        return ma, last_close
    with api.connect('119.147.212.81', 7709):
        """
        category: K线种类
            0 5分钟K线 1 15分钟K线 2 30分钟K线 
            3 1小时K线 4 日K线 5 周K线 6 月K线 
            7 1分钟 8 1分钟K线 9 日K线 10 季K线 11 年K线
        market: 市场代码 0:深圳，1:上海
        stockcode: 证券代码
        start: 指定的范围开始位置 0表示当天
        count: 用户要请求的 K 线数目，最大值为 800
        """
        if code[0] in ('0', '3'):
            market = 0
        else:
            market = 1
        data = api.get_security_bars(category=9, market=market, code=code, start=start, count=MA_DAY-1)
        pd_df = api.to_df(data)
        ma = pd_df['close'].mean()
        last_close = pd_df[-1:]['close'].values[0]

        # 对全局变量赋值 避免重复计算
        dict_code_last_close[code] = last_close
        dict_code_ma[code] = ma

        return ma, last_close


# 从本地文件中读取股票的历史数据并计算MA20， 获取指定代码号的股票上一日收盘价及对应的均线信息
def get_history_data(code, MA_DAY=20):
    """
    :param code: 股票代码：如：000001
    :return:  股票代码对应的数据，按照日期倒叙排好
    """
    #首选查内存，有直接取数据，读表计算
    if code in dict_code_ma.keys():
        ma = dict_code_ma[code]
        last_close = dict_code_last_close[code]
        return ma, last_close
    base_dir = r"E:\deeplearning\stock-data-validation\data\base_data_csv"
    code_data_file = os.path.join(base_dir, code + ".csv")
    code_data_df = pd.read_csv(code_data_file, names=["date", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"])
    code_data_df["date"] = code_data_df["date"].apply(int)
    code_data_df = code_data_df.sort_values(by=["date"], axis=0, ascending=False)[: MA_DAY-1]
    last_close = code_data_df.values.tolist()[0][4]
    ma = code_data_df["CLOSE"].mean()
    #对全局变量赋值 避免重复计算
    dict_code_last_close[code] = last_close
    dict_code_ma[code] = ma
    return ma, last_close


def get_now_data(code_list):
    # 新浪 ['sina'] 腾讯 ['tencent', 'qq']
    mail = random.sample(["tencent", "sina", "qq"], k=1)[0]
    try:
        quotation = easyquotation.use(mail)

        # 获取所有股票行情
        quotation.market_snapshot(prefix=False) # prefix 参数指定返回的行情字典中的股票代码 key 是否带 sz/sh 前缀
        # 单只股票
        # quotation.real(code) # 支持直接指定前缀，如 'sh000001'
        # 多只股票
        # quotation.stocks(['000001', '162411'])
        return quotation.stocks(code_list)

    except Exception as err:
        time_error = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("频繁请求：报错时间:{}".format(time_error))
        time.sleep(2)
        err_log = traceback.format_exc()
        print(str(err_log))
        return {}


# 读取自选股中历史数据
def get_zixuan_data():
    """
    :return: 返回战法对应的选股股票 key 为日期 如 20210714 value 为当天选出来的股票 一个list ； 如{"20210804":[000001,600003]}
    """
    # 自选文件夹
    data_file_dir = r"D:\tdx\T0002\blocknew"
    file_path = os.path.join(data_file_dir, "ZXG.blk")
    with open(file_path, encoding="utf-8") as f:
        code_str = f.readlines()
        # 只返回股票，不返回基金
        code_list = [str(elem).strip()[1:7] for elem in code_str if len(elem) > 2 and str(elem)[1] in ('0', '3', '6')]
    return code_list


if __name__ == "__main__":

    code_list = get_zixuan_data()

    have_code_list = []
    zixuan_list = []
    for i, code in enumerate(code_list):
        if code != "159949":
            have_code_list.append(code)
        else:
            if i < len(code_list)-1:
                zixuan_list = code_list[i+1:]
            break

    print("您的持仓股为：{}".format(",".join(have_code_list)))
    print("您的自选股为：{}".format(",".join(zixuan_list)))

    dt = get_format_day(0)
    morning_begin_time = dt + " " + "09:25:00"
    morning_end_time = dt + " " + "11:30:00"
    afternoon_begin_time = dt + " " + "13:00:00"
    afternoon_end_time = dt + " " + "15:00:00"
    time_stamp_begin_1 = time.mktime(time.strptime(morning_begin_time, '%Y-%m-%d %H:%M:%S'))
    time_stamp_end_1 = time.mktime(time.strptime(morning_end_time, '%Y-%m-%d %H:%M:%S'))
    time_stamp_begin_2 = time.mktime(time.strptime(afternoon_begin_time, '%Y-%m-%d %H:%M:%S'))
    time_stamp_end_2 = time.mktime(time.strptime(afternoon_end_time, '%Y-%m-%d %H:%M:%S'))

    # 9:25---15:00
    now_time = int(time.time())
    while True: # time_stamp_begin_1 < now_time < time_stamp_end_2:
        now_time = int(time.time())

        # 9:30 以前 or  15:00 以后
        while now_time < time_stamp_end_1 or now_time > time_stamp_begin_2:
            time.sleep(30)
            now_time = int(time.time())

        # 11:30 - 13:00
        while time_stamp_end_1 < now_time < time_stamp_begin_2:
            time.sleep(3)
            now_time = int(time.time())

        # 统计已发送邮件的次数，超过100 停止运行
        send_times = 0
        for _, t in send_email_times.items():
            send_times += t
        if send_times > 100:
            break

        ma_day = 20
        now_have_data_dict = get_now_data(have_code_list)
        if len(now_have_data_dict) == 0:

            time.sleep(10)
            continue
        # 持有的股票 ，涨幅超过五个点提醒， 跌幅超过三个点，跌破二十日线提醒
        for code in have_code_list:
            ma, last_close = get_history_data_pytdx(code, ma_day)
            now_price = now_have_data_dict[code]['now']
            name = now_have_data_dict[code]['name']
            ma_price = (ma * (ma_day - 1) + now_price) / ma_day

            if last_close*0.97 >= now_price:
                times = send_email_times.get(code, 0)
                if times <= 2:
                    send_email("【雪球邮件订阅】", "您的持仓：【{}】跌幅超过 3%， 请火速关注".format(name))
                else:
                    send_email_times[code] += 1

            if last_close*1.05 <= now_price:
                times = send_email_times.get(code, 0)
                if times <= 2:
                    send_email("【雪球邮件订阅】", "您的持仓：【{}】涨幅超过 5%，请火速关注".format(name))
                else:
                    send_email_times[code] += 1
            # 昨日还在均线之上，今日跌破提醒， 昨日就在均线之下 不用提醒
            if now_price <= ma_price and (last_close - ma_price)/ma_price >= 0.01:
                times = send_email_times.get(code, 0)
                if times <= 2:
                    send_email("【雪球邮件订阅】", "您的持仓：【{}】跌破均线，请火速关注".format(name))
                else:
                    send_email_times[code] += 1

        print("持仓监控完毕")
        # 自选股下跌提醒
        now_zixuan_data_dict = get_now_data(zixuan_list)

        if len(now_zixuan_data_dict) == 0:
            time.sleep(10)
            continue

        for code in zixuan_list:
            ma, last_close = get_history_data_pytdx(code, MA_DAY=ma_day)
            now_price = now_zixuan_data_dict[code]['now']
            open_price = now_zixuan_data_dict[code]['open']
            ma_price = (ma * (ma_day - 1) + now_price) / ma_day
            name = now_zixuan_data_dict[code]["name"]

            if now_price <= last_close * 0.95:
                times = send_email_times.get(code, 0)
                if times <= 3:
                    send_email("【雪球邮件订阅】", "您关注的【{}】跌幅超过 5%，请火速关注".format(name))
                else:
                    send_email_times[code] += 1

            if now_price <= last_close * 0.965:
                times = send_email_times.get(code, 0)
                if times == 0:
                    send_email("【雪球邮件订阅】", "您关注的【{}】跌幅超过 3.5%，请火速关注".format(name))
                else:
                    send_email_times[code] += 1

            if abs((now_price - ma_price)/ma_price) <= 0.02 and (last_close - ma_price)/ma_price >= 0.02:
                times = send_email_times.get(code, 0)
                if times <= 2:
                    send_email("【雪球邮件订阅】", "您关注的【{}】回落20均线附近， 请火速关注".format(name))
                else:
                    send_email_times[code] += 1
        now_time = int(time.time())
        time.sleep(1)
        print("自选监控完毕")

        # 下午三点之后, 九点半之前
        # now_time = int(time.time())
        # if now_time > time_stamp_end_2 or now_time < time_stamp_begin_1:
        #     print("非交易时间休息5分钟")
        #     time.sleep(60 * 5)

