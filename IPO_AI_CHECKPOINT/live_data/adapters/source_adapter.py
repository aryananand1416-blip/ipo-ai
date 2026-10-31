from datetime import datetime, timezone


class SourceAdapter:

    def __init__(self, source_name):
        self.source_name = source_name

    def normalize(self, record):
        """
        Convert source-specific data into IPO_AI standard format.
        """

        normalized = {
            "timestamp": record.get(
                "timestamp",
                datetime.now(timezone.utc).isoformat()
            ),
            "source": self.source_name,
            "exchange": record.get("exchange"),
            "symbol": record.get("symbol"),
            "ipo_id": record.get("ipo_id"),
            "ipo_name": record.get("ipo_name"),
            "price": record.get("price"),
            "open": record.get("open"),
            "high": record.get("high"),
            "low": record.get("low"),
            "close": record.get("close"),
            "volume": record.get("volume"),
            "market_cap": record.get("market_cap"),
            "status": record.get("status", "LIVE")
        }

        return normalized

    def health(self):
        return {
            "source": self.source_name,
            "status": "adapter_ready"
        }
