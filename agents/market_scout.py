import requests
from loguru import logger

def get_market_signal(asset: str) -> dict:
    # Use Binance public API — no key needed, never times out
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        resp = requests.get(url, params={"symbol": f"{asset}USDT"}, timeout=10)
        data = resp.json()
        change_pct = float(data.get("priceChangePercent", 0))
        price = float(data.get("lastPrice", 0))
        logger.info(f"[{asset}] Binance 24h change: {change_pct:.2f}%  Price: ${price:,.2f}")
        return {"change_pct": change_pct, "price": price}
    except Exception as e:
        logger.error(f"Binance ticker failed for {asset}: {e}")
        return {"change_pct": 0, "price": 0}

def run_market_scout(asset: str) -> str:
    data = get_market_signal(asset)
    change = data["change_pct"]
    price = data["price"]

    if change > 1.0:
        signal = f"SIGNAL: UP | CONFIDENCE: 70% | Price: ${price:,.2f} (+{change:.1f}%)"
    elif change < -1.0:
        signal = f"SIGNAL: DOWN | CONFIDENCE: 70% | Price: ${price:,.2f} ({change:.1f}%)"
    else:
        conf = 50 + abs(change) * 10
        direction = "UP" if change >= 0 else "DOWN"
        signal = f"SIGNAL: {direction} | CONFIDENCE: {conf:.0f}% | Price: ${price:,.2f} ({change:+.1f}%)"

    logger.info(f"[{asset}] Market scout signal: {signal}")
    return signal