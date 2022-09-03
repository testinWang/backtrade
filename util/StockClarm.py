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
import numpy as np
from email.mime.text import MIMEText
from pytdx.hq import TdxHq_API
from email.header import Header
import traceback
api = TdxHq_API(auto_retry=True)
from util.TransBaseData import main
#全局变量
dict_code_ma_20 = dict()
dict_code_ma_10 = dict()
dict_code_last_close = dict()


#刷新本地数据
#main()


def get_format_day(numdays=0,sep = "-"):
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=numdays)
    n_days = now + delta
    return n_days.strftime("%Y{}%m{}%d".format(sep, sep))


def send_email(subject, text, receiver_tag=0):
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
    #mail_user, mail_pass, sender, receivers = random.sample(mail_config_list, k=1)[0]
    mail_user, mail_pass, sender, receivers = mail_config_list[receiver_tag]
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

def get_history_data_pytdx(code, start = 1):

    #先查表
    if code in dict_code_ma_20.keys():
        ma_20 = dict_code_ma_20[code]
        ma_10 = dict_code_ma_10[code]
        last_close = dict_code_last_close[code]
        return ma_20, ma_10, last_close
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
        data_20 = api.get_security_bars(category=9, market=market, code=code, start=start, count=20-1)
        pd_df_20 = api.to_df(data_20)
        ma_20 = pd_df_20['close'].mean()
        last_close = pd_df_20[-1:]['close'].values[0]

        data_10 = api.get_security_bars(category=9, market=market, code=code, start=start, count=10-1)
        pd_df_10 = api.to_df(data_10)
        ma_10 = pd_df_10['close'].mean()

        # 对全局变量赋值 避免重复计算
        dict_code_last_close[code] = last_close
        dict_code_ma_20[code] = ma_20
        dict_code_ma_10[code] = ma_10

        return ma_20, ma_10, last_close
#
# # 从本地文件中读取股票的历史数据并计算MA20， 获取指定代码号的股票上一日收盘价及对应的均线信息
# def get_history_data(code, MA_DAY=20):
#     """
#     :param code: 股票代码：如：000001
#     :return:  股票代码对应的数据，按照日期倒叙排好
#     """
#     #首选查内存，有直接取数据，读表计算
#     if code in dict_code_ma_20.keys():
#         ma = dict_code_ma_20[code]
#         last_close = dict_code_last_close[code]
#         return ma, last_close
#     base_dir = r"E:\deeplearning\stock-data-validation\data\base_data_csv"
#     code_data_file = os.path.join(base_dir, code + ".csv")
#     code_data_df = pd.read_csv(code_data_file, names=["date", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"])
#     code_data_df["date"] = code_data_df["date"].apply(int)
#     code_data_df = code_data_df.sort_values(by=["date"], axis=0, ascending=False)[: MA_DAY-1]
#     last_close = code_data_df.values.tolist()[0][4]
#     ma = code_data_df["CLOSE"].mean()
#     #对全局变量赋值 避免重复计算
#     dict_code_last_close[code] = last_close
#     dict_code_ma_20[code] = ma
#     return ma, last_close
#

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
        time.sleep(5)
        err_log = traceback.format_exc()
        print(str(err_log))
        return {}


# 读取自选股中历史数据
def get_code_list():
    """
    :return: 返回战法对应的选股股票 key 为日期 如 20210714 value 为当天选出来的股票 一个list ； 如{"20210804":[000001,600003]}
    """
    # 自选文件夹
    data_file_dir = r"D:\tdx\T0002\blocknew"
    file_path = os.path.join(data_file_dir, "ZXG.blk")
    with open(file_path, encoding="utf-8") as f:
        code_str = f.readlines()
        # 只返回股票，不返回基金
        all_code_list = [str(elem).strip()[1:7] for elem in code_str if len(elem) > 2 and
                     (str(elem)[1] in ('0', '3', '6') or str(elem)[1:7] == '159949')]

    have_code_list = all_code_list[:1]
    zixuan_list = all_code_list[1:]
    #后面放的不需要监控，以茅台作为 sep 直接截断
    sep_index = zixuan_list.index('600519')
    zixuan_list = zixuan_list[:sep_index]

    print("您的持仓股为：{}".format(",".join(have_code_list)))
    print("您的自选股为：{}".format(",".join(zixuan_list)))
    return have_code_list, zixuan_list

