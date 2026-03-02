# 黃金跨境 套利計算器

台越黃金貿易即時利潤計算器 - 專業套利工具

## 功能特性

✨ **核心功能**
- 🧮 即時黃金套利利潤計算
- 📊 詳細的成本分析
- 💼 介紹費 10% 自動計算
- 📈 利潤率統計
- 💾 計算歷史記錄
- 📋 一鍵複製報告

🎯 **優化功能**
- ✅ **通道費欄位** - 支援自訂通道費用
- ✅ **介紹費計算** - 自動計算淨利的 10% 介紹費，並顯示最終淨利

📍 **支援位置**
- 台北 (TPE)
- 台中 (RMQ)
- 高雄 (KHH)

## 計算邏輯

### 基本公式

```
營收 = 越南賣價 × 黃金重量(錢) × 匯率
購買成本 = 台灣買價 × 黃金重量(錢)
毛利 = 營收 - 購買成本
淨利 = 毛利 - 開銷總計
介紹費 = 淨利 × 10%
最終淨利 = 淨利 - 介紹費
```

### 開銷項目

- ✈️ 機票
- 🏨 飯店
- 🍽️ 餐飲雜支
- 🚗 交通車費
- 🔐 通道費 (新增)

## 本地運行

### 前置要求

- Python 3.8+
- pip

### 安裝依賴

```bash
pip install -r requirements.txt
```

### 運行應用

```bash
python app.py
```

應用將在 `http://localhost:8080` 啟動

## Railway 部署

### 部署步驟

1. **連接 GitHub 倉庫**
   - 登入 Railway (https://railway.app)
   - 點擊「New Project」
   - 選擇「Deploy from GitHub」
   - 授權並選擇此倉庫

2. **配置環境變數**
   - 進入 Project Settings → Variables
   - 無需額外配置（應用已支援 Railway 的 PORT 環境變數）

3. **自動部署**
   - Railway 會自動偵測 `Procfile`
   - 自動安裝 `requirements.txt` 中的依賴
   - 自動啟動應用

### 部署檢查

部署完成後，應用會在 Railway 提供的域名上運行。

健康檢查端點：`GET /health`

## API 文檔

### 計算端點

**POST** `/api/calculate`

請求體：
```json
{
  "gold_weight": 200,
  "buy_price": 1000,
  "sell_price": 1685,
  "exchange_rate": 835,
  "ticket_cost": 5000,
  "hotel_cost": 3000,
  "meal_cost": 2000,
  "transport_cost": 1000,
  "channel_cost": 500
}
```

響應：
```json
{
  "gold_weight": 200,
  "mace": 53.33,
  "revenue": 75000000,
  "purchase_cost": 53333.33,
  "total_expenses": 11500,
  "total_cost": 64833.33,
  "gross_profit": 74946666.67,
  "net_profit": 74935166.67,
  "introduction_fee": 7493516.67,
  "final_net_profit": 67441650,
  "profit_margin": 89.98,
  "timestamp": "2026-03-02T00:00:00"
}
```

### 歷史記錄端點

**GET** `/api/history`

返回最後 20 筆計算記錄

**POST** `/api/clear-history`

清除所有計算記錄

### 健康檢查

**GET** `/health`

返回應用健康狀態

## 技術棧

- **後端**: Flask 3.0
- **前端**: HTML5 + CSS3 + Vanilla JavaScript
- **部署**: Railway
- **版本控制**: Git + GitHub

## 環境變數

- `PORT` - 應用監聽的端口（預設 8080，Railway 會自動設定）

## 文件結構

```
gold-forex-pro-advisor/
├── app.py                 # Flask 應用主程式
├── requirements.txt       # Python 依賴
├── Procfile              # Railway 部署配置
├── .gitignore            # Git 忽略檔案
├── README.md             # 本檔案
└── templates/
    └── index.html        # 前端頁面
```

## 更新日誌

### v1.1.0 (2026-03-02)

**新增功能**
- ✅ 通道費欄位
- ✅ 介紹費 10% 自動計算版塊
- ✅ 最終淨利顯示
- ✅ Railway 部署支援

**改進**
- 優化計算邏輯
- 改進用戶介面
- 增強錯誤處理

## 許可證

MIT License

## 聯繫方式

如有問題或建議，請提交 Issue 或 Pull Request。

---

**Made with ❤️ for Gold Arbitrage Traders**