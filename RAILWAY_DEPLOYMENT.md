# 🚀 Railway 部署完整指南

## 📋 前置要求

- ✅ Railway 付費帳號（已有）
- ✅ GitHub 帳號（nicepolo1222@gmail.com）
- ✅ Telegram Bot Token（已有）

## 🎯 部署步驟

### 第一步：準備代碼

代碼已經準備好，包含：
- ✅ `app.py` - Flask 應用 + Telegram Bot
- ✅ `requirements.txt` - Python 依賴
- ✅ `Procfile` - Railway 配置
- ✅ `templates/index.html` - 前端頁面

### 第二步：上傳到 GitHub

#### 方式 A：使用 GitHub Web 界面（推薦新手）

1. 進入 GitHub：https://github.com/new
2. 建立新倉庫 `gold-arbitrage-calculator`
3. 選擇 Public（開放給其他人）
4. 點擊「Create repository」
5. 複製倉庫 URL

#### 方式 B：使用命令行

```bash
# 在您的本地機器上執行
cd /path/to/gold-forex-pro-advisor

# 初始化新倉庫
git init
git add .
git commit -m "Initial commit: Gold Arbitrage Calculator v2.0"

# 添加遠程倉庫
git remote add origin https://github.com/nicepolo/gold-arbitrage-calculator.git

# 推送代碼
git branch -M main
git push -u origin main
```

### 第三步：在 Railway 上部署

#### 1. 登入 Railway

進入 https://railway.app，使用 GitHub 帳號登入

#### 2. 建立新 Project

- 點擊「New Project」
- 選擇「Deploy from GitHub」
- 授權 Railway 訪問您的 GitHub
- 選擇倉庫：`nicepolo/gold-arbitrage-calculator`

#### 3. 配置環境變數

進入 Project Settings → Variables，添加：

| 變數名 | 值 |
|--------|-----|
| `TELEGRAM_TOKEN` | `8303439821:AAELkeuCKwGgFqlsgHz-s23LLGzSQCjvdzg` |
| `PORT` | `8080` |

#### 4. 自動部署

Railway 會自動：
- ✅ 偵測 `Procfile`
- ✅ 安裝 `requirements.txt` 中的依賴
- ✅ 啟動應用

部署完成後，您會獲得一個 URL，例如：
```
https://gold-arbitrage-calculator-production.up.railway.app
```

### 第四步：設定 Telegram Webhook

部署完成後，設定 Telegram Webhook 以接收 Bot 訊息。

#### 方式 A：使用 curl 命令

```bash
curl -X POST https://your-railway-url.up.railway.app/telegram/set-webhook \
  -H "Content-Type: application/json" \
  -d '{"webhook_url": "https://your-railway-url.up.railway.app/telegram/webhook"}'
```

#### 方式 B：在瀏覽器中訪問

1. 進入 Railway 應用 URL：`https://your-railway-url.up.railway.app`
2. 頁面會自動顯示網頁版計算器
3. 在瀏覽器開發者工具中執行：

```javascript
fetch('https://your-railway-url.up.railway.app/telegram/set-webhook', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({webhook_url: 'https://your-railway-url.up.railway.app/telegram/webhook'})
}).then(r => r.json()).then(console.log)
```

### 第五步：測試應用

#### 測試網頁版

進入 Railway 應用 URL，應該看到完整的計算器介面

#### 測試 Telegram Bot

1. 在 Telegram 中搜尋您的 Bot
2. 發送 `/start` 命令
3. 依序輸入參數
4. 接收計算報告

## 📊 應用架構

```
Railway App
├── Web UI (http://your-app.up.railway.app)
│   ├── 計算參數輸入
│   ├── 即時計算結果
│   ├── 歷史紀錄
│   └── 三語言支持
│
├── API 端點
│   ├── POST /api/calculate - 計算利潤
│   ├── GET /api/history - 獲取歷史
│   └── POST /api/clear-history - 清除歷史
│
├── Telegram Bot
│   ├── /start - 啟動 Bot
│   ├── 對話式引導輸入
│   └── 實戰報告發送
│
└── Webhook
    └── POST /telegram/webhook - 接收 Telegram 訊息
```

## 🔧 故障排除

### 問題 1：部署失敗

**症狀**：Railway 顯示「Build failed」

**解決方案**：
1. 檢查 `Procfile` 是否存在
2. 檢查 `requirements.txt` 中的依賴版本
3. 查看 Railway 的部署日誌（Logs 標籤）

### 問題 2：Bot 無法接收訊息

**症狀**：發送 `/start` 後沒有回應

**解決方案**：
1. 檢查 `TELEGRAM_TOKEN` 是否正確設定
2. 確認 Webhook 已設定
3. 檢查應用健康狀態：`GET /health`

### 問題 3：計算結果不正確

**症狀**：計算出現錯誤

**解決方案**：
1. 檢查輸入數值是否有效
2. 確認匯率單位（VND/TWD）
3. 確認越南賣價單位（萬 VND）

## 📞 支援資源

- **Railway 文檔**：https://docs.railway.app
- **Flask 文檔**：https://flask.palletsprojects.com
- **Telegram Bot API**：https://core.telegram.org/bots/api

## 🎉 部署完成

部署完成後，您將擁有：

✅ **網頁版計算器**
- 完整的黃金套利計算功能
- 三語言支持（中文、英文、越南文）
- 歷史紀錄和一鍵複製報告

✅ **Telegram Bot**
- 對話式引導輸入
- 完整的實戰報告
- 開放給其他用戶使用

✅ **持續運行**
- 24/7 在線
- 自動重啟
- 無需手動維護

---

**祝您部署順利！如有問題，請查看應用日誌或聯繫 Railway 支援。**
