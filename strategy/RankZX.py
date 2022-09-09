#本文件根据先验知识对自选股票进行排序
import os
import sys


class RankZX:
    def __init__(self):
        self.base_data_path = r'C:\zd_zyb\T0002\blocknew'
        self.zx_path = os.path.join(self.base_data_path, "ZXG.blk")

    # 读取自选列表
    def get_zx_code_list(self):
        with open(self.zx_path, encoding="utf-8") as f:
            code_str_line = f.readlines()
            # 自选股的存储第一位表示沪深，后六位才是真正的股票代码
            code_list = []
            for code_str in code_str_line:
                code_str = str(code_str).strip()
                if len(code_str) == 7:
                    market = code_str[0]
                    code = code_str[1:7]
                    code_dict = {'market': market, 'code': code}
                    code_list.append(code_dict)
        return code_list

    # 将重新计算好的code_list回写自选文件
    def rewrite_zx_data(self, code_list):
        with open(self.zx_path, encoding="utf-8", mode="w") as f:
            write_lines = []
            for code_dict in code_list:
                market = code_dict['market']
                code = code_dict['code']
                write_lines.append(str(market)+str(code))
            f.write('\n'.join(write_lines))
