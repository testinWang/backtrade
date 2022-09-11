import datetime


def get_format_day(days=0, sep="-") -> str:
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=days)
    n_days = now + delta
    return n_days.strftime("%Y{}%m{}%d".format(sep, sep))


# 标准化东方财富不规范的日期 2022-9-2 -> 2022-09-02
def standard_dt(str_dt: str) -> str:
    year, month, date = str_dt.split('-')
    if len(month) == 1:
        month = '0' + month
    if len(date) == 1:
        date = '0' + date
    return "-".join((year, month, date))


import datetime


def days_delta(str1, str2):
    date1 = datetime.datetime.strptime(str1[0:10], "%Y-%m-%d")
    date2 = datetime.datetime.strptime(str2[0:10], "%Y-%m-%d")
    num = (date1 - date2).days
    return num


def months_delta(str1, str2):
    year1 = datetime.datetime.strptime(str1[0:10], "%Y-%m-%d").year
    year2 = datetime.datetime.strptime(str2[0:10], "%Y-%m-%d").year
    month1 = datetime.datetime.strptime(str1[0:10], "%Y-%m-%d").month
    month2 = datetime.datetime.strptime(str2[0:10], "%Y-%m-%d").month
    num = (year1 - year2) * 12 + (month1 - month2)
    return num


if __name__ == "__main__":
    print(get_format_day(0, '-'))
    print(days_delta('2022-10-11', '2022-10-23'))