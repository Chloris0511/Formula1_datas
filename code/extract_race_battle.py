# 這個檔案專門用來處理正賽中 Hamilton 與 Leclerc 的位置與差距計算
# 透過分析名次變動，精準抓出影片中需要呈現的超車和換位圈次
import fastf1 as ff1
import pandas as pd

# 1. 啟用緩存
ff1.Cache.enable_cache('f1_cache')

print("--- 任務二：開始提取正賽 HAM vs LEC 纏鬥數據 ---")

# 2. 載入正賽 Session
session_r = ff1.get_session(2026, 'China', 'R')
session_r.load(telemetry=False)

# 3. 提取 HAM 與 LEC 的圈數據
ham_laps = session_r.laps.pick_driver('HAM')
lec_laps = session_r.laps.pick_driver('LEC')

# 4. 篩選關鍵欄位 (圈數、名次、當圈結束時的比賽總時間)
ham_df = ham_laps[['LapNumber', 'Position', 'Time']].copy()
lec_df = lec_laps[['LapNumber', 'Position', 'Time']].copy()

# 5. 合併兩位車手的數據
battle_df = pd.merge(ham_df, lec_df, on='LapNumber', suffixes=('_HAM', '_LEC'))

# 6. 計算兩人之間的實時時間差距 (秒)
battle_df['Gap_Seconds'] = (battle_df['Time_HAM'] - battle_df['Time_LEC']).dt.total_seconds()

# 7. 使用 diff() 計算每圈的名次變化
battle_df['HAM_Pos_Diff'] = battle_df['Position_HAM'].diff()
battle_df['LEC_Pos_Diff'] = battle_df['Position_LEC'].diff()

# 8. 邏輯判斷：當兩人的相對前後順序發生改變時，標記為超車圈 (True)
battle_df['Overtake_Occurred'] = (
    (battle_df['Position_HAM'] < battle_df['Position_LEC']) != 
    (battle_df['Position_HAM'].shift(1) < battle_df['Position_LEC'].shift(1))
)
# 排除第一圈的初始相對位置被誤判為超車
battle_df.loc[0, 'Overtake_Occurred'] = False

# 9. 輸出 CSV
output_filename = 'ham_lec_positions.csv'
battle_df.to_csv(output_filename, index=False)

print(f"正賽纏鬥數據處理完畢！已成功輸出至：{output_filename}")