import json
from datetime import datetime

from app.config import LOG_FILE


def log_response(user_query, response, source="faq", score=None, fallback_reason=None):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_query": user_query,
        "response": response,
        "source": source,
    }

    if score:
        entry["score"] = score
    if fallback_reason:
        entry["fallback_reason"] = fallback_reason

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

