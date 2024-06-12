import requests
import time
import pandas as pd
import os
import mplfinance as mpf
import matplotlib
import matplotlib.pyplot as plt


pd.set_option('expand_frame_repr', False)

COIN = input('輸入查詢幣種(建議小寫 例如:btc)：')

if not os.path.isdir( COIN + '_csv'):
    os.mkdir(COIN +'_csv')
BASE_URL = 'https://www.binance.com'
limit = 1000
end_time = int(time.time() // 60 * 60 * 1000)
print(end_time)
start_time =  int(end_time - limit*60*1000)
print(start_time)

file_dir = os.path.dirname(os.path.abspath(__file__))
csv_folder = COIN + '_csv'
flag = True

#設定獲取的時間範圍    
input_time = input('輸入時間範圍(範例:2023-06-15)：')
def get_timestamp_from_input(input_time):
    try:
       struct_time = time.strptime(input_time + ' 00:00:00', "%Y-%m-%d %H:%M:%S")  # 轉成時間元組
       time_stamp = int(time.mktime(struct_time))  # 轉成時間戳
       return time_stamp
    except ValueError:
       print("日期格式錯誤，請使用 YYYY-MM-DD 格式")
       print(time_stamp)
            
time_stamp = get_timestamp_from_input(input_time) 


while flag:

    url = BASE_URL + '/fapi/v1/continuousKlines?limit=' +str(limit) +'&pair=' + COIN + 'USDT&contractType=PERPETUAL&interval=1m' + '&startTime=' + str(start_time) + '&endTime=' + str(end_time)
  
    print(url)
    resp = requests.get(url)
    data = resp.json()
    df = pd.DataFrame(data, columns={'open_time': 0, 'open': 1, 'high': 2, 'low': 3, 'close': 4, 'volume': 5,
                                     'close_time': 6, 'quote_volume': 7, 'trades': 8, 'taker_base_volue': 9,
                                     'taker_quote_volume': 10, 'ignore': 11})

    df.set_index('open_time', inplace=True)
    #df.to_csv(str(end_time) + '.csv')
    file_path = os.path.join(file_dir, csv_folder, str(end_time) +  '.csv')
    df.to_csv(file_path)
    print(df)

    if len(df) < 1000:
            break
        
    end_time = start_time
    start_time = int(end_time - limit * 60 * 1000)
    print(start_time)
    
    if start_time < time_stamp * 1000: #載入資料之時間小於設定之時間時離開 While
       flag = False
    
pd.set_option('expand_frame_repr', False)

project_dir = os.getcwd() #path.dirname(os.path.dirname(__file__))
# print(project_dir)

csv_dir = project_dir + '/' + COIN + '_csv'
# print(csv_dir)

# for root, dirs, files in os.walk(csv_dir):
#     print('root:', root)  # 当前的目录
#     print('dirs:', dirs)  # 文件件加目录
#     print('files:', files)  # 文件
#     print("**"*20)
#
# print("****"*10)
# 批量读取文件名称
csv_file_paths = []

for root, dirs, files in os.walk(csv_dir):
    # 当files不为空的时候
    if files:
        for f in files:
            if f.endswith('.csv'):
                file_path = os.path.join(root, f)
                # print(file_path)
                csv_file_paths.append(file_path)


# 遍历文件名，批量导入数据
all_df = pd.DataFrame()

print(csv_file_paths)

for file in sorted(csv_file_paths):
    print(file)
    # 导入数据
    df = pd.read_csv(file)
    #  合并数据
    all_df = all_df.append(df, ignore_index=True)

# print(all_df)


# 删除重复的数据.
all_df.drop_duplicates(subset=['open_time'], inplace=True, keep='first')
# print(all_df)

#排序
all_df.sort_values(by=['open_time'], ascending=1, inplace=True)

all_df['open_time'] = pd.to_datetime(all_df['open_time'], unit='ms')

# 換時區 台灣時區 = +8 
all_df['open_time'] = all_df['open_time'] + pd.DateOffset(hours=8)

all_df = all_df[['open_time', 'open', 'high', 'low', 'close', 'volume']]

# df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
all_df.set_index('open_time', inplace=True)

#all_df.to_csv('binance_btc_1min.csv')
file_dir = os.path.dirname(os.path.abspath(__file__))
# 儲存路徑

if not os.path.isdir('alldata'):
    os.mkdir('alldata')
# 創建alldata資料夾

csv_folder = 'alldata'
file_path = os.path.join(file_dir, csv_folder,'binance_' + COIN + '_1min.csv')
all_df.to_csv(file_path)
print

pd.set_option('expand_frame_repr', False)

df = pd.read_csv('alldata/binance_' + COIN + '_1min.csv')
# print(df)
# print(df.dtypes)

df['open_time'] = pd.to_datetime(df['open_time'])

# print(df.dtypes)
# print(df)
# exit()

# df['open_time'] >= pd.to_datetime('2019-06-07 15:00:00')
df = df[df['open_time'] >= pd.to_datetime('2019-06-07 15:00:00')]  # 筛选时间周期的 df['open_time'] >= pd.to_datetime('2019-06-07 15:00:00')
# print(df)
#
# exit()

# 第一种方法，通过Series进行转换.
# 将时间周期相关的列设置为索引index
# df.set_index('open_time', inplace=True)
#
# # 周期转换方法：resample
# rule_cycle = '1D'  # rule_cycle='5T'：意思是5分钟，意味着转变为5分钟数据  # 15T  1H  1D 一天
#
# cycle_df = pd.DataFrame()
# cycle_df['close'] = df['close'].resample(rule=rule_cycle).last()  # last：取这5分钟的最后一行数据
# # # 开、高、低的价格，成交量
# cycle_df['open'] = df['open'].resample(rule=rule_cycle).first()  # 五分钟内的第一个值就是开盘价
# cycle_df['high'] = df['high'].resample(rule=rule_cycle).max()  # 五分钟内的最高价就是High
# cycle_df['low'] = df['low'].resample(rule=rule_cycle).min()  # 五分钟内的最低价就是low
# cycle_df['volume'] = df['volume'].resample(rule=rule_cycle).sum()  # 五分钟内的成交量的综合就是成交量
#
# print(cycle_df)
# exit()


# 通过DataFrame直接进行转换.

# rule_cycle = '5T'
# df.set_index('open_time', inplace=True)
# cycle_df1 = df.resample(rule=rule_cycle).agg(
#     {'open': 'first',
#      'high': 'max',
#      'low': 'min',
#      'close': 'last',
#      'volume': 'sum',
#      })
#
# print(cycle_df1)
# exit()

# 通过DataFrame直接进行转换.
rule_cycle = input('輸入時間週期：')
# df.reset_index(drop=False, inplace=True)  #
cycle_df1 = df.resample(rule=rule_cycle, on='open_time').agg(
    {'open': 'first',
     'high': 'max',
     'low': 'min',
     'close': 'last',
     'volume': 'sum',
     })




cycle_df1 = cycle_df1[['open', 'high', 'low', 'close', 'volume']]
#print(cycle_df1)


# 去除不必要的数据 去除一天都没有交易的周
cycle_df1.dropna(subset=['open'], inplace=True)
# 去除成交量为0的交易周期

cycle_df1 = cycle_df1[cycle_df1['volume'] > 0] # cycle_df1['volume'] > 0
print(cycle_df1)  #

file_dir = os.path.dirname(os.path.abspath(__file__))
# 儲存路徑
csv_folder = 'alldata'
file_path = os.path.join(file_dir, csv_folder,'binance_' + COIN + '_'+ rule_cycle +'.csv')
cycle_df1.to_csv(file_path)
"""
    B       business day frequency
    C       custom business day frequency (experimental)
    D       calendar day frequency
    W       weekly frequency
    M       month end frequency
    SM      semi-month end frequency (15th and end of month)
    BM      business month end frequency
    CBM     custom business month end frequency
    MS      month start frequency
    SMS     semi-month start frequency (1st and 15th)
    BMS     business month start frequency
    CBMS    custom business month start frequency
    Q       quarter end frequency
    BQ      business quarter endfrequency
    QS      quarter start frequency
    BQS     business quarter start frequency
    A       year end frequency
    BA      business year end frequency
    AS      year start frequency
    BAS     business year start frequency
    BH      business hour frequency
    H       hourly frequency
    T       minutely frequency
    S       secondly frequency
    L       milliseonds
    U       microseconds
    N       nanoseconds
"""

target_stock = COIN + 'Usdt_'
#rule_cycle = input('輸入時間週期：')

df = pd.read_csv(r'alldata/binance_' + COIN + '_'+rule_cycle+'.csv',parse_dates=True, index_col='open_time') #讀取目標股票csv檔的位置
df.rename(columns={'Turnover':'Volume'}, inplace = True) 
#這裡針對資料表做一下修正，因為交易量(Turnover)在mplfinance中須被改為Volume才能被認出來

mc = mpf.make_marketcolors(up='g',down='r',inherit=True)
s  = mpf.make_mpf_style(base_mpf_style='binance',marketcolors=mc)
#針對線圖的外觀微調，將上漲設定為紅色，下跌設定為綠色，符合台股表示習慣
#接著把自訂的marketcolors放到自訂的style中，而這個改動是基於預設的yahoo外觀

filename = target_stock + rule_cycle +'.png'

if not os.path.isdir('pictures'):
    os.mkdir('pictures')
# 創建pictures資料夾

file_dir = os.path.dirname(os.path.abspath(__file__))
csv_folder = 'pictures'
filename = os.path.join(file_dir, csv_folder,target_stock + rule_cycle +'.png')

kwargs = dict(type='candle', volume=True, figratio=(10,8), figscale=0.75, title=target_stock + rule_cycle, style=s) # mav=(5,20,60),均線 可加可不加 savefig =  filename
#設定可變參數kwargs，並在變數中填上繪圖時會用到的設定值

mpf.plot(df, **kwargs)
plt.savefig(filename,dpi=300)
#選擇df資料表為資料來源，帶入kwargs參數，畫出目標股票的走勢圖
