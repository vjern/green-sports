import argparse
import json
import re
import sys
from typing import Iterable


def process(data: Iterable[str]) -> Iterable[str]:
    for i, row in enumerate(data):
        row = row.strip()
        if not i % 5:
            yield "Multiple de 5"
        elif "$" in row:
            yield re.sub(r"\s", "_", row)
        elif row.endswith("."):
            yield row
        elif row.startswith("{"):
            decoded = json.loads(row)
            decoded["pair"] = not i % 2
            yield json.dumps(decoded)
        else:
            yield "Rien à afficher"


def main(argv: list[str] = sys.argv[1:]):

    parser = argparse.ArgumentParser()
    parser.add_argument("filepath")

    args = parser.parse_args(argv)

    with open(args.filepath) as f:
        data = process(f)
        for row in data:
            print(row)


def test_rules():
    assert list(
        process(
            [
                "Line dot.",
                "Line dot.",
                json.dumps({"a": 3}),
                json.dumps({"b": 4}),
                f"The price is $$$\ttoo expensive?",
                "no condition",
            ]
        )
    ) == [
        "Multiple de 5",
        "Line dot.",
        json.dumps({"a": 3, "pair": True}),
        json.dumps({"b": 4, "pair": False}),
        "The_price_is_$$$_too_expensive?",
        "Multiple de 5",
    ]


if __name__ == "__main__":
    main()
