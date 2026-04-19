from loguru import logger
import os

os.makedirs("logs", exist_ok=True)
logger.add("logs/predictions.jsonl", serialize=True, rotation="10 MB")

def log_prediction(asset, prediction, confidence, kelly_fraction, market_odds):
    entry = {
        "asset": asset,
        "prediction": prediction,
        "confidence": confidence,
        "kelly_fraction": kelly_fraction,
        "market_odds": market_odds,
    }
    logger.info("Prediction logged", **entry)
    return entry