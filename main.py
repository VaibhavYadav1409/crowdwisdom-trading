from agents.market_scout import run_market_scout
from agents.data_fetcher import fetch_ohlcv
from agents.kronos_predictor import run_kronos_predictor
from agents.risk_manager import run_risk_manager
from agents.feedback_loop import run_feedback_loop
from loguru import logger

ASSETS = ["BTC", "ETH"]
BANKROLL = 1000.0

def run_pipeline():
    logger.info("=== CrowdWisdom Trading Pipeline Starting ===")
    results = []

    for asset in ASSETS:
        logger.info(f"--- Processing {asset} ---")

        market_signal = run_market_scout(asset)
        bars = fetch_ohlcv(asset, limit=100)
        prediction = run_kronos_predictor(asset, bars, market_signal)
        risk = run_risk_manager(prediction, bankroll=BANKROLL)

        results.append(risk)
        print(f"\n{'='*40}")
        print(f"  {asset}")
        print(f"  Signal:     {risk['signal']}")
        print(f"  Confidence: {risk['confidence']:.0%}")
        print(f"  Bet size:   ${risk['bet_amount']} of ${BANKROLL}")
        print(f"{'='*40}\n")

    feedback = run_feedback_loop()
    print(feedback)
    return results

if __name__ == "__main__":
    run_pipeline()