import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

from app.faq import faq_data
from app.config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, EMBEDDING_MODEL


client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

model = SentenceTransformer(EMBEDDING_MODEL)
print(f"📦 Loaded embedding model: {EMBEDDING_MODEL}")


# ---- Create Collection ----
def create_collection():

    coll_exists = client.collection_exists(collection_name=COLLECTION_NAME)

    if not coll_exists:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        print(f"✅ Collection '{COLLECTION_NAME}' created.")
    else:
        print(f"ℹ️ Collection '{COLLECTION_NAME}' already exists.")


# ---- Index FAQ ----
def index_faq():
    points = []
    for i, item in enumerate(faq_data):
        vector = model.encode(item["question"]).tolist()
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"question": item["question"], "answer": item["answer"]}
            )
        )
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"✅ Indexed {len(points)} FAQs into '{COLLECTION_NAME}'")


# ---- Search ----
def search_faq(user_input, threshold=0.4):
    query_vector = model.encode(user_input).tolist()

    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=1,
        score_threshold=threshold,
        with_payload=True
    )

    if hits:
        answer = hits[0].payload["answer"]
        score = hits[0].score
        return answer, score

    return "__fallback__", None

