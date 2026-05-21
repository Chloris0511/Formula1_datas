import fastf1 as ff1
import os

# ==========================================
# 第二步：建立並啟用緩存 (Cache)
# ==========================================
cache_dir = 'f1_cache' # 設定緩存資料夾名稱

# 檢查資料夾是否存在，若無則自動建立
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
    print(f"已建立緩存資料夾: {cache_dir}")

# 啟用 FastF1 緩存功能，將路徑指向剛剛建立的資料夾
ff1.Cache.enable_cache(cache_dir)

# ==========================================
# 第三步：掛機下載上海站 Qualifying + Race
# ==========================================
print("開始連接 API，準備下載 2026 上海大獎賽數據 (這可能需要幾分鐘，請稍候)...")

# 獲取並載入排位賽 (Qualifying) 數據
# 參數說明：年份, 國家/賽事名稱, 賽程縮寫 ('Q' 代表排位賽)
session_q = ff1.get_session(2026, 'China', 'Q')
session_q.load() 
print("排位賽 (Qualifying) 數據下載並緩存完成！")

# 獲取並載入正賽 (Race) 數據
# 參數說明：'R' 代表正賽
session_r = ff1.get_session(2026, 'China', 'R')
session_r.load()
print("正賽 (Race) 數據下載並緩存完成！")

# ==========================================
# 第四步：驗證 session 可正常讀取
# ==========================================
print("\n--- 數據讀取驗證 ---")
try:
    # 驗證排位賽基本資訊
    print(f"賽事名稱: {session_q.event['EventName']} - {session_q.name}")
    
    # 簡單印出排位賽成績前三名的車手簡寫與名次
    print("\n排位賽前三名車手:")
    print(session_q.results[['DriverNumber', 'Abbreviation', 'Position']].head(3))
    
    print("\n驗證成功！數據已完美存入本地，後續調用將會非常快速。")
except Exception as e:
    print(f"驗證過程中發生錯誤: {e}")