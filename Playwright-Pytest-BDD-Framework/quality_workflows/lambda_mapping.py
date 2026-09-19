"""Offline AWS Lambda-style contract example; does not connect to AWS."""

import json


def handler(event, context=None):
    # Explicit allowlist: do not copy arbitrary source fields to the downstream payload.
    if event.get("source") != "synthetic" or not str(event.get("id", "")).startswith(
        "SYN-"
    ):
        raise ValueError("Only generated sample records are accepted")
    quantity = event.get("quantity")
    if type(quantity) is not int or not 1 <= quantity <= 10:
        return {"statusCode": 400, "body": json.dumps({"error": "invalid_quantity"})}
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "correlation_id": event["id"],
                "quantity": quantity,
                "total_cents": quantity * 1250,
                "status": "validated",
            }
        ),
    }


if __name__ == "__main__":
    print(handler({"source": "synthetic", "id": "SYN-0001", "quantity": 2}))
