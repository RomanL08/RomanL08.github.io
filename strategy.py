def smart_strategy(analysis):
    regime = analysis["regime"]
    bias = analysis["bias"]
    trigger = analysis["trigger"]
    confidence = analysis["confidence"]

    if trigger == "Waiting":
        return "HOLD"

    if bias == "Bullish" and regime in ["Strong Bull", "Bull Recovery", "Bull Pullback"]:
        if confidence >= 50:
            return "BUY"

    if bias == "Bearish" and regime in ["Strong Bear", "Bear Continuation"]:
        if confidence >= 50:
            return "SELL"

    return "HOLD"