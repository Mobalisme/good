import eel
import yfinance as yf
import requests
import json
import os
import pandas as pd
from datetime import datetime

# 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIARY_FILE = os.path.join(BASE_DIR, 'diary.json')

# 웹 폴더 초기화
eel.init('web')

# # 상위 10위 주식 데이터 가져오기
# def get_top_stocks():
#     stock_symbols = ['005930.KS', '000660.KS', '035420.KS', '051910.KS', '005380.KS', 
#                      '003550.KS', '017670.KS', '066570.KS', '032830.KS', '000270.KS']
#     stocks = []

#     for symbol in stock_symbols:
#         try:
#             stock_data = yf.Ticker(symbol)
#             stock_info = stock_data.history(period="2d")
#             if stock_info.empty:
#                 print(f"No data available for symbol: {symbol}")
#                 continue
            
#             stock_name = stock_data.info.get('Name', symbol)  # 주식 이름 또는 기본 심볼 반환
#             stock_price_yesterday = float(stock_info['Close'][-2])
#             stock_price_today = float(stock_info['Close'][-1])
#             market_cap = stock_data.info.get('marketCap', 'N/A')
#             per = stock_data.info.get('trailingPE', 'N/A')
#             pbr = stock_data.info.get('priceToBook', 'N/A')

#             stocks.append({
#                 'name': stock_name,
#                 'symbol': symbol,
#                 'price_yesterday': stock_price_yesterday,
#                 'price_today': stock_price_today,
#                 'market_cap': market_cap,
#                 'per': per,
#                 'pbr': pbr
#             })
#         except Exception as e:
#             print(f"Error fetching data for {symbol}: {e}")
#     return stocks

# # 암호화폐 데이터 가져오기
# def get_crypto_data():
#     try:
#         response = requests.get("https://api.coinpaprika.com/v1/tickers?quotes=KRW")
#         if response.status_code != 200:
#             print(f"Error fetching data: {response.status_code}")
#             return []

#         data = response.json()
#         coins = data[:10]  # 상위 10개 암호화폐 데이터 선택

#         # 필요한 데이터 가공
#         result = []
#         for coin in coins:
#             name = coin['name']
#             price_today = coin['quotes']['KRW']['price']  # 오늘의 가격
#             percent_change_24h = coin['quotes']['KRW'].get('percent_change_24h', None)

#             if percent_change_24h is not None:
#                 price_yesterday = price_today / (1 + percent_change_24h / 100)
#             else:
#                 price_yesterday = None

#             result.append({
#                 "name": name,
#                 "price_yesterday": price_yesterday,
#                 "price_today": price_today
#             })

#         return result
#     except Exception as e:
#         print(f"Error: {e}")
#         return []

# 암호화폐 데이터 가져오기
def get_crypto_data():
    try:
        response = requests.get("https://api.coinpaprika.com/v1/tickers?quotes=KRW")
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            return []

        data = response.json()

        # 필요한 데이터 가공
        result = []
        for coin in data:
            name = coin['name']
            price_now = coin['quotes']['KRW']['price']  # 오늘의 가격
            percent_change_15m = coin['quotes']['KRW'].get('percent_change_15m', None)
            price_15m = price_now / (1 + percent_change_15m / 100) if percent_change_15m is not None else None
            percent_change_30m = coin['quotes']['KRW'].get('percent_change_30m', None)
            price_30m = price_now / (1 + percent_change_30m / 100) if percent_change_30m is not None else None
            percent_change_1h = coin['quotes']['KRW'].get('percent_change_1h', None)
            price_1h = price_now / (1 + percent_change_1h / 100) if percent_change_1h is not None else None
            percent_change_6h = coin['quotes']['KRW'].get('percent_change_6h', None)
            price_6h = price_now / (1 + percent_change_6h / 100) if percent_change_6h is not None else None
            result.append({
                "name": name,
                "price_15m": price_15m,
                "price_30m": price_30m,
                "price_1h": price_1h,
                "price_6h": price_6h,
                "price_now": price_now
            })

        # 가격을 기준으로 내림차순 정렬 후 상위 7개 선택
        result = sorted(result, key=lambda x: x['price_now'], reverse=True)[:7]
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []

# 일기 저장 기능
def save_diary(date, mood, text, chart_data):
    try:
        diary_entry = {
            'date': date,
            'mood': mood,
            'text': text,
            'chart_data': chart_data
        }

        diaries = []
        if os.path.exists(DIARY_FILE):
            try:
                with open(DIARY_FILE, 'r', encoding='utf-8') as f:
                    diaries = json.load(f)
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error: {e}")
                diaries = []

        diaries.append(diary_entry)

        with open(DIARY_FILE, 'w', encoding='utf-8') as f:
            json.dump(diaries, f, ensure_ascii=False, indent=4)

        return diaries
    except Exception as e:
        print(f"Error saving diary: {e}")
        return []

# Eel에 함수 노출
@eel.expose
def fetch_crypto_data():
    return get_crypto_data()

# @eel.expose
# def fetch_stock_data():
#     return get_top_stocks()

@eel.expose
def save_diary_entry(date, mood, text, chart_data):
    return save_diary(date, mood, text, chart_data)

# Eel 서버 시작
try:
    eel.start('index.html', block=False)

    # 데이터 30초마다 갱신
    while True:
        eel.sleep(30)
except Exception as e:
    print(f"Error starting Eel server: {e}")
