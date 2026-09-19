"""Deterministic test data generated without reading any personal information."""

import json


def generate(count=20):
    if not 1 <= count <= 1000:
        raise ValueError("Use 1-1000 synthetic records")
    return [
        {
            "id": f"SYN-{i:04d}",
            "email": f"fixture{i:04d}@example.invalid",
            "quantity": [0, 1, 2, 10, 11][(i - 1) % 5],
            "source": "synthetic",
        }
        for i in range(1, count + 1)
    ]


if __name__ == "__main__":
    print(json.dumps(generate(), indent=2))
