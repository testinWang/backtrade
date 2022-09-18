



# 上影线和下影线
def yingxian(dict_price: dict) -> (bool, float):
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



