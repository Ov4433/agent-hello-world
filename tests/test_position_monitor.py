import unittest

import position_monitor


class PositionMonitorTests(unittest.TestCase):
    def test_evaluate_returns_take_profit_state(self) -> None:
        result = position_monitor.evaluate(
            {
                "issue_number": 2,
                "asset": "PONS",
                "contract": "0xabc",
                "pair_address": "0xpair",
                "entry_fill_usd": 1.0,
                "entry_liquidity_usd": 1000.0,
                "scale_price_usd": 1.1,
                "stop_price_usd": 0.75,
                "take_profit_1_usd": 2.0,
                "take_profit_2_usd": 4.0,
                "structural_gate": "PASS",
            },
            {
                "priceUsd": "2.5",
                "pairAddress": "0xpair",
                "liquidity": {"usd": 1000},
                "volume": {"h24": 55},
                "txns": {"h24": {"buys": 10, "sells": 8}},
            },
        )

        self.assertEqual(result["state"], "TP1")
        self.assertEqual(result["asset"], "PONS")
        self.assertAlmostEqual(result["return_pct"], 150.0)

    def test_evaluate_uses_liquidity_warning_when_pool_drops(self) -> None:
        result = position_monitor.evaluate(
            {
                "issue_number": 2,
                "asset": "PONS",
                "contract": "0xabc",
                "pair_address": "0xpair",
                "entry_fill_usd": 1.0,
                "entry_liquidity_usd": 1000.0,
                "scale_price_usd": 1.1,
                "stop_price_usd": 0.75,
                "take_profit_1_usd": 2.0,
                "take_profit_2_usd": 4.0,
                "structural_gate": "PASS",
            },
            {
                "priceUsd": "1.05",
                "pairAddress": "0xpair",
                "liquidity": {"usd": 600},
                "volume": {"h24": 55},
                "txns": {"h24": {"buys": 10, "sells": 8}},
            },
        )

        self.assertEqual(result["state"], "LIQUIDITY_WARNING")

    def test_validate_position_rejects_missing_fields(self) -> None:
        with self.assertRaisesRegex(ValueError, "pair_address must be a non-empty string"):
            position_monitor.validate_position(
                {
                    "issue_number": 2,
                    "asset": "PONS",
                    "contract": "0xabc",
                    "pair_address": "",
                    "entry_fill_usd": 1.0,
                    "entry_liquidity_usd": 1000.0,
                    "scale_price_usd": 1.1,
                    "stop_price_usd": 0.75,
                    "take_profit_1_usd": 2.0,
                    "take_profit_2_usd": 4.0,
                    "structural_gate": "PASS",
                }
            )


if __name__ == "__main__":
    unittest.main()
