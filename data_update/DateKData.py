# -*- coding: UTF-8 -*-
import os
import traceback

from pytdx.hq import TdxHq_API
from util.LoadConfig import get_conf
from util.MysqlClient import MysqlClient
from util.BaseFunc import days_delta, get_format_day
api = TdxHq_API(auto_retry=True)


class DateKData(object):

    def __init__(self):
        self.sql_client = MysqlClient()

    def save_to_mysql(self, data_list: list) -> None:

        for d in data_list:
            try:
                write_sql = """
                            INSERT 
                            INTO 
                            date_k(code, dt, open, close, high, low, amount, vol) 
                            VALUES(%s,%s,%f,%f,%f,%f,%f,%f)
                            """ % (tuple(d))
                self.sql_client.exec_sql('insert_one', write_sql)
                print(write_sql)

            except Exception as e:
                print(traceback.format_exc())

    def get_data_tdx(self, code: str, start=0, count=20, max_dt=None) -> list:
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
            data = api.get_security_bars(category=9, market=market, code=code, start=start, count=count)
            pd_df = api.to_df(data)
            pd_df['code'] = '1' + code
            pd_df = pd_df[["code", 'datetime', 'open', 'close', 'high', 'low', 'amount', 'vol']]
            pd_df['datetime'] = pd_df['datetime'].apply(lambda x: str(x).split(" ")[0].replace("-", ""))
            pd_df['amount'] = pd_df['amount'].apply(lambda x: round(float(x)/10000, 3))
            pd_df['vol'] = pd_df['vol'].apply(lambda x: round(float(x) / 10000, 3))

        if max_dt is None:
            return pd_df.values.tolist()
        else:
            max_dt = max_dt[0]
            pd_df = pd_df[pd_df['dt'] > max_dt]
            return pd_df.values.tolist()

    def stock_to_mysql(self, code: str, start=0) -> None:

        max_dt_sql = """select 
                                    max(dt) 
                                from 
                                    date_k 
                                where 
                                    code=%s
                            """ % code

        max_dt = self.sql_client.exec_sql(sql_type='select_one', sql=max_dt_sql)[0]

        if max_dt is None:
            count = 100
        else:
            today = get_format_day(0, "-")
            format_mysql_save_max_dt = max_dt[:4] + "-" + max_dt[4:6] + "-" + max_dt[6:8]
            count = days_delta(today, format_mysql_save_max_dt)

        if count == 0:
            print('今天已经更新， 无需再更新')
            return

        sql_insert_list = self.get_data_tdx(code, start=start, count=count, max_dt=max_dt)
        if len(sql_insert_list) == 0:
            return

        self.save_to_mysql(sql_insert_list)

    def main(self):
        tdx_path = get_conf('tdx_data_path')
        sh_tdx_path = tdx_path['tdx_file_dir_sh']
        sz_tdx_path = tdx_path['tdx_file_dir_sz']
        sh_files = os.listdir(sh_tdx_path)
        sz_files = os.listdir(sz_tdx_path)
        all_files = sh_files + sz_files
        for file in set(all_files):
            # 股票代码
            code = file[2:8]
            print(code)
            if code[0] not in ['0', '3', '6']:
                continue
            try:
                self.stock_to_mysql(code, start=0)
            except Exception as e:
                print(traceback.format_exc())
                print('代码：{} 刷新数据失败， 请稍后重试'.format(code))


if __name__ == "__main__":
    save_d = DateKData()
    save_d.main()

