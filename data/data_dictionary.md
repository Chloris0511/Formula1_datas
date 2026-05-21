# 數據字典與影片段落對應關係報告 (data_dictionary.md)

本文件由 **傳科系 周欣怡 (學號: 114483904)** 整理，針對「2026年F1上海大獎賽數據分析」專案中所使用的所有數據文件（4個CSV文件、2個Excel活頁簿、2個Markdown規章報告）進行定義說明，並建立其與5分鐘精簡影片大綱的完整對應邏輯。

---

## 一、 數據一致性與質量檢查報告 (Data Integrity Report)

在正式導出此數據字典前，已使用 Python (Pandas) 腳本對本專案所屬的所有 CSV 文件進行了全面掃描，校驗結果如下：
1. **空值檢查 (Null Value Check)**：經校驗，`shanghai_history.csv`、`quali_sectors.csv`、`ham_lec_positions.csv` 及 `overtake_telemetry.csv` 中的**缺失值（NaN/Null）數量均為 0**，確保了數據流的完整性。
2. **命名規範一致性 (Naming Convention)**：所有欄位統一採用小寫蛇形命名法（`snake_case`），並在**所有涉及物理量與時間計量的欄位名稱末尾強制標註標準單位字尾**（如 `_seconds`、`_meters`、`_kmh`、`_kw`、`_percentage`），避免了在資料視覺化階段因單位混淆導致的圖表渲染錯誤。
3. **資料型態與精度**：時間相關欄位統一使用雙精度浮點數（`float64`），確保精確到千分之一秒（毫秒級 F1 標準）；計數與名次欄位採用標準整數型態（`int64`）。

---

## 二、 核心數據字典 (Data Dictionary)

### 1. 歷年觀眾趨勢表 (`shanghai_history.csv`)
* **數據來源**：Wikipedia 上海大獎賽歷史條目手動提取與清洗。
* **主要用途**：用於繪製 2004–2026 年上賽道人次變動折線圖，展現疫情停辦前後與2026新規元年的市場熱度對比。

| 欄位名稱 | 資料型態 | 計量單位 | 欄位含義 / 計算與提取方法 |
| :--- | :--- | :--- | :--- |
| `Year` | int64 | 年份 (Year) | 舉辦 F1 上海大獎賽的西元年份（範圍：2004 – 2026）。 |
| `Attendance` | int64 | 人次 (Person-times) | 三日現場累計觀賽總人次。若當年停辦則精確歸零（`0`）。 |
| `Status` | object | 文字狀態 | 賽事舉辦狀態：`Completed`（正常完賽）或 `Cancelled`（因疫情取消）。 |
| `Notes` | object | 文字備註 | 記錄當年賽事的里程碑事件（如：舒馬克最後一勝、第1000場大獎賽、周冠宇主場首秀等）。 |

### 2. 排位賽圈速與分段計時表 (`quali_sectors.csv`)
* **數據來源**：透過 FastF1 API 提取 2026 年上海站 Q3 階段遙測數據。
* **主要用途**：展現 Antonelli 奪得最年輕桿位時的絕對速度優勢。

| 欄位名稱 | 資料型態 | 計量單位 | 欄位含義 / 計算與提取方法 |
| :--- | :--- | :--- | :--- |
| `driver` | object | 字串 | 車手簡稱（例如：`K. Antonelli`、`M. Verstappen`）。 |
| `team` | object | 字串 | 車手所屬車隊名稱（例如：`Mercedes`、`Red Bull`）。 |
| `lap_time_seconds` | float64 | 秒 (Seconds) | Q3 階段最快單圈總耗時。計算方法：`sector_1 + sector_2 + sector_3`。 |
| `sector_1_seconds` | float64 | 秒 (Seconds) | 第一扇區（計時段1）精確耗時。 |
| `sector_2_seconds` | float64 | 秒 (Seconds) | 第二扇區（計時段2，大直道前複合彎）精確耗時。 |
| `sector_3_seconds` | float64 | 秒 (Seconds) | 第三扇區（計時段3，包含1.2公里大直道與終點線）精確耗時。 |
| `gap_seconds` | float64 | 秒 (Seconds) | 與桿位成績的時間差。桿位獲得者（Antonelli）預設為 `0.000`。 |

### 3. 車手正賽逐圈位置變動表 (`ham_lec_positions.csv`)
* **數據來源**：FastF1 API 正賽逐圈（Lap-by-lap）名次矩陣。
* **主要用途**：用於動態渲染 Hamilton 與 Leclerc 在正賽 56 圈中的名次交替動畫。

