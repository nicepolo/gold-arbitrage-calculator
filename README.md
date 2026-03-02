# 🏆 黃金跨境套利計算器 (河內專業版)

**台越黃金貿易即時利潤計算器** - 集網頁版 App 和 Telegram Bot 於一身的專業套利工具

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 功能特性

### 🌐 網頁版 App

✨ **核心功能**
- 🧮 即時黃金套利利潤計算
- 📊 詳細的成本分析（5 項開銷拆分）
- 💼 保本線計算（Break-even Price）
- 📈 ROI 和利潤率統計
- 💾 計算歷史記錄（localStorage 持久化）
- 📋 一鍵複製報告

🎯 **優化功能**
- ✅ **通道費欄位** - 支援自訂通道費用
- ✅ **越南價格單位簡化** - 輸入「萬」自動轉換為實際 VND
- ✅ **5 項開銷拆分** - 機票、飯店、餐飲、交通、通道費
- ✅ **保本線計算** - 快速判斷虧損風險
- ✅ **ROI 投資報酬率** - 清晰的投資回報指標

🌍 **多語言支持**
- 🇹🇼 繁體中文
- 🇺🇸 English
- 🇻🇳 Tiếng Việt

📱 **UI/UX**
- 現代卡片式設計
- 超大淨利潤數字（綠/紅）
- 快速按鈕（200g/280g/300g）
- 手機優化、強光可見
- 自動全選輸入框

### 🤖 Telegram Bot

✅ **對話式引導**
- `/start` 命令啟動
- 依序引導輸入所有參數
- 實時驗證輸入

✅ **完整計算**
- 共享網頁版的計算邏輯
- 計算結果以格式化報告發送
- 支援所有開銷項目

✅ **實戰報告**
- 完整的財務分析
- 保本線和 ROI 計算
- 一鍵複製到剪貼板

## 📊 計算邏輯

### 基本公式

```
總錢數 = 重量 / 3.75
總成本 = (總錢數 × 台買價) + 機票 + 飯店 + 餐飲 + 交通 + 通道費
總營收 (TWD) = (總錢數 × 越賣價 × 10000) / 匯率
毛利 = 總營收 - (總錢數 × 台買價)
淨利潤 = 毛利 - 開銷總計
保本賣價 = ((總成本 × 匯率) / 總錢數) / 10000
ROI = (淨利潤 / 總成本) × 100%
```

### 開銷項目

- ✈️ 機票費用 (TWD)
- 🏨 飯店住宿 (TWD)
- 🍱 餐飲雜支 (TWD)
- 🚗 交通車費 (TWD)
- 🔐 通道費 (TWD)

## 🚀 快速開始

### 本地運行

#### 前置要求

- Python 3.8+
- pip

#### 安裝依賴

```bash
pip install -r requirements.txt
```

#### 運行應用

```bash
# 設定 Telegram Token（可選）
export TELEGRAM_TOKEN="your_telegram_bot_token"

# 啟動應用
python app.py
```

應用將在 `http://localhost:8080` 啟動

### 訪問應用

- **網頁版**: http://localhost:8080
- **Telegram Bot**: 使用 `/start` 命令啟動

## 🚢 Railway 部署

### 部署步驟

#### 1. 連接 GitHub 倉庫

