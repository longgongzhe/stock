# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 10:57:02 2019

@author: yangwenlong
"""

import tushare as ts
import talib as ta
import numpy as np
import pandas as pd
import os,time,sys,re,datetime
import csv
import scipy

pd.set_option('display.max_columns',20)

#首先是获取沪深两市的股票列表
#这里得到是对应的dataframe数据结构，它是类似于excel中一片数据的数据结构，有这些列：code,代码 name,名称 industry,所属行业 area,地区 pe,市盈率 outstanding,流通股本 totals,总股本(万) totalAssets,总资产(万)liquidAssets,流动资产 fixedAssets,固定资产 reserved,公积金 reservedPerShare,每股公积金 eps,每股收益 bvps,每股净资 pb,市净率 timeToMarket,上市日期
def Get_Stock_List():
    df = ts.get_stock_basics()
    df = df[df.timeToMarket<20120101]
    df=df[~df.name.str.contains('ST')]
#    df.to_csv('D:\\ha\\haan\\stock.csv',encoding='gbk')#选择保存   
    return df

 

#然后定义通过MACD判断买入卖出
def Get_MACD(df_Code):
    operate_array=[]
    for code in df_Code.index:
# 获取每只股票的历史价格和成交量 对应的列有index列,0 - 6列是 date：日期 open：开盘价 high：最高价 close：收盘价 low：最低价 volume：成交量 price_change：价格变动 p_change：涨跌幅
# 7-12列是 ma5：5日均价 ma10：10日均价 ma20:20日均价 v_ma5:5日均量v_ma10:10日均量 v_ma20:20日均量
        
        df = ts.get_hist_data(code,start='2018-11-20')
        
        if df is None:
            df_Code=df_Code.drop(index=code)
            continue
        if df.empty:
            df_Code=df_Code.drop(index=code)
            continue
#        print(df)
        print(code)
#        print(df.shape)
        
        dflen = df.shape[0]
        operate = 0
        if dflen>35:
            dflen = df.shape[1]
            
            df['macd'], df['macdsignal'], df['macdhist'] = ta.MACD(np.array(df.close), fastperiod=12, slowperiod=26, signalperiod=9)
            df=df.dropna(axis=0)
            macd=df.macd
            macdsignal=df.macdsignal
            macdhist=df.macdhist
#            macd, macdsignal, macdhist = ta.MACD(np.array(df.close), fastperiod=12, slowperiod=26, signalperiod=9)
            
                   
            SignalMA5 = ta.MA(macdsignal, timeperiod=5, matype=0)
            SignalMA10 = ta.MA(macdsignal, timeperiod=10, matype=0)
            SignalMA20 = ta.MA(macdsignal, timeperiod=20, matype=0)
#在后面增加3列，分别是13-15列，对应的是 DIFF  DEA  DIFF-DEA       
            df['macd']=pd.Series(macd,index=df.index) #DIFF
            df['macdsignal']=pd.Series(macdsignal,index=df.index)#DEA
            df['macdhist']=pd.Series(macdhist,index=df.index)#DIFF-DEA

            MAlen = len(SignalMA5)
            #2个数组 1.DIFF、DEA均为正，DIFF向上突破DEA，买入信号。 2.DIFF、DEA均为负，DIFF向下跌破DEA，卖出信号。

            if df.iat[(dflen-1),13]>0:
                if df.iat[(dflen-1),14]>0:
                    if df.iat[(dflen-1),13]>df.iat[(dflen-1),14]:
                        operate = operate + 1#买入
            else:
                if df.iat[(dflen-1),14]<0:
                    if df.iat[(dflen-1),13]<df.iat[(dflen-1),14]:
                        operate = operate - 1#卖出
       
            #3.DEA线与K线发生背离，行情反转信号。
            if df.iat[(dflen-1),7]>=df.iat[(dflen-1),8] and df.iat[(dflen-1),8]>=df.iat[(dflen-1),9]:#K线上涨
                if SignalMA5[MAlen-1]<=SignalMA10[MAlen-1] and SignalMA10[MAlen-1]<=SignalMA20[MAlen-1]: #DEA下降
                    operate = operate - 1
            elif df.iat[(dflen-1),7]<=df.iat[(dflen-1),8] and df.iat[(dflen-1),8]<=df.iat[(dflen-1),9]:#K线下降
                if SignalMA5[MAlen-1]>=SignalMA10[MAlen-1] and SignalMA10[MAlen-1]>=SignalMA20[MAlen-1]: #DEA上涨
                    operate = operate + 1
               
       
            #4.分析MACD柱状线，由负变正，买入信号。
            if df.iat[(dflen-1),15]>0 and dflen >30 :
                for i in range(1,26):
                    if df.iat[(dflen-1-i),15]<=0:#
                        operate = operate + 1
                        break
            #由正变负，卖出信号   
            if df.iat[(dflen-1),15]<0 and dflen >30 :
                for i in range(1,26):
                    if df.iat[(dflen-1-i),15]>=0:#
                        operate = operate - 1
                        break

               
        operate_array.append(operate)        
    df_Code['MACD']=pd.Series(operate_array,index=df_Code.index)   
    return df_Code

 

#输出CSV文件，其中要进行转码，不然会乱码
def Output_Csv(df,Dist):
    TODAY = datetime.date.today()
    CURRENTDAY=TODAY.strftime('%Y-%m-%d')
#    reload(sys)
#    sys.setdefaultencoding( "gbk" )
    df.to_csv(Dist+CURRENTDAY+'stock.csv',encoding='gbk')#选择保存   

 

def Close_machine():
    o="c:\\windows\\system32\\shutdown -s"#########
    os.system(o)#########
       
df = Get_Stock_List()
#print(df)
print(df.iloc[:,0].size)
#print(df)
df = Get_MACD(df)

#st = ts.get_st_classified()
#print(st)

Dist = 'D:\\ha\\haan\\'
Output_Csv(df,Dist)
