# -*- coding: UTF-8 -*-
import os
import traceback
import time

from pytdx.hq import TdxHq_API
from util.LoadConfig import get_conf
from util.BaseFunc import days_delta, get_format_day


class KDataClient(object):

    def __init__(self):
        self.api = TdxHq_API(auto_retry=True)
        self.config = get_conf('tdx_data_url')

    @staticmethod
    def get_market(code: str) -> int:
        if code[0] in ('0', '3'):
            market = 0
        else:
            market = 1
        return market

    def get_price_by_dt(self, code, dt: str, left=100, right=100, only_all=False) -> dict:

        # 预估计算日期距离当天的时间
        today = get_format_day(0, '-')
        delta_days = days_delta(today, dt)
        with self.api.connect(self.config['ip'], int(self.config['port'])):
            try:
                market = self.get_market(code)
                start = max(int(delta_days/7 * 5) - right, 0)
                data = self.api.get_security_bars(category=9, market=market, code=code, start=start, count=left)
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
                res = dict()
                res['whole_data'] = data
                res['current_dt_data'] = dict()
                if only_all:
                    return res
                else:

                    for order_dict in data:
                        if str(order_dict['datetime']).split(" ")[0] == dt:
                            res['current_dt_data'] = dict(order_dict)
                            break
                    if len(res['current_dt_data']) == 0:
                        print('您查找的日期不存在交易数据')
                    return res

            except Exception as e:
                print(traceback.format_exc())

    # 获取当前日期 前第几天数据： 通达信REF功能

    def get_data_forward_ref(self, code: str, dt: str, forward_nums: int) -> dict:

        data = self.get_price_by_dt(dt=dt, code=code, only_all=True)

        order_dict_list = data['whole_data']
        dt_list = [elem['datetime'].split(' ')[0] for elem in order_dict_list]
        dt_2_id_dict = dict(zip(dt_list, range(len(dt_list))))

        dt_id = dt_2_id_dict[dt]
        res_id = dt_id - forward_nums
        res = dict()
        res['whole_data'] = data['whole_data']
        res['current_data'] = order_dict_list[res_id]
        return res

    # 计算均线
    def ma(self, code: str, dt: str, nums: int) -> int:
        data = self.get_price_by_dt(dt=dt, code=code, only_all=True)
        order_dict_list = data['whole_data']
        dt_list = [elem['datetime'].split(' ')[0] for elem in order_dict_list]
        dt_2_id_dict = dict(zip(dt_list, range(len(dt_list))))

        end_id = dt_2_id_dict[dt]
        begin_id = end_id - nums
        if begin_id < 0:
            print('左侧数据不够用， 请调大get_price_by_dt参数left')
            return 0
        return sum([elem['close']  for elem in data[begin_id:end_id]])/nums


if __name__ == "__main__":
    save_d = KDataClient()
    time_begin = time.time()
    print(save_d.get_price_by_dt('000001', '2022-05-05'))
    # print(save_d.get_data_forward_ref('000001', '2022-05-05', forward_nums=2))
    print(time.time()-time_begin)
