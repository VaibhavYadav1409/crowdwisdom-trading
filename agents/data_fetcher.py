import requests
from loguru import logger

def fetch_ohlcv(asset: str, limit: int = 100) -> list:
    """Fetch OHLCV candles directly from Binance public API (no key needed)."""
    try:
        logger.info(f"Fetching {limit} OHLCV bars for {asset} from Binance...")
        url = "https://api.binance.com/api/v3/klines"
        params = {"symbol": f"{asset}USDT", "interval": "5m", "limit": limit}
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        raw = resp.json()
        bars = [
            {
                "open":   float(r[1]),
                "high":   float(r[2]),
                "low":    float(r[3]),
                "close":  float(r[4]),
                "volume": float(r[5]),
            }
            for r in raw
        ]
        logger.info(f"Fetched {len(bars)} bars for {asset}")
        return bars
    except Exception as e:
        logger.error(f"Binance fetch failed for {asset}: {e}")
        return [{"close": 60000 + i * 10, "open": 60000,
                 "high": 60100, "low": 59900, "volume": 100}
                for i in range(20)]