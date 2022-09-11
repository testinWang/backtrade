import os
import sys
from util.BaseFunc import get_format_day
from util.StockPrice import dt_price, zt_price


class Two10PercentRise(object):

    def __init__(self):
        pass

    @staticmethod
    def get_test_dt_list(n_days=10):
        return [get_format_day(0-i) for i in range(0, n_days)][::-1]




if __name__ == '__main__':
    print(Two10PercentRise.get_test_dt_list(10))




"""
{主板或者创业板两个涨停}
{主板涨停}
AA:=C<=H AND H=ZTPRICE(REF(C,1),0.1) AND NOT (CODELIKE('688') OR CODELIKE('300'));
{主板上 最高涨幅点在5-10个点涨幅 且 当天上涨}
AA1:=C>=REF(C,1) AND C>O AND H>ZTPRICE(REF(C,1),0.03) AND NOT (CODELIKE('688') OR CODELIKE('300'));
{创业板涨停}
CC:=C<=H AND H=ZTPRICE(REF(C,1),0.2) AND CODELIKE('30');
{创业板上 最高涨幅点在8-20个点涨幅 且 当天上涨}
CC1:=C>=ZTPRICE(REF(C,1),0.02) AND H>=ZTPRICE(REF(C,1),0.05) AND H<=ZTPRICE(REF(C,1),0.2) AND CODELIKE('30');
{市值小于300亿 且 上市时间超过十天}
TJ:=FINANCE(40)/100000000<500 AND FINANCE(42)>=50 AND MA(C,20)/C<=1.03; {市值小于500亿且上市超过10天}
AM:=AMOUNT>=600000000 OR VOL/CAPITAL*100>10;{成交量超过5亿或者换手率超过15%}
ZT2:=((COUNT(CC,12)>=1 AND COUNT(CC1,8)>=1) OR (COUNT(AA,8)=1 AND COUNT(AA1,8)>=1) OR COUNT(AA,10)>=2 OR COUNT(CC,10)>=2) AND TJ AND COUNT(AM,6)>=2;

{涨停回调}
MM:=C=H AND NOT (CODELIKE('688') OR CODELIKE('300')) AND H=ZTPRICE(REF(C,1),0.1); {一个涨停}
PP:=C<H AND NOT (CODELIKE('688') OR CODELIKE('300')) AND H=ZTPRICE(REF(C,1),0.1);
EE:=C=H AND CODELIKE('30') AND H=ZTPRICE(REF(C,1),0.2); {一个触达涨停}
LL:=ZTPRICE(REF(C,1),0.04); {昨日涨幅4%}
FF:=ZTPRICE(REF(C,1),0.06);
HH:=ZTPRICE(REF(C,1),0.095); {昨日涨幅9.5%}
DD:=C<=HH AND C>=LL AND H>=FF ; {涨幅5%-9%}
MAX_HH:=HHV(H,10); {最近的最高价}
NN:=(MAX_HH)/C>=1.08; {最近从高点回调10%以上}
ZT3:=((EXIST(MM,10) AND EXIST(DD,10)) OR COUNT(MM,10)>=2 OR COUNT(PP,10)>=2 OR COUNT(EE,10)>=1);

{主力资金}
TIMETJ:=MACHINEDATE<01230331;
ZHULI:=IF(TIMETJ,(L2_AMO(0,0)+L2_AMO(1,0)-(L2_AMO(0,1)+L2_AMO(1,1)))/10000,0);

ZT4:=REF(C,1)=ZTPRICE(REF(C,2),0.1) AND C>O AND H<ZTPRICE(REF(C,1),0.07) AND (REF(ZHULI,2)>10000 OR SUM(ZHULI,2)>2000) AND NOT (CODELIKE('688') OR CODELIKE('30'));


ZL:=EXIST(ZHULI>=8000,2) OR SUM(ZHULI,2)>5000 OR (COUNT(ZHULI>0,5)>=4 AND SUM(ZHULI,5)>2000);

XG: ((ZT2 OR ZT3) AND (ZL OR CODELIKE('30'))) OR COUNT(ZT4,3)>=1 ;
"""
