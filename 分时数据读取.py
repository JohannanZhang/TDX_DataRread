# 股票的历史分时数据读取
# 读取的属性：每个交易日的每一分钟量价数据，具体为：分时收盘价与分时成交量、对应日期
# 读取的时间范围：自股票上市以来每个交易日都可读取，一个交易日240条数据
# 读取的方式：调用最下方函数：Mysql_Read_Stock_Alltimeshare(stock_num = '') stock_num为股票代码，字符串形式。
# 读取的结果：函数会返回特定股票上市以来至今所有交易日的分时数据，dataframe格式。可通过最末尾注释的命令，将数据导入MySQL的特定数据库特定表。
from mootdx.quotes import Quotes
from mootdx.reader import Reader
client = Quotes.factory(market='std')

# 先定义函数，获取特定股票、特定天数的分时数据（date的数据结构就是年月日的字符串，如'20230426'）
def Mysql_Read_Stock_Timeshare(stock_num: str, date: str):
    a = client.minutes(symbol=stock_num, date=date)
    a['date'] = date
    return a


# 获取特定股票自上市以来的所有交易日的分时数据
def Mysql_Read_Stock_Alltimeshare(stock_num: str):
    import pandas as pd
    # 导入读取日线的命令，为了得到股票上市以来所有的交易日
    reader = Reader.factory(market='std', tdxdir='E:/tdx')
    day = reader.daily(symbol=stock_num)
    # 设定读取循环的初始状态
    i = 0
    F = Mysql_Read_Stock_Timeshare(stock_num=stock_num, date=day.index[0].strftime('%Y%m%d'))
    # 设置循环
    while i < len(day.index)-1:
        i = i+1
        b = day.index[i].strftime('%Y%m%d')  #得出当天的字符串形式日期
        f = Mysql_Read_Stock_Timeshare(stock_num=stock_num, date=b)
        F = pd.concat([F, f], ignore_index=False)

    # file1 = open(f'D:/历史分时数据的压缩文件汇总/ts_stock/{stock_num}.csv', "a", newline='')
    # F.to_csv(file1)



