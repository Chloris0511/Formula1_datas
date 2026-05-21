# 這個檔案專門用來處理 2026 年 F1 上海大獎賽 的排位賽圈速與各扇區時間
# 並特別標記出 Antonelli 創造最年輕桿位  的歷史性數據。
import fastf1 as ff1
import pandas as pd

# 1. 啟用緩存
ff1.Cache.enable_cache('f1_cache')

print("--- 任務一：開始提取排位賽數據 ---")

# 2. 載入排位賽 Session
session_q = ff1.get_session(2026, 'China', 'Q')
session_q.load(telemetry=False)

# 3. 挑選有效快圈
quick_laps = session_q.laps.pick_quicklaps()

# 4. 聚合每位車手的最佳 S1, S2, S3 與最快單圈時間
best_sectors = quick_laps.groupby('Driver').agg({
    'Sector1Time': 'min',
    'Sector2Time': 'min',
    'Sector3Time': 'min',
    'LapTime': 'min'
}).reset_index()

# 5. 將 timedelta 轉換為秒數 (float)
for col in ['Sector1Time', 'Sector2Time', 'Sector3Time', 'LapTime']:
    best_sectors[col] = best_sectors[col].dt.total_seconds()

# 6. 計算各車手的扇區排名 (數值越小排名越靠前)
best_sectors['S1_Rank'] = best_sectors['Sector1Time'].rank(method='min')
best_sectors['S2_Rank'] = best_sectors['Sector2Time'].rank(method='min')
best_sectors['S3_Rank'] = best_sectors['Sector3Time'].rank(method='min')

# 7. 標記 Antonelli (ANT) 用於後續視覺化亮點分析
best_sectors['Is_Antonelli'] = best_sectors['Driver'].apply(lambda x: 'Yes' if x == 'ANT' else '')

# 8. 輸出 CSV
output_filename = 'quali_sectors.csv'
best_sectors.to_csv(output_filename, index=False)

print(f"排位賽數據處理完畢！已成功輸出至：{output_filename}")
