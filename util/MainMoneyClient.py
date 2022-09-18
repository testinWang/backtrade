# 查询数据主要通过 mysql查询
from util.MysqlClient import MysqlClient
from util.LoadConfig import get_conf


class MainMoneyClient(object):
    def __init__(self):
        self.mysql_client = MysqlClient()
        self.main_money_tale_name = get_conf('mysql_table')['main_money_k_table']

    def get_main_money_by_dt(self, code: str, begin_dt: str, end_dt: str) -> dict:

        # code 在mysql 中存储 前缀都增加了前缀 '1'
        # dt 存储格式如 '20220808'
        code = '1' + code
        if len(begin_dt) == 10:
            begin_dt = str(begin_dt).replace("-", "")
            end_dt = str(end_dt).replace("-", "")
        query_sql = """ 
        select 
           distinct * 
        from 
            %s 
        where 
        dt >= %s 
            and dt <=%s 
            and code = %s
        order by dt
        """ % (self.main_money_tale_name, begin_dt, end_dt, code)
        # print(query_sql)
        query_res = self.mysql_client.exec_sql(sql_type='select_list', sql=query_sql)
        res = dict()
        if query_res:

            columns = ['代码', '日期', '超大单净流入', '大单净流入',  '中单净流入', '小单净流入', '主力净流入', '主力净流入占比', '涨跌幅']
            for i, one_data in enumerate(query_res):
                dt = one_data[1]
                one_data_dict = dict(zip(columns, one_data))
                one_data_dict['idx'] = i
                res[dt] = one_data_dict
        else:
            print('当天没有主力资金交易数据，请刷新数据 并检查')
        return res


if __name__ == '__main__':
    test_util = MainMoneyClient()
    res_ = test_util.get_main_money_by_dt(begin_dt='20220904', end_dt='20220909', code='000001')
    print(res_)
