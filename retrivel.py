import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def retrieve_documents(query, top_k=3):
    database_path = Path(__file__).with_name("database.json")

    with open(database_path, "r", encoding="utf-8") as file:
        database = json.load(file)

    if not database or not query.strip():
        return []

    documents = [
        f"{item.get('title', '')} {item.get('content', '')}"
        for item in database
    ]

    vectorizer = TfidfVectorizer()
    document_vectors = vectorizer.fit_transform(documents)
    query_vector = vectorizer.transform([query])

    scores = cosine_similarity(
        query_vector, document_vectors
    ).flatten()

    ranked_indices = scores.argsort()[::-1]

    results = []

    for index in ranked_indices:
        if scores[index] <= 0:
            continue

        results.append(database[index])

        if len(results) >= top_k:
            break

    return results