import json
from loguru import logger

def load_recent_predictions(n: int = 10) -> list:
    results = []
    try:
        with open("logs/predictions.jsonl", "r", encoding="utf-8") as f:
            lines = f.readlines()[-n:]
            for line in lines:
                entry = json.loads(line)
                results.append(entry.get("record", entry))
    except FileNotFoundError:
        logger.warning("No prediction log found yet.")
    return results

def run_feedback_loop() -> str:
    recent = load_recent_predictions(10)

    if not recent:
        return "No prediction history yet — run a few cycles first."

    up_count = sum(1 for r in recent if r.get("extra", {}).get("prediction") == "UP")
    down_count = sum(1 for r in recent if r.get("extra", {}).get("prediction") == "DOWN")
    avg_confidence = sum(
        r.get("extra", {}).get("confidence", 0.5) for r in recent
    ) / len(recent)
    avg_kelly = sum(
        r.get("extra", {}).get("kelly_fraction", 0) for r in recent
    ) / len(recent)

    summary = (
        f"\n{'='*40}\n"
        f"  FEEDBACK LOOP SUMMARY ({len(recent)} predictions)\n"
        f"  UP signals:       {up_count}\n"
        f"  DOWN signals:     {down_count}\n"
        f"  Avg confidence:   {avg_confidence:.0%}\n"
        f"  Avg Kelly bet:    {avg_kelly:.1%} of bankroll\n"
        f"{'='*40}"
    )

    logger.info(summary)
    return summary