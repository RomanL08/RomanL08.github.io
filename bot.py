import time
import os
import portfolio

from decision import decide_action

from datetime import datetime

from config import *
from kraken import get_ticker, get_candles
from indicators import sma, rsi
from strategy import smart_strategy

from analysis import analyze_signal

last_signal = None

candles = get_candles(pair=PAIR)
latest_candle = candles[-2]
last_candle_update = 0

while True:
    os.system("cls")

    ticker = get_ticker(pair=PAIR)
    price = ticker["price"]

    spread = ticker["ask"] - ticker["bid"]
    spread_pct = (spread / ticker["ask"]) * 100

    now = time.time()

    if now - last_candle_update >= CANDLE_UPDATE_INTERVAL:
        candles = get_candles(pair=PAIR)
        last_candle_update = now

        latest_candle = candles[-2]

        print(
            f"NEW CANDLE | "
            f"O {latest_candle['open']:.2f} | "
            f"H {latest_candle['high']:.2f} | "
            f"L {latest_candle['low']:.2f} | "
            f"C {latest_candle['close']:.2f} | "
            f"Vol {latest_candle['volume']:.6f} | "
            f"Trades {latest_candle['count']}"
        )

    vwap_status = "Close > VWAP" if latest_candle["close"] > latest_candle["vwap"] else "Close < VWAP"
    live_vwap_status = "Price > VWAP" if price > latest_candle["vwap"] else "Price < VWAP"

    candle_vwap_diff = latest_candle["close"] - latest_candle["vwap"]
    candle_vwap_diff_pct = (candle_vwap_diff / latest_candle["vwap"]) * 100

    live_vwap_diff = price - latest_candle["vwap"]
    live_vwap_diff_pct = (live_vwap_diff / latest_candle["vwap"]) * 100

    closes = [candle["close"] for candle in candles]

    sma20 = sma(closes, SMA_FAST)
    sma50 = sma(closes, SMA_SLOW)

    previous_sma20 = sma(closes[:-1], SMA_FAST)
    previous_sma50 = sma(closes[:-1], SMA_SLOW)

    rsi14 = rsi(closes, RSI_PERIOD)

    analysis = analyze_signal(
        price,
        latest_candle,
        sma20,
        sma50,
        previous_sma20,
        previous_sma50,
        rsi14
    )

    reasons = analysis["reasons"]

    signal = decide_action(analysis, portfolio)

    trade_action = "Geen trade"

    if signal != last_signal:
        if signal == "BUY":
            if portfolio.cash > 0:
                portfolio.buy(ticker["ask"], spread)
                trade_action = f"BUY uitgevoerd @ Ask €{ticker['ask']:.2f}"
            else:
                trade_action = "BUY signaal, maar geen cash beschikbaar"

        elif signal == "SELL":
            if portfolio.btc > 0:
                portfolio.sell(ticker["bid"], spread)
                trade_action = f"SELL uitgevoerd @ Bid €{ticker['bid']:.2f}"
            else:
                trade_action = "SELL signaal, maar geen BTC om te verkopen"

        last_signal = signal

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 45)
    print("KRAKEN BTC/EUR BOT")
    print("=" * 45)
    print(f"Time      : {current_time}")
    print()

    print("Market")
    print(f"Price     : €{price:.2f}")
    print(f"Bid       : €{ticker['bid']:.2f}")
    print(f"Ask       : €{ticker['ask']:.2f}")
    print(f"Spread    : €{spread:.2f} ({spread_pct:.3f}%)")
    print()

    print("Indicators")
    print(f"SMA20     : €{sma20:.2f}")
    print(f"SMA50     : €{sma50:.2f}")
    print(f"RSI14     : {rsi14:.2f}")
    print()

    close_arrow = "▲" if candle_vwap_diff > 0 else "▼"
    live_arrow = "▲" if live_vwap_diff > 0 else "▼"

    print("VWAP Analysis")
    print(f"VWAP      : €{latest_candle['vwap']:.2f}")
    print(f"Close     : €{latest_candle['close']:.2f} {close_arrow} {candle_vwap_diff:+.2f}€ ({candle_vwap_diff_pct:+.3f}%)")
    print(f"Live      : €{price:.2f} {live_arrow} {live_vwap_diff:+.2f}€ ({live_vwap_diff_pct:+.3f}%)")
    print()

    print("Portfolio")
    profit = portfolio.total_value(price) - 10000
    profit_pct = (profit / 10000) * 100
    print(f"Cash      : €{portfolio.cash:.2f}")
    print(f"BTC       : {portfolio.btc:.6f}")
    print(f"Position : {portfolio.position}")

    if portfolio.entry_price is not None:
        print(f"Entry    : €{portfolio.entry_price:.2f}")
    else:
        print("Entry    : -")

    if portfolio.position == "LONG":
        open_profit = (price - portfolio.entry_price) * portfolio.btc
        open_profit_pct = ((price - portfolio.entry_price) / portfolio.entry_price) * 100
        print(f"Open P/L : {open_profit:+.2f}€ ({open_profit_pct:+.2f}%)")
    else:
        print("Open P/L : -")    

    print(f"Total     : €{portfolio.total_value(price):.2f}")
    print(f"P/L       : {profit:+.2f}€ ({profit_pct:+.2f}%)")
    print()
    print("Market Analysis")
    print(f"Regime     : {analysis['regime']}")
    print(f"Strategy   : {analysis['strategy_mode']}")
    print(f"Opportunity : {analysis['opportunity']}")
    print(f"Trend      : {analysis['trend']}")
    print(f"Momentum   : {analysis['momentum']}")
    print(f"RSI State  : {analysis['strength']}")
    print(f"Entry      : {analysis['trigger']}")
    print(f"Score      : {analysis['score']:+}")
    print(f"Confidence : {analysis['confidence']}%")
    print(f"Bias       : {analysis['bias']}")
    print()

    print("Market Story")

    for line in analysis["market_story"]:
        print(f"• {line}")

    print()
    print("Trading Plan")
    print(f"Action      : {signal}")
    print(f"Reason      : {analysis['trading_plan']['reason']}")
    print(f"Opportunity : {analysis['trading_plan']['opportunity']}")
    print(f"Next Step   : {analysis['trading_plan']['next_step']}")
    print()
    print("Entry Checklist")

    for line in analysis["entry_checklist"]:
        print(line)

    print()

    print("=" * 45)
    time.sleep(UPDATE_INTERVAL)