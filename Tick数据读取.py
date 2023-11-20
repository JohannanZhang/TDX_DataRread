# 股票的历史分笔数据读取
# 读取的属性：①股票每分钟内的每三秒钟的收盘价、成交量 ②buyorsell（价格变动方向，0为不变动，1为下跌，2为上涨） ③时间（time精确到分钟，date为日期
# 读取的时间范围：自股票上市以来每个交易日都可读取
# Read_Stock_Tick(stock_num: str, date: str) 为最基础的函数形式，读取特定股票特定交易日的行情，在此基础上空间可以拓展到全沪深市场、
# 时间上可拓展至全历史数据
# 读取的方式：直接调用相应函数
# 读取的结果：函数会返回特定股票上市以来至今所有交易日的分笔数据，dataframe格式。后可依据需求保存为相应csv、或压缩文件等


# 函数Mysql_Read_Stock_Tick所需要的模块
from mootdx.quotes import Quotes
client = Quotes.factory(market='std')

# 函数Mysql_Read_Stock_Alltick所需要的模块
from mootdx.reader import Reader
# 注意factory函数的参数tdxdir为通达信应用文件安装所在地址
reader = Reader.factory(market='std', tdxdir='C:/new_tdx')

# 两个函数都需要的模块
import pandas as pd


# 基础函数，获取特定股票、特定天数的分笔数据
def Read_Stock_Tick(stock_num: str, date: str):
    a = client.transactions(symbol=stock_num, date=date, start=0, offset=1800)
    i = 1
    t = client.transactions(symbol=stock_num, date=date, start=0, offset=1800)
    while t.empty == False:
        t = client.transactions(symbol=stock_num, date=date, start=1800 * i, offset=1800)
        a = pd.concat([t, a], ignore_index=True)
        i = i + 1

    a['date'] = date
    return a


# 获取特定股票自上市以来的所有交易日的分笔数据
def Read_Stock_Alltick(stock_num: str):
    # 导入读取日线的命令，为了得到股票上市以来所有的交易日
    day = reader.daily(symbol=stock_num)
    # 设定读取循环的初始状态
    i = 0
    F = Read_Stock_Tick(stock_num=stock_num, date=day.index[0].strftime('%Y%m%d'))
    # 设置循环
    while i < len(day.index)-1:
        i = i+1
        d = day.index[i].strftime('%Y%m%d')  #得出当天的字符串形式日期
        f = Read_Stock_Tick(stock_num=stock_num, date=d)
        F = pd.concat([F, f], ignore_index=False)

    return F


# 获取特定股票过去至今一共n个交易日的分笔数据
def Read_Stock_Special_tick(stock_num: str, datenum: int):
    # 导入读取日线的命令，为了得到股票上市以来所有的交易日
    day = reader.daily(symbol=stock_num)
    # 设定读取循环的初始状态
    i = 0
    F = Read_Stock_Tick(stock_num=stock_num, date=day.index[len(day)-1].strftime('%Y%m%d'))
    # 设置循环
    while i < datenum:
        i = i+1
        d = day.index[len(day)-i].strftime('%Y%m%d')  #得出当天的字符串形式日期
        f = Read_Stock_Tick(stock_num=stock_num, date=d)
        F = pd.concat([F, f], ignore_index=False)

    return F



