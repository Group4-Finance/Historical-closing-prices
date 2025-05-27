# === 1 ：匯入套件 ===
import yfinance as yf
import pandas as pd
import time
import matplotlib.pyplot as plt
from datetime import datetime

# 設定英文字型，避免 matplotlib 找不到中文字體的警告
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# === 2 ：設定參數 ===
ticker = '00631L.TW'  # Yahoo Finance ETF 代碼
start_date = '2020-01-01'
end_date = pd.Timestamp.today().strftime('%Y-%m-%d')

# === 3 ：下載資料（保留原始 Close 與 Adj Close）===
time.sleep(5)  # 避免過於頻繁請求
df = yf.download(ticker, start=start_date, end=end_date, group_by='ticker', auto_adjust=False)

# 提取該股票對應的資料欄位（扁平化）
df_single = df.xs(ticker, level='Ticker', axis=1)

# 判斷是否包含 Adj Close 欄位
has_adj = 'Adj Close' in df_single.columns
plot_column = 'Adj Close' if has_adj else 'Close'

# 顯示前 5 筆資料
print("前五筆資料：")
print(df_single.head())

# === 4 ：儲存成 CSV（保留 Close、Adj Close（若有）、Volume）===
today_str = datetime.today().strftime('%Y%m%d')
csv_filename = f"{ticker.replace('.TW', '')}_price_data_{today_str}.csv"

# 動態選擇欄位
columns_to_save = ['Close', 'Volume']
if has_adj:
    columns_to_save.insert(1, 'Adj Close')  # 加在 Close 後面

df_single[columns_to_save].to_csv(csv_filename)
print(f"已儲存資料至：{csv_filename}")

# === 5 ：繪製趨勢圖（使用調整後價格或收盤價）===
plt.figure(figsize=(12, 6))
plt.plot(df_single.index, df_single[plot_column], label=plot_column)
plt.title(f"{ticker} {plot_column} Trend ({start_date} to {end_date})")
plt.xlabel("Date")
plt.ylabel(plot_column)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()