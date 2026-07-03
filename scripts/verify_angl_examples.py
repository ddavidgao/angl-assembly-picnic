from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

from picnic_adapter import optimize_picnic_basket  # noqa: E402


def _extract_examples(text: str) -> list[dict]:
    examples = []
    current = None
    pending = None
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("### "):
            if current:
                examples.append(current)
            current = {"name": line[4:].strip(), "inputs": {}, "returns": None}
            pending = None
        elif current and line.startswith("Input `"):
            match = re.match(r"Input `([^`]+)`:", line)
            pending = ("input", match.group(1))
        elif current and line == "Returns:":
            pending = ("returns", None)
        elif current and line == "```json":
            block = []
            i += 1
            while i < len(lines) and lines[i].strip() != "```":
                block.append(lines[i])
                i += 1
            value = json.loads("\n".join(block))
            if pending and pending[0] == "input":
                current["inputs"][pending[1]] = value
            elif pending and pending[0] == "returns":
                current["returns"] = value
            pending = None
        i += 1
    if current:
        examples.append(current)
    return [ex for ex in examples if ex["inputs"] and ex["returns"] is not None]


def main() -> int:
    spec = ROOT / "specs" / "optimize_picnic_basket.angl"
    examples = _extract_examples(spec.read_text())
    failures = []
    for example in examples:
        actual = optimize_picnic_basket(
            example["inputs"]["items"],
            example["inputs"]["constraints"],
        )
        if actual != example["returns"]:
            failures.append((example["name"], actual, example["returns"]))
            print(f"FAIL {example['name']}")
            print("  actual:  ", json.dumps(actual, sort_keys=True))
            print("  expected:", json.dumps(example["returns"], sort_keys=True))
        else:
            print(f"PASS {example['name']}")
    print(f"\n{len(examples) - len(failures)}/{len(examples)} Angl examples passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
