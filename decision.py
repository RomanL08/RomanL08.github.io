def decide_action(analysis, portfolio):
    regime = analysis["regime"]
    trigger = analysis["trigger"]
    confidence = analysis["confidence"]
    position = portfolio.position

    if position == "FLAT":
        if trigger == "Waiting":
            return "HOLD"

        if regime in ["Strong Bull", "Bull Recovery", "Bull Pullback"] and confidence >= 60:
            return "BUY"

        if regime in ["Strong Bear", "Bear Continuation", "Bear Rally"] and confidence >= 60:
            return "SHORT"

    if position == "LONG":
        if regime in ["Strong Bear", "Bear Continuation"]:
            return "EXIT LONG"

        return "HOLD"

    if position == "SHORT":
        if regime in ["Strong Bull", "Bull Recovery"]:
            return "COVER SHORT"

        return "HOLD"

    return "HOLD"