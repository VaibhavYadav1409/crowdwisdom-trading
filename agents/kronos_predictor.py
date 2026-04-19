import numpy as np
from loguru import logger

def simple_direction_signal(bars: list) -> dict:
    if len(bars) < 10:
        return {"signal": "NEUTRAL", "confidence": 0.5}

    closes = [float(b.get("close", 0)) for b in bars[-20:]]
    recent_avg = np.mean(closes[-5:])
    older_avg = np.mean(closes[:15]) if len(closes) >= 15 else closes[0]
    diff_pct = (recent_avg - older_avg) / (older_avg + 0.0001)

    if diff_pct > 0.001:
        conf = min(0.5 + abs(diff_pct) * 100, 0.85)
        return {"signal": "UP", "confidence": round(conf, 2)}
    elif diff_pct < -0.001:
        conf = min(0.5 + abs(diff_pct) * 100, 0.85)
        return {"signal": "DOWN", "confidence": round(conf, 2)}
    else:
        return {"signal": "NEUTRAL", "confidence": 0.5}

def run_kronos_predictor(asset: str, bars: list, market_signal: str) -> dict:
    tech = simple_direction_signal(bars)
    logger.info(f"[{asset}] Technical signal: {tech}")

    # Combine market signal + technical signal
    market_up = "UP" in market_signal
    tech_up = tech["signal"] == "UP"

    if market_up and tech_up:
        final_signal = "UP"
        confidence = min((tech["confidence"] + 0.1), 0.90)
    elif not market_up and not tech_up:
        final_signal = "DOWN"
        confidence = min((tech["confidence"] + 0.1), 0.90)
    else:
        # Signals disagree — lower confidence
        final_signal = tech["signal"]
        confidence = 0.52

    result = {
        "asset": asset,
        "signal": final_signal,
        "confidence": round(confidence, 2),
    }
    logger.info(f"[{asset}] Final prediction: {result}")
    return result