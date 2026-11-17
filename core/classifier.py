def classify_email(subject, body):
    text = f"{subject} {body}".lower()

    categories = {
        "Career": ["interview", "job", "recruiter", "application", "resume"],
        "Support": ["refund", "payment", "issue", "failed", "support"],
        "Work": ["meeting", "project", "deadline", "report", "team"],
        "Personal": ["weekend", "coffee", "family", "birthday"]
    }

    category = "General"

    for name, keywords in categories.items():
        if any(word in text for word in keywords):
            category = name
            break

    urgent_words = ["urgent", "asap", "immediately"]
    high_words = ["interview", "meeting", "payment", "refund"]

    if any(word in text for word in urgent_words):
        priority = "Urgent"
    elif any(word in text for word in high_words):
        priority = "High"
    else:
        priority = "Normal"

    return {
        "category": category,
        "priority": priority
    }
