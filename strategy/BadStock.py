import datetime
from util.StockDataGet import StockDataGet


def get_format_day(numdays=0, sep='-') -> str:
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=numdays)
    n_days = now + delta
    return n_days.strftime("%Y{}%m{}%d".format(sep, sep))

# 策略一 有涨停但是持续阴跌的票
def yindie(code):
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