- 登入 Railway (https://railway.app)
- 點擊「New Project」
- 選擇「Deploy from GitHub」
- 授權並選擇此倉庫

#### 2. 配置環境變數

進入 Project Settings → Variables，添加以下變數：

```
TELEGRAM_TOKEN=your_telegram_bot_token_here
```

#### 3. 自動部署

- Railway 會自動偵測 `Procfile`
- 自動安裝 `requirements.txt` 中的依賴
- 自動啟動應用

#### 4. 設定 Telegram Webhook

部署完成後，向應用發送 POST 請求設定 Webhook：

```bash
curl -X POST https://your-railway-app.up.railway.app/telegram/set-webhook \
  -H "Content-Type: application/json" \
  -d '{"webhook_url": "https://your-railway-app.up.railway.app/telegram/webhook"}'
```

### 部署檢查

健康檢查端點：`GET /health`

```bash
curl https://your-railway-app.up.railway.app/health
```

## 📡 API 文檔

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
  "success": true,
  "gold_weight": 200,
  "mace": 53.33,
  "revenue": 75000000,
  "purchase_cost": 53333.33,
  "total_expenses": 11500,
  "total_cost": 64833.33,
  "gross_profit": 74946666.67,
  "net_profit": 74935166.67,
  "break_even_price": 1234.56,
  "roi": 116234.56,
  "profit_margin": 99.98,
  "timestamp": "2026-03-02T00:00:00"
}
```

### 歷史記錄端點

**GET** `/api/history`

返回最後 20 筆計算記錄

**POST** `/api/clear-history`

清除所有計算記錄

### Telegram Webhook

**POST** `/telegram/webhook`

Telegram 服務器發送的 webhook 端點

**POST** `/telegram/set-webhook`

設定 Telegram Webhook URL

## 🤖 Telegram Bot 使用指南

### 啟動 Bot

在 Telegram 中發送 `/start` 命令

### 對話流程

```
1. 輸入黃金重量（克）
2. 輸入台灣買價（TWD/錢）
3. 輸入越南賣價（萬VND/錢）
4. 輸入匯率（VND/TWD）
5. 輸入機票費用（TWD）
6. 輸入飯店費用（TWD）
7. 輸入餐飲雜支（TWD）
8. 輸入交通車費（TWD）
9. 輸入通道費（TWD）
```

### 接收報告

計算完成後，Bot 會自動發送格式化的實戰報告，包含：
- 基本信息（重量、價格、匯率）
- 財務分析（營收、成本、利潤）
- 實戰指標（保本線、ROI、利潤率）

## 🛠️ 技術棧

- **後端**: Flask 3.0
- **前端**: HTML5 + CSS3 + Vanilla JavaScript
- **Bot**: python-telegram-bot 20.3
- **部署**: Railway
- **版本控制**: Git + GitHub

## 📁 文件結構

```
gold-forex-pro-advisor/
├── app.py                 # Flask 應用主程式（後端 + Bot）
├── requirements.txt       # Python 依賴
├── Procfile              # Railway 部署配置
├── .gitignore            # Git 忽略檔案
├── README.md             # 本檔案
└── templates/
    └── index.html        # 前端頁面（網頁版 App）
```

## 🔐 環境變數

| 變數名 | 說明 | 必需 | 預設值 |
|--------|------|------|--------|
| `PORT` | 應用監聽的端口 | 否 | 8080 |
| `TELEGRAM_TOKEN` | Telegram Bot Token | 否 | - |

## 📝 更新日誌

### v2.0.0 (2026-03-02)

**新增功能**
- ✅ 完整的網頁版 App
- ✅ Telegram Bot 整合
- ✅ 三語言支持（中文、英文、越南文）
- ✅ 通道費欄位
- ✅ 保本線計算
- ✅ ROI 投資報酬率
- ✅ 歷史紀錄持久化
- ✅ 一鍵複製報告
- ✅ Railway 部署支援

**改進**
- 優化計算邏輯
- 改進用戶介面
- 增強錯誤處理
- 支援多語言

## 🐛 故障排除

### Bot 無法連接

1. 檢查 `TELEGRAM_TOKEN` 是否正確設定
2. 確認 Webhook URL 已設定
3. 檢查應用健康狀態：`GET /health`

### 計算結果不正確

1. 檢查輸入數值是否有效
2. 確認匯率單位（VND/TWD）
3. 確認越南賣價單位（萬 VND）

### Railway 部署失敗

1. 檢查 `Procfile` 是否存在
2. 確認 `requirements.txt` 中的依賴版本
3. 查看 Railway 的部署日誌

## 📞 聯繫方式

如有問題或建議，請提交 Issue 或 Pull Request。

## 📄 許可證

MIT License

---

**Made with ❤️ for Gold Arbitrage Traders**

**黃金跨境套利計算器 (河內專業版) - 您的專業套利助手**
