from datetime import datetime

cash = 10000.0      # Startsaldo in euro
btc = 0.0           # Aantal BTC in bezit
trades = []

position = "FLAT"   # FLAT, LONG, SHORT
entry_price = None

def buy(price, spread):
    global cash, btc, position, entry_price

    if cash > 0:
        btc = cash / price
        cash = 0

        position = "LONG"
        entry_price = price

        trades.append({
            "type": "BUY",
            "price": price,
            "btc": btc,
            "spread": spread,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})

def sell(price, spread):
    global cash, btc, position, entry_price

    if btc > 0:
        cash = btc * price
        btc = 0

        position = "FLAT"
        entry_price = None

        trades.append({
            "type": "SELL",
            "price": price,
            "btc": btc,
            "spread": spread,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

def total_value(price):
    return cash + btc * price
