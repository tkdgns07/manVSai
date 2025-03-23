from django.http import JsonResponse
import numpy as np
from scipy.stats import norm

def black_scholes_call(K, S0, T=1/12, r=0.05, sigma=0.2):
    # d1과 d2 계산
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # 콜 옵션 가격 계산
    call_price = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

def black_scholes_put(K, S0, T=1/12, r=0.05, sigma=0.2):
    # d1과 d2 계산
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # 풋 옵션 가격 계산
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)
    return put_price

def optionPricing(request):
    strikePrice = float(request.GET.get("strikePrice", 0))
    lastStock = float(request.GET.get("lastStock", 0))
    
    call_premium = black_scholes_call(strikePrice, lastStock)
    put_premium = black_scholes_put(strikePrice, lastStock)
    
    option_prices = { "call" : call_premium, "put" : put_premium }
    
    return JsonResponse(option_prices, safe=False)