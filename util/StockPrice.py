

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