if __name__ == "__main__":

    dt = get_format_day(0)
    morning_begin_time = dt + " " + "09:25:00"
    morning_end_time = dt + " " + "11:30:00"
    afternoon_begin_time = dt + " " + "13:00:00"
    afternoon_end_time = dt + " " + "15:00:00"
    time_stamp_begin_1 = time.mktime(time.strptime(morning_begin_time, '%Y-%m-%d %H:%M:%S'))
    time_stamp_end_1 = time.mktime(time.strptime(morning_end_time, '%Y-%m-%d %H:%M:%S'))
    time_stamp_begin_2 = time.mktime(time.strptime(afternoon_begin_time, '%Y-%m-%d %H:%M:%S'))
    time_stamp_end_2 = time.mktime(time.strptime(afternoon_end_time, '%Y-%m-%d %H:%M:%S'))
    have_code_list, zixuan_list = get_code_list()

    chiyou_clarm_mt = np.zeros(shape=[len(have_code_list), 5], dtype=int)
    zixuan_clarm_mt = np.zeros(shape=[len(zixuan_list), 3], dtype=int)

    # 9:25---15:00
    while True:
        now_time = int(time.time())

        # 9:30以前 和 11:30 - 13:00
        while now_time < time_stamp_begin_1 or time_stamp_end_1 < now_time < time_stamp_begin_2:
            time.sleep(10)
            print("非开盘时间，请等待......")
            now_time = int(time.time())

        now_have_data_dict = get_now_data(have_code_list)
        if len(now_have_data_dict) == 0:
            time.sleep(10)
            continue
        # 持有的股票 ，涨幅超过五个点提醒， 跌幅超过三个点，跌破二十日线提醒
        for i, code in enumerate(have_code_list):
            last_ma_20, last_ma_10, last_close = get_history_data_pytdx(code)
            now_price = now_have_data_dict[code]['now']
            name = now_have_data_dict[code]['name']
            ma_price_20 = (last_ma_20 * (20 - 1) + now_price) / 20
            ma_price_10 = (last_ma_10 * (10 - 1) + now_price) / 10
            chiyou_clarm_name = ["跌幅超3%", "涨幅超过4%", "涨幅超过7%", '跌破10日均线', '跌破20日线']

            if now_price <= last_close*0.97:
                if chiyou_clarm_mt[i, 0] == 0:
                    send_email("【雪球邮件订阅】", "您持有的\n【{}】\n{}，请分批止盈".format(name, chiyou_clarm_name[0]))
                    chiyou_clarm_mt[i, 0] = 1

            if now_price >= last_close*1.04:
                if chiyou_clarm_mt[i, 1] == 0:
                    send_email("【雪球邮件订阅】", "您持有的\n【{}】\n{}，请分批止盈".format(name, chiyou_clarm_name[1]))
                    chiyou_clarm_mt[i, 1] = 1

            if now_price >= last_close * 1.07:
                if chiyou_clarm_mt[i, 2] == 0:
                    send_email("【雪球邮件订阅】", "您持有的\n【{}】\n{}，请分批止盈".format(name, chiyou_clarm_name[2]))
                    chiyou_clarm_mt[i, 2] = 1

            # 昨日还在均线之上，今日跌破提醒， 昨日就在均线之下 不用提醒
            if now_price <= ma_price_10 and (last_close - ma_price_10) / ma_price_10 >= 0.01:
                if chiyou_clarm_mt[i, 3] == 0:
                    send_email("【雪球邮件订阅】", "您持有的\n【{}】\n{}，请火速关注".format(name, chiyou_clarm_name[3]))
                    chiyou_clarm_mt[i, 3] = 1

            # 昨日还在均线之上，今日跌破提醒， 昨日就在均线之下 不用提醒
            if now_price <= ma_price_20 and (last_close - ma_price_20)/ma_price_20 >= 0.01:
                if chiyou_clarm_mt[i, 4] == 0:
                    send_email("【雪球邮件订阅】", "您持有的\n【{}】\n{}，请火速关注".format(name, chiyou_clarm_name[4]))
                    chiyou_clarm_mt[i, 4] = 1

        # 自选股下跌提醒
        now_zixuan_data_dict = get_now_data(zixuan_list)
        if len(now_zixuan_data_dict) == 0:
            time.sleep(10)
            continue
        for i, code in enumerate(zixuan_list):
            last_ma_20, last_ma_10, last_close = get_history_data_pytdx(code)
            now_price = now_zixuan_data_dict[code]['now']
            open_price = now_zixuan_data_dict[code]['open']
            ma_price_20 = (last_ma_20 * (20 - 1) + now_price) / 20
            ma_price_10 = (last_ma_10 * (10 - 1) + now_price) / 10
            name = now_zixuan_data_dict[code]["name"]
            zixuan_clarm_name = ["跌幅超5%", "跌至20日线附近", "跌至10日线附近"]
            if now_price <= last_close * 0.95:
                if zixuan_clarm_mt[i, 0] == 0:
                    send_email("【雪球邮件订阅】", "您关注的\n【{}】\n{}，请火速关注".format(name, zixuan_clarm_name[0]), receiver_tag=1)
                    zixuan_clarm_mt[i, 0] = 1

            if abs((now_price - ma_price_20)/ma_price_20) <= 0.01 and (last_close - ma_price_20)/ma_price_20 >= 0.01:

                if zixuan_clarm_mt[i, 1] == 0:
                    send_email("【雪球邮件订阅】", "您关注的\n【{}】\n{}，请火速关注".format(name, zixuan_clarm_name[1]), receiver_tag=1)
                    zixuan_clarm_mt[i, 1] = 1

            if abs((now_price - ma_price_10)/ma_price_10) <= 0.01 and (last_close - ma_price_10)/ma_price_10 >= 0.01:

                if zixuan_clarm_mt[i, 2] == 0:
                    send_email("【雪球邮件订阅】", "您关注的\n【{}】\n{}，请火速关注".format(name, zixuan_clarm_name[2]), receiver_tag=1)
                    zixuan_clarm_mt[i, 2] = 1

        now_time = int(time.time())
        time.sleep(5)
        # 三点之后 停止监控
        if now_time > time_stamp_end_2:
            print("下午三点啦，休市啦，监控结束")
            break