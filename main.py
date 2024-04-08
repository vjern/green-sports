import argparse
import json
import re
import sys
from typing import Iterable


def process(data: Iterable[str]) -> Iterable[str]:
    for i, row in enumerate(data):
        row = row.strip()
        new_data = "Rien à afficher"
        if not i % 5:
            new_data = "Multiple de 5"
        elif "$" in row:
            new_data = re.sub(r"\s", "_", row)
        elif row.endswith("."):
            new_data = row
        elif row.startswith("{"):
            decoded = json.loads(row)
            decoded["pair"] = not i % 2
            new_data = json.dumps(decoded)
        yield new_data


def main(argv: list[str] = sys.argv[1:]):

    parser = argparse.ArgumentParser()
    parser.add_argument("filepath")

    args = parser.parse_args(argv)

    with open(args.filepath) as f:
        data = process(f)
        for i, row in enumerate(data):
            print(f"{i} : {row}")


def test_rules():
    assert list(
        process(
            [
                "Line dot.",
                "Line dot.",
                json.dumps({"a": 3}),
                json.dumps({"b": 4}),
                f"The price is $$$\ttoo expensive?",
                "$$$ a $$$",
                "no condition",
                json.dumps({"b": 5}) + ".",
            ]
        )
    ) == [
        "Multiple de 5",
        "Line dot.",
        json.dumps({"a": 3, "pair": True}),
        json.dumps({"b": 4, "pair": False}),
        "The_price_is_$$$_too_expensive?",
        "Multiple de 5",
        "Rien à afficher",
        json.dumps({"b": 5}) + ".",
    ]


if __name__ == "__main__":
    main()