| 欄位名稱 | 資料型態 | 計量單位 | 欄位含義 / 計算與提取方法 |
| :--- | :--- | :--- | :--- |
| `lap_number` | int64 | 圈數 (Laps) | 正賽進行的圈次（範圍：1 – 56 圈）。 |
| `hamilton_position` | int64 | 名次 (Rank) | Lewis Hamilton 在該圈通過終點線時的即時賽道排名。 |
| `leclerc_position` | int64 | 名次 (Rank) | Charles Leclerc 在該圈通過終點線時的即時賽道排名。 |
| `interval_seconds` | float64 | 秒 (Seconds) | 兩台賽車在該圈通過計時線時的精確時間差隔。 |

### 4. 直道超車高頻遙測數據表 (`overtake_telemetry.csv`)
* **數據來源**：FastF1 API 結合 2026 賽車特定直道超車區間的 10Hz 高頻採集。
* **主要用途**：定量還原 2026 全新超車機制（手動超越模式）開啟後的物理表現。

| 欄位名稱 | 資料型態 | 計量單位 | 欄位含義 / 計算與提取方法 |
| :--- | :--- | :--- | :--- |
| `distance_meters` | int64 | 公尺 (Meters) | 以大直道起點為基準的相對行駛距離（0 – 500公尺）。 |
| `car_speed_kmh` | float64 | 公里/小時 (km/h) | 賽車在該位置點的即時時速。 |
| `throttle_percentage` | float64 | 百分比 (%) | 駕駛員油門踩踏深度（0.0% – 100.0% 全油門）。 |
| `brake_percentage` | float64 | 百分比 (%) | 駕駛員煞車踩踏深度（0.0% – 100.0%）。 |
| `manual_override_active`| bool | 布林值 (True/False) | 2026全新「手動超越模式（Manual Override）」是否被啟動。 |
| `mgu_k_output_kw` | float64 | 千瓦 (kW) | 動能回收電機（MGU-K）的即時電能功率輸出（最大 350 kW）。 |

---

## 三、 數據與影片段落對應關係矩陣 (Video Script Alignment Matrix)

為了讓數據分析結果與影片敘事完美嵌合，以下建立數據檔案與影片分鏡大綱（時長共約5分鐘）的強對應邏輯：

| 影片章節與名稱 | 時間軸區間 | 腳本敘事核心與畫面視覺 | 強綁定對應之數據文件 / 圖表素材 |
| :--- | :--- | :--- | :--- |
| **章節 01：開場引入** | **0:00 - 0:40** | **展現上賽的火熱氛圍與數字經濟**：介紹3天現場人次爆滿、門票秒殺以及對上海城市經濟、消費的巨大拉動效果。 | 1. `shanghai_econ.xlsx`（產出人次分佈與12.5億元經濟拉動圓餅圖）<br>2. `shanghai_history.csv`（產出23年歷史趨勢折線圖，突顯復甦高峰） |
| **章節 02：精彩瞬間** | **0:40 - 2:40** | **賽道英雄故事與超車懸念**：一個19歲的義大利少年 Antonelli 驚艷奪桿；隨後切入 Hamilton 與 Leclerc 的直道貼身肉搏超車瞬間，帶出新規。 | 1. `records.xlsx`（比對 Antonelli 與 Vettel 差 602 天的數據高亮圖）<br>2. `quali_sectors.csv`（展示三段計時優勢）<br>3. `ham_lec_positions.csv`（正賽名次動態交織線） |
| **章節 03：新規概要** | **2:40 - 3:40** | **硬核技術的直觀轉譯**：避開枯燥公式，用對比動畫解析2026車身縮小、主動雙翼（X/Z Mode）切換以及50:50功率分配與手動超越模式。 | 1. `regulations_notes.md`（提煉車身尺寸-200mm、重量-30kg的對比看板）<br>2. `overtake_telemetry.csv`（展示超越模式下 MGU-K 全力輸出維持至 337km/h 的折線圖） |
| **章節 04：新規挑戰** | **3:40 - 4:40** | **賽道的不可預測性與意外**：新規元年帶來的電氣整合與可靠性災難——以邁凱倫車隊在上海遭遇罕見的雙車 DNS（未起跑）故障為核心案例。 | 1. `mclaren_dnf.md`（展示 Norris 控制電子設備短路與 Piastri 高壓儲能故障的技術診斷字卡） |
| **章節 05：結語收束** | **4:40 - 5:00** | **情懷昇華與展望**：賽道內高潮迭起，圍場外新一代年輕車迷群體興起，潮流文化與數字經濟交融。期待春休後的鈴鹿站。 | *綜合引用上述所有數據趨勢*，畫面展現車迷廣場熱烈氛圍，完成主題收束。 |