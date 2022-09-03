import os
import struct
import datetime

def stock_csv(tdx_file, save_csv_file):

    with open(tdx_file, 'rb') as f:
        file_object = open(save_csv_file, mode="w")
        while True:
            stock_date = f.read(4)
            stock_open = f.read(4)
            stock_high = f.read(4)
            stock_low = f.read(4)
            stock_close = f.read(4)
            stock_amount = f.read(4)
            stock_vol = f.read(4)
            stock_reservation = f.read(4)

            # date,open,high,low,close,amount,vol,reservation

            if not stock_date:
                break
            stock_date = struct.unpack("l", stock_date)     # 4字节 如20091229
            stock_open = struct.unpack("l", stock_open)     #开盘价*100
            stock_high = struct.unpack("l", stock_high)     #最高价*100
            stock_low= struct.unpack("l", stock_low)        #最低价*100
            stock_close = struct.unpack("l", stock_close)   #收盘价*100
            stock_amount = struct.unpack("f", stock_amount) #成交额
            stock_vol = struct.unpack("l", stock_vol)       #成交量
            stock_reservation = struct.unpack("l", stock_reservation) #保留值

            date_format = datetime.datetime.strptime(str(stock_date[0]),'%Y%M%d') #格式化日期
            list= date_format.strftime('%Y%M%d')+","+str(stock_open[0]/100)+","+str(stock_high[0]/100.0)+","+str(stock_low[0]/100.0)+","+str(stock_close[0]/100.0)+","+str(stock_vol[0])+"\n"
            file_object.writelines(list)
        file_object.close()

def main():
    # 上海证券交易所股票目录
    tdx_file_dir_sh = r"D:\tdx\vipdoc\sh\lday"
    # 深圳证券交易所股票目录
    tdx_file_dir_sz = r"D:\tdx\vipdoc\sz\lday"
    save_flie_dir = r"E:\deeplearning\stock-data-validation\data\base_data_csv"
    # if os.path.exists(save_flie_dir):
    #     print(True)
    file_list_sh = os.listdir(tdx_file_dir_sh)[:1]
    for file in file_list_sh:
        tdx_file = os.path.join(
            tdx_file_dir_sh, file)
        # 股票代码
        code = file[0:8]
        if not (str(code[2:4]) == "60" and code[:2] == "sh"):
            continue
        save_csv_file = os.path.join(save_flie_dir, code[2:8] + ".csv")
        stock_csv(tdx_file, save_csv_file)

    file_list_sz = os.listdir(tdx_file_dir_sz)[:1]
    for file in file_list_sz:
        tdx_file = os.path.join(tdx_file_dir_sz, file)
        # 股票代码
        code = file[0:8]
        if not (str(code[2:4]) == "00" and code[:2] == "sz"):
            continue
        save_csv_file = os.path.join(save_flie_dir, code[2:8] + ".csv")
        stock_csv(tdx_file, save_csv_file)

if __name__ == "__main__":
    #基础数据落入到自己所需要的格式csv中
    main()



