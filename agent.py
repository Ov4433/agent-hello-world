"""Dependency-free Bitcoin price monitor."""

import os

from workflow_utils import request_json, write_github_output


API_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
    "?ids=bitcoin&vs_currencies=usd"
)


def fetch_bitcoin_price() -> float:
    payload = request_json(API_URL)
    try:
        return float(payload["bitcoin"]["usd"])
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError("CoinGecko response did not include bitcoin.usd") from exc


def main() -> None:
    try:
        threshold = float(os.getenv("BTC_ALERT_ABOVE_USD", "150000"))
        force_alert = os.getenv("FORCE_ALERT", "false").lower() == "true"
        price = fetch_bitcoin_price()
        should_alert = force_alert or price >= threshold

        print(f"Bitcoin price: ${price:,.2f}")
        print(f"Alert threshold: ${threshold:,.2f}")
        print(f"Should alert: {should_alert}")

        write_github_output("price", f"{price:.2f}")
        write_github_output("threshold", f"{threshold:.2f}")
        write_github_output("should_alert", str(should_alert).lower())
        write_github_output("forced", str(force_alert).lower())
    except Exception as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
