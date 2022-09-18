from util.BaseFunc import between_dt_list
from util.MainMoneyClient import MainMoneyClient
main_money_client = MainMoneyClient()

# 计算涨停价
def zt_price(current_price: float, percent: float) -> float:
    up_price = current_price * (1 + percent)

    if up_price < 1:
        up_price_str = format(up_price, '0.4f')
        if up_price_str[-1] == '5':
            up_price = round(up_price + 0.0001, 3)
        else:
            up_price = round(up_price, 3)

    else:
        up_price_str = format(up_price, '0.3f')

        if up_price_str[-1] == '5':
            up_price = round(up_price + 0.001, 2)
        else:
            up_price = round(up_price, 2)

    return up_price


# 计算跌停价
def dt_price(current_price: float, percent: float) -> float:

    down_price = current_price * (1 - percent)

    if down_price < 1:
        down_price_str = format(down_price, '0.4f')
        if down_price_str[-1] == '5':
            down_price = round(down_price + 0.0001, 3)
        else:
            down_price = round(down_price, 3)

    else:
        down_price_str = format(down_price, '0.3f')

        if down_price_str[-1] == '5':
            down_price = round(down_price + 0.001, 2)
        else:
            down_price = round(down_price, 2)

    return down_price


# 计算上影线和下影线的长度
def yingxian(dict_price: dict) -> (float, float):
    """
    :param dict_price: 价格字典
    :return: 影线长度的百分比
    """
    high = dict_price['high']
    low = dict_price['low']
    open = dict_price['open']
    close = dict_price['close']

    up_yx = (high - max(open, close))/max(open, close)
    down_yx = .0 - (min(open, close) - low) / low

    return up_yx, down_yx


# 计算涨停的日期, 返回指定日期内的所有涨停日期
def zt_dt(code: str, dict_price_list: list) -> list:
    zt_list = list()

    if len(dict_price_list) <= 1:
        print("价格行情，数据小于等于1天， 请确认")
        return zt_list
    for i, dict_price in enumerate(dict_price_list):
        if i == 0:
            continue

        last_close = dict_price_list[i-1]
        if code[0] == '3' or code[:3] == '688':
            percent = 0.2
        else:
            percent = 0.1
        today_zt_price = zt_price(last_close, percent)
        if dict_price['close'] == today_zt_price:
            zt_list.append(dict_price['datetime'][:10])

    return zt_list


# 计算指定日期内的主力资金流向
def main_money_sum(code: str, begin_dt: str, end_dt: str) -> (float, float):
    between_dts = between_dt_list(begin_dt=begin_dt, end_dt=end_dt)
    main_money_dict = main_money_client.get_main_money_by_dt(code, begin_dt=begin_dt, end_dt=end_dt)
    res_amount = 0
    res_rate = 0
    for dt in between_dts:
        if dt in main_money_dict.keys():
            res_amount += main_money_dict[dt].get('主力净流入', 0)
            res_rate += main_money_dict[dt].get('主力净流入占比', 0)

    return res_amount, res_rate
