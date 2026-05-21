import fastf1 as ff1
import pandas as pd
import sys

# 1. 啟用緩存
ff1.Cache.enable_cache('f1_cache')

print("--- 任務三：開始提取超車瞬間高頻遙測數據 ---")

# ==========================================
# 步驟一：從先前生成的 CSV 中確認換位（超車）圈次
# ==========================================
try:
    positions_df = pd.read_csv('ham_lec_positions.csv')
except FileNotFoundError:
    print("錯誤：找不到 ham_lec_positions.csv")
    sys.exit()

# 找出所有發生超車（相對位置反轉）的圈次
overtake_laps = positions_df[positions_df['Overtake_Occurred'] == True]['LapNumber'].tolist()

if not overtake_laps:
    print("提示：在數據中未偵測到明確的相對位置反轉圈次。")
    # 如果沒抓到，預設指定一個可能發生纏鬥的圈次進行分析（例如第 15 圈，可自由修改）
    target_lap = 15 
    print(f"將默認提取第 {target_lap} 圈的數據進行分析。")
else:
    # 選擇第一個發生超車的圈次作為影片主敘事點
    target_lap = overtake_laps[0]
    print(f"成功確認超車圈次！將提取第 {target_lap} 圈的高頻遙測數據。")

# ==========================================
# 步驟二：載入正賽並提取該圈的 Telemetry 數據
# ==========================================
session_r = ff1.get_session(2026, 'China', 'R')
# 注意：這次必須將 telemetry 設為 True，以載入油門、煞車、速度等核心數據
session_r.load(telemetry=True)

# 獲取兩位車手在該圈的單圈對象
lap_ham = session_r.laps.pick_driver('HAM').pick_lap(target_lap)
lap_lec = session_r.laps.pick_driver('LEC').pick_lap(target_lap)

# 提取遙測數據並自動計算 Distance (距離字段)
# 註：get_telemetry() 比 get_car_data() 更全面，能一次整合速度、油門、煞車與 DRS 狀態
tel_ham = lap_ham.get_telemetry().add_distance()
tel_lec = lap_lec.get_telemetry().add_distance()

# 篩選出你需要的核心欄位
keep_cols = ['Distance', 'Speed', 'Throttle', 'Brake', 'DRS']
tel_ham = tel_ham[keep_cols].copy()
tel_lec = tel_lec[keep_cols].copy()

# ==========================================
# 步驟三：以 Distance 字段對齊兩車數據
# ==========================================
# 確保數據依距離排序
tel_ham = tel_ham.sort_values('Distance')
tel_lec = tel_lec.sort_values('Distance')

# 使用 pandas 完美的 merge_asof 功能，以 HAM 的距離點為基準，
# 自動媒合 LEC 離該距離最近的遙測數據，達到完美的「空間對齊」
aligned_telemetry = pd.merge_asof(
    tel_ham, 
    tel_lec, 
    on='Distance', 
    suffixes=('_HAM', '_LEC'), 
    direction='nearest'
)

# ==========================================
# 步驟四：輸出 CSV 檔案
# ==========================================
output_filename = 'overtake_telemetry.csv'
aligned_telemetry.to_csv(output_filename, index=False)

print(f"超車遙測數據處理完畢！已成功輸出至：{output_filename}")