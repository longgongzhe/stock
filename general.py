import tushare as ts
symbols = ts.get_stock_basics()
st = ts.get_st_classified()
lv_price_1 = 50
def isSt(stockID):
    for sti in st.code:
        if sti == stockID:
            return True
    return False
for inx in range(len(symbols)):
    symbol = symbols.index[inx]
    df = ts.get_k_data(symbol, ktype='60', start=start_day)
# 1，过滤停牌            
xn = len(df.index)-1
if type(df) != type(None) and xn >= 0 and df.ix[xn]['date'] != endToday:
    continue
#2，过滤高价股            
if type(df) != type(None) and xn >= 0 and df.ix[xn]['close'] > lv_price_1 ):
    continue
# 3，过滤PE        
pe = symbols.ix[inx]['pe']
if pe < 20:
    continue
#4，过滤ST        
if isSt(symbol):
    continue
