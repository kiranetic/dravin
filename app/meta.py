from app.config import OPENAI_MODEL, QDRANT_URL, EMBEDDING_MODEL
from app.faq import faq_data


VERSION = "0.1.0-beta"


APP_METADATA = {
    "app_name": "Dravin",
    "version": VERSION,
    "vector_db": "Qdrant",
    "embedding_model": EMBEDDING_MODEL,
    "openai_model": OPENAI_MODEL,
    "qdrant_url": QDRANT_URL,
    "faq_count": len(faq_data),
    "gpt_fallback_enabled": True,
    "logging": ["csv", "jsonl"]
}
