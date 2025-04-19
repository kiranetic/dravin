import os
from pathlib import Path
from dotenv import load_dotenv


# Load from project root .env
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
ENV_FILE = PROJECT_ROOT / ".env"

# Logging
JSON_LOG = PROJECT_ROOT / "dlogs.jsonl"
CSV_LOG = PROJECT_ROOT / "dlogs.csv"


load_dotenv(dotenv_path=ENV_FILE)

# Timezone
TZ = os.getenv("TIMEZONE", "UTC")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

# Qdrant
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "dravin_faq")

