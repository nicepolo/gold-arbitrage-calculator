import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 設定 Port，支援 Railway 環境變數
PORT = int(os.environ.get("PORT", 8080))

# 模擬數據存儲（實際應用應使用數據庫）
calculations_history = []


def calculate_arbitrage(gold_weight, buy_price, sell_price, exchange_rate, 
                       ticket_cost, hotel_cost, meal_cost, transport_cost, channel_cost):
    """
    計算黃金跨境套利利潤
    
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
    
    # 將克轉換為錢（1錢 = 3.75克）
    mace = gold_weight / 3.75
    
    # 計算營收：越南賣價 × 錢數 × 匯率
    # sell_price 單位是萬 VND，所以需要乘以 10000
    revenue = sell_price * mace * exchange_rate * 10000
    
    # 計算成本
    # 台灣購買成本
    purchase_cost = buy_price * mace
    
    # 開銷總和
    total_expenses = ticket_cost + hotel_cost + meal_cost + transport_cost + channel_cost
    
    # 總成本 = 購買成本 + 開銷
    total_cost = purchase_cost + total_expenses
    
    # 毛利 = 營收 - 購買成本
    gross_profit = revenue - purchase_cost
    
    # 淨利 = 毛利 - 開銷
    net_profit = gross_profit - total_expenses
    
    # 介紹費 = 淨利 × 10%
    introduction_fee = net_profit * 0.10
    
    # 最終淨利 = 淨利 - 介紹費
    final_net_profit = net_profit - introduction_fee
    
    # 利潤率
    profit_margin = (final_net_profit / revenue * 100) if revenue > 0 else 0
    
    return {
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
        'introduction_fee': round(introduction_fee, 2),
        'final_net_profit': round(final_net_profit, 2),
        'profit_margin': round(profit_margin, 2),
        'timestamp': datetime.now().isoformat()
    }


@app.route('/')
def index():
    """主頁面"""
    return render_template('index.html')


@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    """計算 API 端點"""
    try:
        data = request.json
        
        # 驗證必要欄位
        required_fields = ['gold_weight', 'buy_price', 'sell_price', 'exchange_rate']
        for field in required_fields:
            if field not in data or data[field] is None:
                return jsonify({'error': f'缺少必要欄位: {field}'}), 400
        
        # 提取數據，設定預設值為 0
        result = calculate_arbitrage(
            gold_weight=float(data.get('gold_weight', 0)),
            buy_price=float(data.get('buy_price', 0)),
            sell_price=float(data.get('sell_price', 0)),
            exchange_rate=float(data.get('exchange_rate', 0)),
            ticket_cost=float(data.get('ticket_cost', 0)),
            hotel_cost=float(data.get('hotel_cost', 0)),
            meal_cost=float(data.get('meal_cost', 0)),
            transport_cost=float(data.get('transport_cost', 0)),
            channel_cost=float(data.get('channel_cost', 0))
        )
        
        # 保存到歷史記錄
        calculations_history.append(result)
        
        return jsonify(result), 200
    
    except ValueError as e:
        return jsonify({'error': f'數值錯誤: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'計算錯誤: {str(e)}'}), 500


@app.route('/api/history', methods=['GET'])
def api_history():
    """獲取計算歷史"""
    return jsonify(calculations_history[-20:]), 200  # 返回最後 20 筆記錄


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False)
