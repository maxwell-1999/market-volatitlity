import math
import time

import requests


def RawSD(close_prices):
    mean = sum(close_prices) / len(close_prices)
    diff = [(close_prices[i] - mean) ** 2 for i in range(len(close_prices))]
    varience = sum(diff) / (len(close_prices) - 1)
    sd = math.sqrt(varience)
    return sd


def returnSD(close_prices):
    log_returns = [
        (close_prices[i] / close_prices[i - 1] - 1) for i in range(1, len(close_prices))
    ]

    historical_volatility = RawSD(log_returns)

    return historical_volatility


def logReturnSD(close_prices):
    log_returns = [
        math.log(close_prices[i] / close_prices[i - 1])
        for i in range(1, len(close_prices))
    ]

    historical_volatility = RawSD(log_returns)

    return historical_volatility


def calc(days=1, resolution=5):
    end_time = math.ceil(time.time() - 60)
    start_time = math.ceil(end_time) - days * 24 * 60 * 60
    request_url = f"https://pyth-api.vintage-orange-muffin.com/v2/history?from={start_time}&to={end_time}&resolution={resolution}&symbol=ETH%2FUSD"
    r = requests.get(request_url)
    prices = r.json()
    if "c" in prices:
        rawVolatility = returnSD(
            [
                float(i)
                for i in "147.82,149.5,149.78,149.86,149.93,150.89,152.39,153.74,152.79,151.23,151.78".split(
                    ","
                )
            ]
        )
        logVolatility = logReturnSD(
            [
                float(i)
                for i in "147.82,149.5,149.78,149.86,149.93,150.89,152.39,153.74,152.79,151.23,151.78".split(
                    ","
                )
            ]
        )
        print("Log Volatility: ", logVolatility)
        print("Historical Volatility:", rawVolatility)
    else:
        print("error while fetching data ", prices,
              " for request : ", request_url)


calc(1, 5)
