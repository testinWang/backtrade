#!/usr/bin/python
# -*- coding: utf-8 -*-
from pytdx.hq import TdxHq_API


class StockDataGet:
    def __init__(self):
        self.tdx_ip = '119.147.212.81'
        self.tdx_port = 7709
        self.api = TdxHq_API(auto_retry=True)

    @staticmethod
    def code_to_market(code):
        """
        :param code: 股票代码
        :return: 沪市或者深市
        """
        if code[0] in ('0', '3'):
            market = 0
        else:
            market = 1
        return market

    def get_k(self, code, start=0, count=1, category=9):
        """
        :param code: 股票代码
        :param start: 指定的范围开始位置 0表示当天
        :param count: 用户要请求的 K 线数目，最大值为 800
        :param category: K线种类
            0 5分钟K线 1 15分钟K线 2 30分钟K线
            3 1小时K线 4 日K线 5 周K线 6 月K线
            7 1分钟 8 1分钟K线 9 日K线 10 季K线 11 年K线
        :return: 返回开始日期到结束日期的股票的数据，pd.dataframe 格式
        """
        market = self.code_to_market(code)
        data = self.api.get_security_bars(category=category, market=market, code=code, start=start, count=count)
        pd_df = self.api.to_df(data)
        return pd_df