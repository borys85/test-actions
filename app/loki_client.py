import os
import time
from typing import Any

import httpx

LOKI_URL = os.getenv("LOKI_URL", "http://localhost:3100")
LOKI_PUSH_URL = f"{LOKI_URL.rstrip('/')}/loki/api/v1/push"
APP_LABEL = "my_app"


def send_log_to_loki(message: str, level: str = "info", extra_labels: dict[str, str] | None = None) -> dict[str, Any]:
    """Отправляет лог-сообщение в Loki через HTTP POST на /loki/api/v1/push."""
    labels = {"app": APP_LABEL, "level": level}
    if extra_labels:
        labels.update(extra_labels)

    timestamp_ns = str(int(time.time() * 1_000_000_000))
    payload = {
        "streams": [
            {
                "stream": labels,
                "values": [[timestamp_ns, message]],
            }
        ]
    }

    response = httpx.post(
        LOKI_PUSH_URL,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=5.0,
    )
    response.raise_for_status()
    return {"status": "sent", "labels": labels, "message": message}
