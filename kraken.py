import requests


BASE_URL = "https://api.kraken.com/0/public"


def get_ticker(pair="XBTEUR"):
    url = f"{BASE_URL}/Ticker"
    params = {"pair": pair}

    response = requests.get(url, params=params)
    data = response.json()

    if data["error"]:
        raise Exception(data["error"])

    result = data["result"]
    pair_key = list(result.keys())[0]

    ticker = result[pair_key]

    return {
        "pair": pair,
        "price": float(ticker["c"][0]),
        "bid": float(ticker["b"][0]),
        "ask": float(ticker["a"][0]),
        "high": float(ticker["h"][1]),
        "low": float(ticker["l"][1]),
        "volume": float(ticker["v"][1]),
    }


def get_candles(pair="XBTEUR", interval=1):
    url = f"{BASE_URL}/OHLC"
    params = {
        "pair": pair,
        "interval": interval
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["error"]:
        raise Exception(data["error"])

    result = data["result"]
    pair_key = [key for key in result.keys() if key != "last"][0]

    candles = []

    for candle in result[pair_key]:
        candles.append({
            "time": int(candle[0]),
            "open": float(candle[1]),
            "high": float(candle[2]),
            "low": float(candle[3]),
            "close": float(candle[4]),
            "vwap": float(candle[5]),
            "volume": float(candle[6]),
            "count": int(candle[7]),
        })

    return candles


def get_orderbook(pair="XBTEUR", count=10):
    url = f"{BASE_URL}/Depth"
    params = {
        "pair": pair,
        "count": count
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["error"]:
        raise Exception(data["error"])

    result = data["result"]
    pair_key = list(result.keys())[0]

    return result[pair_key]


if __name__ == "__main__":
    ticker = get_ticker()
    print("Ticker:", ticker)

    candles = get_candles()
    print("Laatste candle:", candles[-1])

    orderbook = get_orderbook()
    print("Beste bid:", orderbook["bids"][0])
    print("Beste ask:", orderbook["asks"][0])