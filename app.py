import os
import json
from datetime import datetime, timezone, timedelta
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
from functools import wraps

app = Flask(__name__)
CORS(app)

# 設定 Port，支援 Railway 環境變數
PORT = int(os.environ.get("PORT", 8080))
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# 模擬數據存儲（實際應用應使用數據庫）
calculations_history = []
user_states = {}  # 存儲用戶的對話狀態


# ==================== 計算邏輯（共享） ====================

class GoldCalculator:
    """黃金套利計算器核心邏輯"""
    
    # 單位換算常數
    MACE_TO_GRAM = 3.75  # 1錢 = 3.75克
    VND_UNIT = 10000  # 越南賣價單位（萬）
    
    @staticmethod
    def calculate(gold_weight, buy_price, sell_price, exchange_rate,
                  ticket_cost=0, hotel_cost=0, meal_cost=0, transport_cost=0, channel_cost=0):
        """
        計算黃金套利利潤
        
        參數：
        - gold_weight: 黃金重量（克）
        - buy_price: 台灣買價（TWD/錢）
        - sell_price: 越南賣價（萬 VND/錢）
        - exchange_rate: 匯率（VND/TWD）
        - ticket_cost: 機票費用（TWD）
        - hotel_cost: 飯店費用（TWD）
        - meal_cost: 餐飲雜支（TWD）
        - transport_cost: 交通車費（TWD）
        - channel_cost: 通道費（TWD）
        
        返回：計算結果字典
        """
        try:
            # 轉換為浮點數
            gold_weight = float(gold_weight)
            buy_price = float(buy_price)
            sell_price = float(sell_price)
            exchange_rate = float(exchange_rate)
            ticket_cost = float(ticket_cost) if ticket_cost else 0
            hotel_cost = float(hotel_cost) if hotel_cost else 0
            meal_cost = float(meal_cost) if meal_cost else 0
            transport_cost = float(transport_cost) if transport_cost else 0
            channel_cost = float(channel_cost) if channel_cost else 0
            
            # 驗證輸入
            if gold_weight <= 0 or buy_price <= 0 or sell_price <= 0 or exchange_rate <= 0:
                raise ValueError("重量、買價、賣價和匯率必須大於 0")
            
            # 單位換算
            mace = gold_weight / GoldCalculator.MACE_TO_GRAM
            
            # 計算營收：(越南賣價 × 錢數 × 10000) / 匯率
            revenue = (sell_price * mace * GoldCalculator.VND_UNIT) / exchange_rate
            
            # 計算成本
            purchase_cost = buy_price * mace
            total_expenses = ticket_cost + hotel_cost + meal_cost + transport_cost + channel_cost
            total_cost = purchase_cost + total_expenses
            
            # 計算利潤
            gross_profit = revenue - purchase_cost
            net_profit = gross_profit - total_expenses
            
            # 保本線計算：((總成本 × 匯率) / 總錢數) / 10000
            break_even_price = ((total_cost * exchange_rate) / mace) / GoldCalculator.VND_UNIT if mace > 0 else 0
            
            # ROI (投資報酬率)
            roi = (net_profit / total_cost * 100) if total_cost > 0 else 0
            
            # 利潤率
            profit_margin = (net_profit / revenue * 100) if revenue > 0 else 0
            
            # 介紹費計算（淨利的 10%）
            referral_fee = net_profit * 0.1
            
            # 實際淨利（扣除介紹費後）
            actual_net_profit = net_profit - referral_fee
            
            return {
                'success': True,
                'gold_weight': gold_weight,
                'mace': round(mace, 2),
                'buy_price': buy_price,
                'sell_price': sell_price,
                'exchange_rate': exchange_rate,
                'revenue': round(revenue, 2),
                'purchase_cost': round(purchase_cost, 2),
                'ticket_cost': ticket_cost,
                'hotel_cost': hotel_cost,
                'meal_cost': meal_cost,
                'transport_cost': transport_cost,
                'channel_cost': channel_cost,
                'total_expenses': round(total_expenses, 2),
                'total_cost': round(total_cost, 2),
                'gross_profit': round(gross_profit, 2),
                'net_profit': round(net_profit, 2),
                'break_even_price': round(break_even_price, 2),
                'roi': round(roi, 2),
                'profit_margin': round(profit_margin, 2),
                'referral_fee': round(referral_fee, 2),
                'actual_net_profit': round(actual_net_profit, 2),
                'timestamp': datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# ==================== Flask 路由 ====================

@app.route('/')
def index():
    """主頁面"""
    return render_template('index.html')


@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    """計算 API 端點"""
    try:
        data = request.json
        
        result = GoldCalculator.calculate(
            gold_weight=data.get('gold_weight', 0),
            buy_price=data.get('buy_price', 0),
            sell_price=data.get('sell_price', 0),
            exchange_rate=data.get('exchange_rate', 0),
            ticket_cost=data.get('ticket_cost', 0),
            hotel_cost=data.get('hotel_cost', 0),
            meal_cost=data.get('meal_cost', 0),
            transport_cost=data.get('transport_cost', 0),
            channel_cost=data.get('channel_cost', 0)
        )
        
        if result['success']:
            calculations_history.append(result)
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/history', methods=['GET'])
def api_history():
    """獲取計算歷史"""
    return jsonify(calculations_history[-20:]), 200


@app.route('/api/clear-history', methods=['POST'])
def api_clear_history():
    """清除計算歷史"""
    global calculations_history
    calculations_history = []
    return jsonify({'message': '歷史記錄已清除'}), 200


@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查端點（用於 Railway）"""
    return jsonify({'status': 'healthy'}), 200


# ==================== Telegram Bot 邏輯 ====================

def send_telegram_message(chat_id, text, parse_mode='HTML'):
    """發送 Telegram 訊息"""
    try:
        url = f"{TELEGRAM_API_URL}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode
        }
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"發送 Telegram 訊息失敗: {e}")
        return None


def send_telegram_report(chat_id, result):
    """發送計算報告到 Telegram"""
    if not result['success']:
        send_telegram_message(chat_id, f"❌ 計算失敗: {result['error']}")
        return
    
    report = f"""
<b>📊 黃金跨境套利計算報告</b>
━━━━━━━━━━━━━━━━━━━━━━━━

<b>📈 基本信息</b>
• 黃金重量: {result['gold_weight']}克 ({result['mace']}錢)
• 台灣買價: {result['buy_price']:,.0f} TWD/錢
• 越南賣價: {result['sell_price']:,.0f} 萬VND/錢
• 匯率: {result['exchange_rate']:,.0f} VND/TWD

<b>💰 財務分析</b>
• 總營收: {result['revenue']:,.0f} TWD
• 購買成本: {result['purchase_cost']:,.0f} TWD
• 開銷總計: {result['total_expenses']:,.0f} TWD
  ✈️ 機票: {result['ticket_cost']:,.0f} TWD
  🏨 飯店: {result['hotel_cost']:,.0f} TWD
  🍱 餐飲: {result['meal_cost']:,.0f} TWD
  🚗 交通: {result['transport_cost']:,.0f} TWD
  🔐 通道費: {result['channel_cost']:,.0f} TWD

<b>📊 利潤計算</b>
• 毛利: {result['gross_profit']:,.0f} TWD
• 淨利潤: <b>{result['net_profit']:,.0f} TWD</b>
• 介紹費 (10%): {result['referral_fee']:,.0f} TWD
• 實際淨利: <b>{result['actual_net_profit']:,.0f} TWD</b>
• 保本賣價: {result['break_even_price']:,.2f} 萬VND/錢
• ROI (投資報酬率): <b>{result['roi']:.2f}%</b>
• 利潤率: {result['profit_margin']:.2f}%

<b>⏰ 計算時間（北京時間）</b>
{result['timestamp']}
━━━━━━━━━━━━━━━━━━━━━━━━
    """.strip()
    
    send_telegram_message(chat_id, report)


@app.route('/telegram/webhook', methods=['POST'])
def telegram_webhook():
    """Telegram Webhook 端點"""
    try:
        data = request.json
        
        if 'message' not in data:
            return jsonify({'ok': True}), 200
        
        message = data['message']
        chat_id = message['chat']['id']
        user_id = message['from']['id']
        text = message.get('text', '').strip()
        
        # 初始化用戶狀態
        if user_id not in user_states:
            user_states[user_id] = {
                'step': 0,
                'data': {}
            }
        
        state = user_states[user_id]
        
        # /start 命令
        if text == '/start':
            state['step'] = 0
            state['data'] = {}
            send_telegram_message(chat_id, 
                "👋 歡迎使用黃金跨境套利計算器！\n\n"
                "請依序輸入以下信息：\n"
                "1️⃣ 黃金重量（克）\n"
                "2️⃣ 台灣買價（TWD/錢）\n"
                "3️⃣ 越南賣價（萬VND/錢）\n"
                "4️⃣ 匯率（VND/TWD）\n"
                "5️⃣ 機票費用（TWD）\n"
                "6️⃣ 飯店費用（TWD）\n"
                "7️⃣ 餐飲雜支（TWD）\n"
                "8️⃣ 交通車費（TWD）\n"
                "9️⃣ 通道費（TWD）\n\n"
                "請先輸入黃金重量（克）："
            )
            state['step'] = 1
            return jsonify({'ok': True}), 200
        
        # 處理各步驟輸入
        try:
            value = float(text)
        except ValueError:
            send_telegram_message(chat_id, "❌ 請輸入有效的數字")
            return jsonify({'ok': True}), 200
        
        steps = [
            ('gold_weight', '黃金重量'),
            ('buy_price', '台灣買價'),
            ('sell_price', '越南賣價'),
            ('exchange_rate', '匯率'),
            ('ticket_cost', '機票費用'),
            ('hotel_cost', '飯店費用'),
            ('meal_cost', '餐飲雜支'),
            ('transport_cost', '交通車費'),
            ('channel_cost', '通道費')
        ]
        
        if 1 <= state['step'] <= len(steps):
            key, label = steps[state['step'] - 1]
            state['data'][key] = value
            
            if state['step'] < len(steps):
                next_key, next_label = steps[state['step']]
                send_telegram_message(chat_id, f"✅ {label}已記錄: {value}\n\n請輸入{next_label}：")
                state['step'] += 1
            else:
                # 所有輸入完成，進行計算
                send_telegram_message(chat_id, "⏳ 正在計算中...")
                result = GoldCalculator.calculate(**state['data'])
                send_telegram_report(chat_id, result)
                
                # 重置狀態
                state['step'] = 0
                state['data'] = {}
                send_telegram_message(chat_id, "✅ 計算完成！\n\n輸入 /start 開始新的計算")
        
        return jsonify({'ok': True}), 200
    
    except Exception as e:
        print(f"Webhook 錯誤: {e}")
        return jsonify({'ok': False, 'error': str(e)}), 500


@app.route('/telegram/set-webhook', methods=['POST'])
def set_telegram_webhook():
    """設定 Telegram Webhook"""
    try:
        webhook_url = request.json.get('webhook_url')
        if not webhook_url:
            return jsonify({'error': '缺少 webhook_url'}), 400
        
        url = f"{TELEGRAM_API_URL}/setWebhook"
        payload = {'url': webhook_url}
        response = requests.post(url, json=payload, timeout=10)
        
        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False)
