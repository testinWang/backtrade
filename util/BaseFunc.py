import datetime
import time


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


def days_delta(end_dt: str, begin_dt: str) -> int:
    if len(end_dt) == 8:
        end_dt = end_dt[:4] + "-" + end_dt[4:6] + "-" + end_dt[6:8]
    if len(begin_dt) == 8:
        begin_dt = begin_dt[:4] + "-" + begin_dt[4:6] + "-" + begin_dt[6:8]
    date1 = datetime.datetime.strptime(end_dt[0:10], "%Y-%m-%d")
    date2 = datetime.datetime.strptime(begin_dt[0:10], "%Y-%m-%d")
    num = (date1 - date2).days
    return num


def months_delta(str1, str2):
    year1 = datetime.datetime.strptime(str1[0:10], "%Y-%m-%d").year
    year2 = datetime.datetime.strptime(str2[0:10], "%Y-%m-%d").year
    month1 = datetime.datetime.strptime(str1[0:10], "%Y-%m-%d").month
    month2 = datetime.datetime.strptime(str2[0:10], "%Y-%m-%d").month
    num = (year1 - year2) * 12 + (month1 - month2)
    return num


def between_dt_list(begin_dt: str, end_dt: str) -> list:
    nums = days_delta(end_dt, begin_dt)
    dt_list = list()
    for i in range(nums+1):
        now = datetime.datetime.strptime(end_dt + ' ' + '00:00:00', "%Y-%m-%d %H:%M:%S")
        delta = datetime.timedelta(days=i - nums)
        n_days = now + delta
        str_dt = n_days.strftime("%Y-%m-%d")

        dt_list.append(str_dt)
    return dt_list


if __name__ == "__main__":
    print(get_format_day(0, '-'))
    print(days_delta('2022-08-23', '2022-08-11'))
    print(between_dt('2022-08-11', '2022-08-23'))

