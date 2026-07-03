from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

from picnic_adapter import optimize_picnic_basket  # noqa: E402


def test_weather_penalties_change_the_winner():
    items = [
        {"id": "ice_cream", "name": "Ice cream", "weight": 2, "happiness": 10, "heat_penalty": 9, "rain_penalty": 0},
        {"id": "fruit", "name": "Fruit", "weight": 2, "happiness": 6, "heat_penalty": 0, "rain_penalty": 0},
        {"id": "water", "name": "Water", "weight": 1, "happiness": 3, "heat_penalty": 0, "rain_penalty": 0},
    ]
    cool = optimize_picnic_basket(items, {"max_weight": 3, "heat": 2, "rain": 0})
    hot = optimize_picnic_basket(items, {"max_weight": 3, "heat": 8, "rain": 0})
    assert cool["selected_ids"] == ["ice_cream", "water"]
    assert hot["selected_ids"] == ["fruit", "water"]


if __name__ == "__main__":
    test_weather_penalties_change_the_winner()
    print("PASS test_weather_penalties_change_the_winner")
