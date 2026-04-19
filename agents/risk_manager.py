from utils.logger import log_prediction
from loguru import logger

def kelly_fraction(win_prob: float) -> float:
    p = win_prob
    q = 1 - p
    b = 1.0  # even odds (1:1 payout)
    kelly = (b * p - q) / b
    # Cap at 25% for safety
    return round(max(0.0, min(kelly, 0.25)), 4)

def run_risk_manager(prediction: dict, bankroll: float = 1000.0) -> dict:
    confidence = prediction["confidence"]
    signal = prediction["signal"]
    asset = prediction["asset"]

    fraction = kelly_fraction(confidence)
    bet_amount = round(bankroll * fraction, 2)

    result = {
        "asset": asset,
        "signal": signal,
        "confidence": confidence,
        "kelly_fraction": fraction,
        "bet_amount": bet_amount,
        "bankroll": bankroll,
    }

    log_prediction(
        asset=asset,
        prediction=signal,
        confidence=confidence,
        kelly_fraction=fraction,
        market_odds=confidence,
    )

    logger.info(f"[{asset}] Risk result: {result}")
    return result