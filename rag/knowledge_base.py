from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

KNOWLEDGE = [
    "Interview: Thank the recruiter, confirm interest and ask for available interview slots.",
    "Refund: Acknowledge the payment issue, request the transaction reference and avoid promising an unverified refund.",
    "Meeting: Confirm the meeting request and ask for the preferred time and agenda.",
    "Professional communication: Keep replies polite, clear and concise."
]

def retrieve_context(query, top_k=2):
    if not query.strip():
        return ""

    vectorizer = TfidfVectorizer(stop_words="english")

    matrix = vectorizer.fit_transform(
        KNOWLEDGE + [query]
    )

    scores = cosine_similarity(
        matrix[-1], matrix[:-1]
    ).flatten()

    ranked = scores.argsort()[::-1][:top_k]

    results = [
        KNOWLEDGE[i]
        for i in ranked
        if scores[i] > 0
    ]

    return "\n".join(results)
