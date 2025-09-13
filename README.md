# smart_traffic_ai – Mode A (Rule-based)

一鍵跑得起的示範專案，涵蓋：安全護欄、仲裁器、四大策略插件、SUMO Runner、Web 儀表板（Flask + SocketIO）、A/B 切換與三段劇情、資料輸出。

## 專案結構
```
core/                # 控制器基底、護欄、仲裁器、SUMO 介面
algorithms/          # 綠波、行人、公車、緊急車策略
experiments/         # Demo 與訓練腳本
web/                 # Flask 儀表板
scripts/             # 產生示範網路與路線
data/                # 配置與輸出
models/              # 模型檔（預留）
logs/                # 日誌（預留）
```

## 安裝與執行
1. **確認 SUMO 可用**
   ```bash
   make sumo_check
   ```
2. **安裝依賴**
   ```bash
   make setup
   ```
3. **產生 demo 網路 / 路線 / sumocfg**
   ```bash
   make net
   ```
4. **啟動 Demo（先跑引擎 + 寫檔）**
   ```bash
   make demo
   ```
5. **另開終端：啟動 Web 儀表板**
   ```bash
   make web
   # 瀏覽 http://127.0.0.1:5000
   ```

## 目錄說明
* `data/config/system_config.yaml`：系統與 SUMO 參數。
* `scripts/make_demo_routes.py`：產生示範網路與路線。
* `experiments/run_demo.py`：執行 SUMO + 決策迴圈。
* `web/app.py`：讀檔推播到前端儀表板。

更多進階功能可參考 `TODO`：
* 實作 detectors、真實行車資料。
* REST API 供前端切換劇情與模式。
* 使用 RLPolicyAdapter 連結強化學習模型。
