import pandas as pd
from django.http import JsonResponse
import os

def extract_csv_data(request):
    ticker = request.GET.get("ticker", "").upper()  # 티커를 대문자로 받음
    page = int(request.GET.get("page", 0))  # 페이지 번호 받기

    # CSV 파일 경로 설정 (동적으로 파일을 처리)
    stock_file_path = f"core/data/{ticker}/{ticker}_REAL.csv"
    lstm1_file_path = f"core/data/{ticker}/{ticker}_LSTM1.csv"
    lstm2_file_path = f"core/data/{ticker}/{ticker}_LSTM2.csv"
    lstm3_file_path = f"core/data/{ticker}/{ticker}_LSTM3.csv"
    arima_file_path = f"core/data/{ticker}/{ticker}_ARIMA.csv"

    # 파일이 존재하는지 체크
    file_paths = {
        "Stocks": stock_file_path,
        "LSTM1": lstm1_file_path,
        "LSTM2": lstm2_file_path,
        "LSTM3": lstm3_file_path,
        "ARIMA": arima_file_path
    }

    # 각 파일을 로드하고 데이터를 처리
    chart_data = []
    
    last_stock = 0

    # Stocks 파일 처리 (라벨은 'price')
    if os.path.exists(stock_file_path):
        df = pd.read_csv(stock_file_path)
        df.columns = ["date", "price"]  # 열 이름 맞추기
        df = df.iloc[page * 25: (page + 1) * 25]  # 페이지네이션
        price_data = df[["date", "price"]].apply(
            lambda row: {"date": row["date"], "price": row["price"] if pd.notnull(row["price"]) else None}, axis=1
        ).tolist()
        chart_data.append({
            "label": "price",  # 라벨을 'price'로 설정
            "data": price_data
        })
        last_stock = price_data[-1]['price']
    else:
        return JsonResponse({"error": f"{ticker}_Stocks.csv 파일이 존재하지 않습니다."}, status=400)

    # LSTM1, LSTM2, LSTM3, ARIMA 파일 처리
    for model in ["LSTM1", "LSTM2", "LSTM3", "ARIMA"]:
        model_data = []
        if os.path.exists(file_paths[model]):
            df = pd.read_csv(file_paths[model])
            df.columns = ["date", "price"]  # 가격 열 이름을 "price"로 통일
            df = df.iloc[(page + 1) * 25: (page + 2) * 25]  # 페이지네이션
            model_data = df[["date", "price"]].apply(
                lambda row: {"date": row["date"], "price": row["price"] if pd.notnull(row["price"]) else None}, axis=1
            ).tolist()
        else:
            return JsonResponse({"error": f"{ticker}_{model}.csv 파일이 존재하지 않습니다."}, status=400)

        # 각 모델별로 데이터 라벨 추가
        chart_data.append({
            "label": model,  # 각 모델의 이름을 라벨로 설정
            "data": model_data
        })

    # 데이터를 JSON 형태로 반환
    return JsonResponse({ "data" : chart_data, "lastStock" : last_stock }, safe=False)
