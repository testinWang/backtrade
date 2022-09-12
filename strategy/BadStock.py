import datetime

from util.BaseFunc import get_format_day
from util.KDataClient import KDataClient
from util.MainMoneyClient import MainMoneyClient

kd_util = KDataClient()
main_money_util = MainMoneyClient()

class BadStock(object):

    def __init__(self, code):
        self.code = code


def valid(code: str, begin_dt: str, end_dt: str) -> str:
    today = get_format_day(0, '-')
    kd_data = kd_util.get_price_by_dt(code, dt=end_dt)
    main_money_data = main_money_util.get_main_money_by_dt(code, begin_dt, end_dt)
    # print(kd_data)
    # print(main_money_data)


# 策略一 有涨停但是持续阴跌的票
def yindie(code,):
    pass


# 策略二： 涨停后次日放巨量收阴线， 放最后， 巨量：超过涨停日成交量150%
def huge_yinxian(code):
    pass


# 策略三：连续三日内收阴，且三日没有一日最高涨幅超过3%的
def three_date_yinxian(code):
    pass


# 策略四：最近有摁地板，
def dieting(code):
    pass


# 连续三日下跌放巨量
def xiadie_huge_vol(code):
    pass


# 连续三日以上阳线，首次出现阴线
def three_yanxian(self, code):
    pass


if __name__ == "__main__":
    test_end_dt = get_format_day(-1, "-")
    test_begin_dt = get_format_day(-20, '-')

    valid('000001', test_begin_dt, test_end_dt)
