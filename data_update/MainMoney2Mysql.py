# -*- coding: UTF-8 -*-
import os
import traceback
import pandas as pd

from util.LoadConfig import get_conf
from util.MysqlClient import MysqlClient
from util.BaseFunc import days_delta, get_format_day


class MainMoney2Mysql(object):

    def __init__(self):
        self.sql_client = MysqlClient()
        self.config = get_conf('tdx_data_path')

    def max_dt(self, code):
        sql = 'select max(dt) from date_main_money_k where code=%s'%code
        max_dt = self.sql_client.exec_sql(sql_type='select_one', sql=sql)[0]
        return max_dt

    def save_to_mysql(self, data_list: list) -> None:

        for d in data_list:
            try:
                write_sql = """INSERT 
                                INTO 
                                date_main_money_k(code, dt, level_4, level_3, level_2, level_1, sum, rate, up) 
                                VALUES(%s,%s,%f,%f,%f,%f,%f,%f,%f)
                            """ % (tuple(d))
                self.sql_client.exec_sql('insert_one', write_sql)
            except Exception as e:
                print(traceback.format_exc())

    def get_main_money_from_local(self, code: str) -> list:
        local_path = self.config['main_money_local_path']
        file_path = os.path.join(local_path, str(code)+'.csv')
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, header=0, encoding='utf-8-sig')
            df['代码'] = '1' + code
            df = df[['代码', '日期', '超大单净流入', '大单净流入',  '中单净流入', '小单净流入', '主力净流入', '主力净流入占比', '涨跌幅']]
            df['日期'] = df['日期'].apply(lambda x: str(x).replace("-", ""))
            df['超大单净流入'] = df['超大单净流入'].apply(lambda x: round(float(x)/10000, 2))
            df['大单净流入'] = df['大单净流入'].apply(lambda x: round(float(x) / 10000, 2))
            df['中单净流入'] = df['中单净流入'].apply(lambda x: round(float(x) / 10000, 2))
            df['小单净流入'] = df['小单净流入'].apply(lambda x: round(float(x) / 10000, 2))
            df['主力净流入'] = df['主力净流入'].apply(lambda x: round(float(x) / 10000, 2))

            # 去掉重复数据：
            max_dt_sql = """select 
                                max(dt) 
                            from 
                                date_main_money_k 
                            where 
                                code=%s
                        """ % code

            max_dt = self.sql_client.exec_sql(sql_type='select_one', sql=max_dt_sql)[0]

            if max_dt is None:
                return df.values.tolist()
            else:
                df = df[df['dt'] > max_dt]
                return df.values.tolist()

        else:
            return []

    def main_money_to_mysql(self, code: str,) -> None:
        sql_insert_list = self.get_main_money_from_local(code)
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
                self.main_money_to_mysql(code)
            except Exception as e:
                print(traceback.format_exc())
                print('代码：{} 刷新数据失败， 请稍后重试'.format(code))


if __name__ == "__main__":
    save_d = MainMoney2Mysql()
    save_d.main()

