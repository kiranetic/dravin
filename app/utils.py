from sentence_transformers import SentenceTransformer, util
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_best_match(user_input, faq_data, threshold=0.6):
    questions = []
    for entry in faq_data:
        questions.append(entry["question"])

    user_embedding = model.encode(user_input, convert_to_tensor=True)
    faq_embeddings = model.encode(questions, convert_to_tensor=True)

    cosine_scores = util.pytorch_cos_sim(user_embedding, faq_embeddings)[0]

    # Find best match
    best_idx = int(np.argmax(cosine_scores))
    best_score = float(cosine_scores[best_idx])

    if best_score >= threshold:
        return faq_data[best_idx]["answer"]

    return "Sorry, I didn't understand that. Can you please rephrase?"
