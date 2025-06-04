import json
from sentence_transformers import SentenceTransformer, util
import os

# Cargar modelo de embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# Cargar preguntas y respuestas conocidas
with open("data/faq.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

questions = [item["question"] for item in faq_data]
answers = [item["answer"] for item in faq_data]

# Preprocesar embeddings de preguntas
question_embeddings = model.encode(questions, convert_to_tensor=True)

# Ruta del archivo para preguntas no respondidas
UNANSWERED_FILE = "data/unanswered.json"

def save_unanswered_question(question):
    # Cargar las existentes o crear una lista nueva
    if os.path.exists(UNANSWERED_FILE):
        with open(UNANSWERED_FILE, "r", encoding="utf-8") as f:
            unanswered = json.load(f)
    else:
        unanswered = []

    # Evitar guardar duplicados
    if any(entry["question"].lower() == question.lower() for entry in unanswered):
        return

    unanswered.append({
        "question": question,
        "answer": ""
    })

    with open(UNANSWERED_FILE, "w", encoding="utf-8") as f:
        json.dump(unanswered, f, ensure_ascii=False, indent=2)

def get_semantic_response(user_question):
    user_embedding = model.encode(user_question, convert_to_tensor=True)
    similarities = util.cos_sim(user_embedding, question_embeddings)[0]

    best_match_idx = similarities.argmax().item()
    best_score = similarities[best_match_idx].item()

    if best_score > 0.6:
        return answers[best_match_idx]
    else:
        save_unanswered_question(user_question)
        return None
