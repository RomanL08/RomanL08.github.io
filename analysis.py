def analyze_signal(
    price,
    latest_candle,
    sma20,
    sma50,
    previous_sma20,
    previous_sma50,
    rsi14
):
    reasons = []
    score = 0

    close = latest_candle["close"]
    vwap = latest_candle["vwap"]

    # 1. SMA crossover trigger
    if previous_sma20 <= previous_sma50 and sma20 > sma50:
        trigger = "Bullish crossover"
        reasons.append("✓ Bullish SMA crossover detected")
        score += 30
    elif previous_sma20 >= previous_sma50 and sma20 < sma50:
        trigger = "Bearish crossover"
        reasons.append("✓ Bearish SMA crossover detected")
        score -= 30
    else:
        trigger = "Waiting"
        reasons.append("• Waiting for SMA crossover")

    # 2. Trend
    if sma20 > sma50:
        trend = "Bullish"
        reasons.append("✓ Trend bullish (SMA20 > SMA50)")
        score += 25
    else:
        trend = "Bearish"
        reasons.append("✓ Trend bearish (SMA20 < SMA50)")
        score -= 25

    # 3. VWAP state
    close_above_vwap = close > vwap
    live_above_vwap = price > vwap

    if close_above_vwap and live_above_vwap:
        momentum = "Bullish continuation"
        reasons.append("✓ Close and live price above VWAP")
        score += 20

    elif not close_above_vwap and not live_above_vwap:
        momentum = "Bearish continuation"
        reasons.append("✓ Close and live price below VWAP")
        score -= 20

    elif not close_above_vwap and live_above_vwap:
        momentum = "Bullish VWAP reclaim"
        reasons.append("✓ Price reclaimed VWAP after bearish candle")
        score += 15

    else:
        momentum = "Bearish VWAP rejection"
        reasons.append("⚠ Price lost VWAP after bullish candle")
        score -= 15

    # Market regime
    if trend == "Bullish":
        if momentum == "Bullish continuation":
            regime = "Strong Bull"
        elif momentum == "Bullish VWAP reclaim":
            regime = "Bull Recovery"
        else:
            regime = "Bull Pullback"

    elif trend == "Bearish":
        if momentum == "Bearish continuation":
            regime = "Strong Bear"
        elif momentum == "Bearish VWAP rejection":
            regime = "Bear Continuation"
        else:
            regime = "Bear Rally"

    else:
        regime = "Range"

    # Strategy mode
    if regime in ["Strong Bull", "Strong Bear"]:
        strategy_mode = "Trend Following"

    elif regime in ["Bull Pullback", "Bear Rally"]:
        strategy_mode = "Mean Reversion Watch"

    else:
        strategy_mode = "Wait"

    # 4. RSI strength
    if rsi14 > 70:
        strength = "Overbought"
        reasons.append("⚠ RSI overbought - possible pullback")
        score -= 10
    elif rsi14 < 30:
        strength = "Oversold"
        reasons.append("⚠ RSI oversold - possible rebound")
        score += 10
    else:
        strength = "Neutral"
        reasons.append("✓ RSI neutral")

    # 5. Bias
    if score >= 35:
        bias = "Bullish"
    elif score <= -35:
        bias = "Bearish"
    else:
        bias = "Neutral"

    confidence = 0

    if regime in ["Strong Bull", "Strong Bear"]:
        confidence += 25

    if momentum in ["Bullish continuation", "Bearish continuation"]:
        confidence += 25

    if trigger != "Waiting":
        confidence += 25

    if strength == "Neutral":
        confidence += 15
    else:
        confidence += 10
    
    # Trade assessment
    assessment = []

    if regime == "Strong Bull":
        assessment.append("Strong bullish trend. Trend-following longs are favored.")

    elif regime == "Bull Recovery":
        assessment.append("Bullish recovery is developing. Momentum is improving.")

    elif regime == "Bull Pullback":
        assessment.append("Bullish trend with temporary weakness. Watch for dip-buy setup.")

    elif regime == "Strong Bear":
        assessment.append("Strong bearish trend. Long positions are risky.")

    elif regime == "Bear Continuation":
        assessment.append("Bearish trend is continuing. Selling pressure remains dominant.")

    elif regime == "Bear Rally":
        assessment.append("Temporary rally inside a bearish trend. Watch for short opportunities.")

    else:
        assessment.append("Market is ranging or unclear. Patience is advised.")

    if strategy_mode == "Trend Following":
        assessment.append("Trend-following strategy is active.")

    elif strategy_mode == "Mean Reversion Watch":
        assessment.append("Mean-reversion opportunity is being watched.")

    else:
        assessment.append("No clear strategy has an edge.")

    if trigger == "Waiting":
        assessment.append("No confirmed entry signal yet.")
    else:
        assessment.append(f"Entry trigger confirmed: {trigger}")

    if confidence >= 70:
        assessment.append("High conviction setup.")
    elif confidence >= 40:
        assessment.append("Moderate conviction.")
    else:
        assessment.append("Low conviction. Wait for more confirmation.")

    entry_checklist = []

    if trend == "Bullish":
        entry_checklist.append("✓ Bullish trend")
    else:
        entry_checklist.append("✓ Bearish trend")

    if momentum in ["Bullish continuation", "Bullish VWAP reclaim"]:
        entry_checklist.append("✓ Bullish momentum")
    elif momentum in ["Bearish continuation", "Bearish VWAP rejection"]:
        entry_checklist.append("✓ Bearish momentum")
    else:
        entry_checklist.append("○ Momentum unclear")

    if trigger != "Waiting":
        entry_checklist.append("✓ SMA crossover confirmed")
    else:
        entry_checklist.append("○ Waiting for SMA crossover")

    if strength == "Neutral":
        entry_checklist.append("✓ RSI healthy")
    elif strength == "Oversold":
        entry_checklist.append("⚠ RSI oversold")
    elif strength == "Overbought":
        entry_checklist.append("⚠ RSI overbought")

    opportunity = "Wait"

    if regime == "Strong Bull":
        opportunity = "Trend continuation long"

    elif regime == "Bull Recovery":
        opportunity = "Recovery long setup"

    elif regime == "Bull Pullback":
        opportunity = "Buy the dip"

    elif regime == "Strong Bear":
        opportunity = "Trend continuation short"

    elif regime == "Bear Continuation":
        opportunity = "Short the weakness"

    elif regime == "Bear Rally":
        opportunity = "Sell the rally"

    else:
        opportunity = "Wait"

    market_story = []

    if regime == "Strong Bull":
        market_story.append("The market is in a strong bullish trend.")
        market_story.append("Buyers are in control and momentum supports the move.")
        market_story.append("The best opportunities are trend-following long entries.")

    elif regime == "Bull Recovery":
        market_story.append("The market is attempting a bullish recovery.")
        market_story.append("Price has reclaimed VWAP, showing improving buyer strength.")
        market_story.append("A confirmed entry trigger is still needed before buying.")

    elif regime == "Bull Pullback":
        market_story.append("The main trend is bullish, but price is pulling back.")
        market_story.append("This may become a dip-buy opportunity if buyers return.")
        market_story.append("Wait for bullish confirmation before entering.")

    elif regime == "Strong Bear":
        market_story.append("The market is in a strong bearish trend.")
        market_story.append("Sellers are in control and momentum supports the move lower.")
        market_story.append("Long positions are risky until the market stabilizes.")

    elif regime == "Bear Continuation":
        market_story.append("The bearish trend is continuing.")
        market_story.append("Selling pressure remains dominant.")
        market_story.append("Short opportunities are preferred after weak rallies.")

    elif regime == "Bear Rally":
        market_story.append("The market is rallying inside a bearish trend.")
        market_story.append("This recovery may be temporary unless buyers break the trend.")
        market_story.append("Avoid chasing longs and wait for bearish confirmation.")

    else:
        market_story.append("The market is unclear or ranging.")
        market_story.append("There is no strong directional edge right now.")
        market_story.append("Waiting for confirmation is the safest approach.")

    trading_plan = {}

    if trigger == "Waiting":
        trading_plan["reason"] = "No confirmed entry trigger yet."
    else:
        trading_plan["reason"] = f"Entry trigger confirmed: {trigger}"

    trading_plan["opportunity"] = opportunity

    if trigger == "Waiting":
        if regime in ["Strong Bull", "Bull Recovery", "Bull Pullback"]:
            trading_plan["next_step"] = "Wait for bullish entry confirmation."
        elif regime in ["Strong Bear", "Bear Continuation", "Bear Rally"]:
            trading_plan["next_step"] = "Wait for bearish entry confirmation."
        else:
            trading_plan["next_step"] = "Wait for clearer market structure."
    else:
        trading_plan["next_step"] = f"Act on confirmed trigger: {trigger}"

    return {
        "trend": trend,
        "momentum": momentum,
        "strength": strength,
        "trigger": trigger,
        "score": score,
        "confidence": confidence,
        "bias": bias,
        "regime": regime,
        "strategy_mode": strategy_mode,
        "reasons": reasons,
        "assessment": assessment,
        "entry_checklist": entry_checklist,
        "opportunity": opportunity,
        "market_story": market_story,
        "trading_plan": trading_plan,
    }