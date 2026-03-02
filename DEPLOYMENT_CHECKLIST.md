# ✅ Railway 部署檢查清單

## 📋 部署前準備

- [ ] 確認 Railway 帳號已登入
- [ ] 確認 GitHub 帳號已連接到 Railway
- [ ] 準備好 Telegram Bot Token：`8303439821:AAELkeuCKwGgFqlsgHz-s23LLGzSQCjvdzg`
- [ ] 準備好 Railway App URL（部署後獲得）

## 🚀 部署步驟

### 步驟 1：建立 GitHub 倉庫

- [ ] 進入 https://github.com/new
- [ ] 建立倉庫名稱：`gold-arbitrage-calculator`
- [ ] 選擇 Public（開放給其他人）
- [ ] 複製倉庫 URL

### 步驟 2：上傳代碼到 GitHub

**使用 Web 界面（簡單）**
- [ ] 進入新建倉庫
- [ ] 點擊「Add file」→「Upload files」
- [ ] 上傳以下文件：
  - [ ] `app.py`
  - [ ] `requirements.txt`
  - [ ] `Procfile`
  - [ ] `README.md`
  - [ ] `RAILWAY_DEPLOYMENT.md`
  - [ ] `templates/index.html`

**或使用命令行（進階）**
- [ ] 執行 git 推送命令
- [ ] 確認代碼已上傳到 GitHub

### 步驟 3：在 Railway 上建立 Project

- [ ] 進入 https://railway.app
- [ ] 點擊「New Project」
- [ ] 選擇「Deploy from GitHub」
- [ ] 授權 Railway 訪問 GitHub
- [ ] 選擇倉庫：`nicepolo/gold-arbitrage-calculator`
- [ ] 點擊「Deploy」

### 步驟 4：配置環境變數

- [ ] 進入 Project Settings → Variables
- [ ] 添加 `TELEGRAM_TOKEN`：`8303439821:AAELkeuCKwGgFqlsgHz-s23LLGzSQCjvdzg`
- [ ] 添加 `PORT`：`8080`
- [ ] 保存變數

### 步驟 5：等待部署完成

- [ ] 查看部署日誌
- [ ] 確認部署成功（Status: Success）
- [ ] 記下 Railway App URL

### 步驟 6：測試應用

**測試網頁版**
- [ ] 進入 Railway App URL
- [ ] 確認頁面正常加載
- [ ] 測試計算功能
- [ ] 測試語言切換

**測試 Telegram Bot**
- [ ] 設定 Webhook（見下方）
- [ ] 在 Telegram 中搜尋 Bot
- [ ] 發送 `/start` 命令
- [ ] 依序輸入參數
- [ ] 接收計算報告

### 步驟 7：設定 Telegram Webhook

在終端執行以下命令（將 URL 替換為您的 Railway App URL）：

```bash
curl -X POST https://YOUR_RAILWAY_URL/telegram/set-webhook \
  -H "Content-Type: application/json" \
  -d '{"webhook_url": "https://YOUR_RAILWAY_URL/telegram/webhook"}'
```

預期響應：
```json
{"ok": true, "result": true, "description": "Webhook was set"}
```

- [ ] Webhook 設定成功

## 🧪 功能測試

### 網頁版功能

- [ ] 輸入黃金重量（200g）
- [ ] 輸入台灣買價（1000 TWD/錢）
- [ ] 輸入越南賣價（1685 萬VND/錢）
- [ ] 輸入匯率（835 VND/TWD）
- [ ] 輸入各項開銷
- [ ] 點擊「計算利潤」
- [ ] 確認結果正確顯示
- [ ] 測試「複製報告」功能
- [ ] 測試「儲存結果」功能
- [ ] 檢查歷史紀錄

### 語言切換

- [ ] 切換到英文
- [ ] 切換到越南文
- [ ] 切換回中文

### Telegram Bot 功能

- [ ] 發送 `/start`
- [ ] 輸入黃金重量
- [ ] 輸入台灣買價
- [ ] 輸入越南賣價
- [ ] 輸入匯率
- [ ] 輸入各項開銷
- [ ] 接收完整報告

## 📊 性能檢查

- [ ] 訪問 `/health` 端點，確認應用健康
- [ ] 檢查 Railway 日誌，確認無錯誤
- [ ] 測試高併發（多個計算請求）
- [ ] 檢查記憶體使用情況

## 🔒 安全檢查

- [ ] 確認 `TELEGRAM_TOKEN` 已設定為環境變數（不在代碼中）
- [ ] 確認 `PORT` 動態設定（支援 Railway）
- [ ] 確認沒有硬編碼的敏感信息
- [ ] 檢查 CORS 設定

## 📈 優化檢查

- [ ] 前端頁面加載速度
- [ ] 計算響應時間
- [ ] 歷史紀錄查詢速度
- [ ] 移動設備顯示效果

## 🚀 上線前最終檢查

- [ ] 所有功能已測試
- [ ] 沒有 JavaScript 控制台錯誤
- [ ] Telegram Bot 正常運行
- [ ] 應用日誌無異常
- [ ] 性能指標正常

## ✅ 部署完成

- [ ] 應用已上線
- [ ] 網頁版可訪問
- [ ] Telegram Bot 可使用
- [ ] 所有功能正常運行

---

**部署完成日期**：________________

**Railway App URL**：https://________________________________

**Telegram Bot 用戶名**：@________________________________

**備註**：
