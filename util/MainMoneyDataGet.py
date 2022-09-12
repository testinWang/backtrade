# -- coding: utf-8 --**
import os
import pandas as pd
import requests
import traceback
import random
from util.MultiPoolUtil import multi_pool_deal_partition
from util.BaseFunc import standard_dt, get_format_day, days_delta
from util.LoadConfig import get_conf


def gen_secid(stock_code: str) -> str:
    '''
    生成东方财富专用的secid
    Parameters
    ----------
    stock_code: 6 位股票代码
    Return
    ------
    str : 东方财富给股票设定的一些东西
    '''
    # 沪市指数
    if stock_code[:3] == '000':
        return f'1.{stock_code}'
    # 深证指数
    if stock_code[:3] == '399':
        return f'0.{stock_code}'
    # 沪市股票
    if stock_code[0] != '6':
        return f'0.{stock_code}'
    # 深市股票
    return f'1.{stock_code}'


def get_history_bill(stock_code: str, data_line: int) -> pd.DataFrame:
    '''
    获取多日单子数据
    -
    Parameters
    ----------
    stock_code: 6 位股票代码
    data_line: 返回最近几天的数据 6 返回最近6天数据
    Return
    ------
    DataFrame : 包含指定股票的历史交易日单子数据（大单、超大单等）
    '''

    EastmoneyHeaders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'http://quote.eastmoney.com/center/gridlist.html',
    }
    EastmoneyBills = {
        'f51': '日期',
        'f52': '主力净流入',
        'f53': '小单净流入',
        'f54': '中单净流入',
        'f55': '大单净流入',
        'f56': '超大单净流入',
        'f57': '主力净流入占比',
        'f58': '小单流入净占比',
        'f59': '中单流入净占比',
        'f60': '大单流入净占比',
        'f61': '超大单流入净占比',
        'f62': '收盘价',
        'f63': '涨跌幅'

    }
    fields = list(EastmoneyBills.keys())
    columns = list(EastmoneyBills.values())
    fields2 = ",".join(fields)
    secid = gen_secid(stock_code)
    params = (
        ('lmt', str(data_line)), # 最多返回数据条数
        ('klt', '101'),    # 101 表示日线
        ('secid', secid),
        ('fields1', 'f1,f2,f3,f7'),
        ('fields2', fields2)
    )
    params = dict(params)
    url = 'http://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get'
    times = 0
    while times <= 2:
        try:
            json_response = requests.get(url, headers=EastmoneyHeaders, params=params).json()
            data = json_response.get('data')
            if data is None:
                if secid[0] == '0':
                    secid = f'1.{stock_code}'
                else:
                    secid = f'0.{stock_code}'
                params['secid'] = secid

                json_response: dict = requests.get(url, headers=EastmoneyHeaders, params=params).json()
                data = json_response.get('data')
            if data is None:
                print('股票代码:', stock_code, '可能有误')
                times += 1
                continue

            if json_response is None:
                times += 1
                continue

            data = json_response['data']
            klines = data['klines']
            rows = []
            for _kline in klines:
                kline = _kline.split(',')
                rows.append(kline)
            df = pd.DataFrame(rows, columns=columns)
            # 日期表示进行标准化
            df['日期'] = df['日期'].apply(str).apply(standard_dt)

            if df['小单净流入'].sum() == 0:
                print('数据异常， 重试一次')
                times += 1
                continue
            else:
                return df
        except Exception as e:
            print(traceback.format_exc())
            times += 1

    # 最终没有结果返回空数据
    return pd.DataFrame(columns=columns)

# 多进程获取并写入csv文件：
def write_data(code_list: list, dt_line: int) -> None:
    """
    :param code_list:  查询股票的代码字典
    :param dt_line: 一次查询多少行数据
    :return: 自动写入csv 无需返回
    """
    for code in code_list:
        new_df = get_history_bill(code, dt_line)
        base_dir = r'E:\stock_data\main_money'
        file_name = os.path.join(base_dir, f'{code}.csv')
        if not os.path.exists(file_name):
            new_df.to_csv(file_name, index=False, encoding='utf-8-sig')
        else:
            origin_data_pd = pd.read_csv(file_name, header=0, encoding='utf-8-sig')
            origin_data_dt = set(origin_data_pd['日期'].values.tolist())
            new_data = new_df.values.tolist()
            save_new_data = []
            for d in new_data:
                if d[0] in origin_data_dt:
                    continue
                else:
                    save_new_data.append(d)

            if len(save_new_data) == 0:
                continue
            save_new_data_pd = pd.DataFrame(save_new_data, columns=origin_data_pd.columns)
            save_data_pd = pd.concat([origin_data_pd, save_new_data_pd], axis=0)
            save_data_pd.to_csv(file_name, index=False, encoding='utf-8-sig')
    print("成功写入本批数据")


# 读取主力资金数据：
def get_main_money_data_from_local(code: str, begin_dt: str, end_dt: str) -> pd.DataFrame or None:
    """
    :param code: 股票代码
    :param begin_dt: 开始时间
    :param end_dt: 结束时间
    :return:
    """
    base_dir = r'E:\stock_data\main_money'
    file_name = os.path.join(base_dir, f'{code}.csv')
    if not os.path.exists(file_name):
        print("没有当前股票信息，请更新数据")
        return None
    else:
        df = pd.read_csv(file_name, header=0, encoding='utf-8-sig')
        if df['小单净流入'].sum() == .0:
            print("本股票{}数据异常：获取所有数据为0 ，不参与回测计算".format(code))
            return None
        df['flag'] = df['日期'].apply(lambda x: 0 if begin_dt <= x <= end_dt else 1)
        df = df[df['flag'] == 0]
        return df


# 获取所有股票代码，#从通达信文件夹直接读取：
def get_stock_list():
    tdx_path = get_conf('tdx_data_path')
    sh_tdx_path = tdx_path['tdx_file_dir_sh']
    sz_tdx_path = tdx_path['tdx_file_dir_sz']
    save_local_path = tdx_path['main_money_local_path']
    sh_file_list = os.listdir(sh_tdx_path)
    sz_file_list = os.listdir(sz_tdx_path)
    all_file_list = set(sh_file_list + sz_file_list)
    code_list = [str(elem).strip()[2:8] for elem in all_file_list]
    # 只留沪深两市
    code_list = [elem for elem in code_list if elem.isdigit() and int(elem[0]) in (0, 3, 6)]

    return code_list


# 更新数据到mysql
def update_data():
    today = get_format_day(0, '-')
    save_data_path = get_conf('tdx_data_path')['main_money_local_path']
    files = os.listdir(save_data_path)
    sample_file = random.sample(files, 10)
    first_df = None
    for file in sample_file:
        try:
            file_name = os.path.join(save_data_path, file)
            df = pd.read_csv(file_name, header=0, encoding='utf-8-sig')
            if len(df) >= 1:
                first_df = df
                first_df = pd.concat([df, first_df])

        except Exception as e:
            pass

    local_max_dt = max(first_df['日期'].values.tolist())
    data_line = days_delta(today, local_max_dt)
    multi_pool_deal_partition(datas=all_code_list, func=write_data, cores=6, slice_size=30, args=data_line)


if __name__ == "__main__":
    all_code_list = get_stock_list()
    # 只在第一次使用
    # multi_pool_deal_partition(datas=all_code_list, func=write_data, cores=6, slice_size=30, args=150)
    update_data()
