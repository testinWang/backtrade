import os
import datetime
import numpy as np
import pandas as pd
from decimal import Decimal

def get_format_day(numdays=0):
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=numdays)
    n_days = now + delta
    return n_days.strftime("%Y%m%d")

# 读取自选股中历史数据
def get_zixuan_data():
    """
    :return: 返回战法对应的选股股票 key 为日期 如 20210714 value 为当天选出来的股票 一个list ； 如{"20210804":[000001,600003]}
    """
    ## 自选文件夹
    formula_select_data_file_dir = r"C:\zd_zyb\T0002\blocknew"
    file_list = os.listdir(formula_select_data_file_dir)
    dic_date_2_code_list = dict()
    for file in file_list:
        #战法保存文件夹对应命名前缀
        if not file[:3] == "202":
            continue
        file_path = os.path.join(formula_select_data_file_dir, file)
        date = file[:8]
        with open(file_path, encoding="utf-8") as f:
            code_str = f.readlines()
            code_list = [str(elem).strip()[1:7] for elem in code_str if len(elem)>2]
            dic_date_2_code_list[date] = code_list
    return dic_date_2_code_list


# 获取指定代码号的股票信息
def get_code_data(code):
    """
    :param code: 股票代码：如：000001
    :return:  股票代码对应的数据，按照日期倒叙排好
    """
    base_dir = r"E:\deeplearning\stock-data-validation\data\base_data_csv"
    code_data_file = os.path.join(base_dir, code + ".csv")
    code_data_df = pd.read_csv(code_data_file, names=["date", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"])
    code_data_df["date"] = code_data_df["date"].apply(int)
    code_data_df = code_data_df.sort_values(by=["date"], axis=0, ascending=False)[:200]
    return code_data_df

# 对每只股票进行分析
def analyse_stock(dic_date_2_code_list):
    """
    :param dic_date_2_code_list:  key 为 日期
    :return:
    """
    up_rate = []
    down_rate = []
    for date, code_list in dic_date_2_code_list.items():
        for code in code_list:
            date = int(date)
            one_code_data_df = get_code_data(code)
            today_data_df = one_code_data_df[one_code_data_df["date"] == date]
            # df 已经根据日期倒排，所以将当日之前的数据去掉，分析用不着

            one_code_data_df = one_code_data_df[one_code_data_df["date"] > date]
            # 取当天之后的最近的五天数据进行分析
            one_code_data_df = one_code_data_df[:-6]
            if len(one_code_data_df) < 5:
                continue
            today_close = today_data_df["CLOSE"].values.tolist()[0]
            five_day_high = one_code_data_df["HIGH"].values.tolist()
            three_day_low = one_code_data_df["LOW"][:-1].values.tolist()
            highest_rate = max(five_day_high)/today_close - 1
            lowest_rate = min(three_day_low)/today_close - 1
            up_rate.append(float(Decimal(highest_rate).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")))
            down_rate.append(float(Decimal(lowest_rate).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")))
    return up_rate, down_rate

# 统计股票对应的


if __name__ == "__main__":
    dic_date_2_code_list = get_zixuan_data()
    print(dic_date_2_code_list)
    up_rate, down_rate = analyse_stock(dic_date_2_code_list)
    # 统计涨跌幅度分布
    up_rate = pd.Series(up_rate)
    down_rate = pd.Series(down_rate)
    up_rate_dict = dict(up_rate.value_counts())
    down_rate_dict = dict(down_rate.value_counts())
    up_pair = sorted(up_rate_dict.items(), key=lambda x: x[1], reverse=True)
    down_pair = sorted(down_rate_dict.items(), key=lambda x: x[1], reverse=True)

    #过滤极端情况
    up_pair = [pair for pair in up_pair if not (pair[0] > 0.30 or pair[1] < 40)]
    down_pair = [pair for pair in down_pair if not (pair[0] > 0.00 or pair[1] < 35 or pair[0] < -0.09)]
    print(up_pair)
    print(down_pair)
    up_avg = sum([pair[0]*pair[1] for pair in up_pair])/sum([pair[1] for pair in up_pair])
    down_avg = sum([pair[0]*pair[1] for pair in down_pair])/sum([pair[1] for pair in down_pair])
    print(up_avg)
    print(down_avg)





