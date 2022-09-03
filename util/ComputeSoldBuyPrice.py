import os
import pandas as pd
from util.Validation import get_code_data, get_format_day
from util.TransBaseData import main as update_data

if __name__ == "__main__":

    #刷新最新的数据
    update_data()
    #自选股所在的文件夹
    file_name = r"D:\tdx\T0002\blocknew\ZXG.blk"
    with open(file_name) as f:
        lines = list(map(str.strip, f.readlines()))

    #### [1-4]挂 -4.5%买入  [5-8] 挂-3.5%买入  [9-12]挂5%个点卖出
    res = []
    for str_code in lines[:20]:
        code = str_code[1:]
        #以任意基金作为拦截符，到了就停止
        if code[0] not in ("0", "6"):
            res.append([0, 0, 0,  0, 0, "", 0])
            continue
        # if code[0] == "0":
        #     query_code = "sz."+ code
        # else:
        #     query_code = "sh." + code
        # name = bs.query_stock_basic(code=query_code).code_name

        close = get_code_data(code)[:1]["CLOSE"].values[0]

        if len(res) <= 15:
            res.append([code, close, round(close*0.975, 2), round(close*0.965, 2), round(close*0.955, 2), round(close*0.945, 2), "买入", round(close*1.05, 2)])
            continue

        if len(res) > 15:
            res.append([code, 0, 0, 0,  0, 0, "卖出", round(close*1.05)])
            continue
    #输出为excel放到桌面
    #先删除前面的文件
    for i in range(10):
        file_name = r"C:\Users\alix\Desktop\stock_quantitative_transaction_{}.xlsx".format(get_format_day(0-i))
        if os.path.exists(file_name):
            os.remove(file_name)
    file_name = r"C:\Users\alix\Desktop\stock_quantitative_transaction_{}.xlsx".format(get_format_day(1))
    pd.DataFrame(res).to_excel(file_name, header=["代码", "当前价", "跌2.5%", "跌3.5%", "跌4.5%", "跌5.5%", "买卖信号", "涨5%"], index=False)
