def analyze_email(subject, body):
    text = f"{subject} {body}".lower()

    if any(x in text for x in ["interview", "recruiter"]):
        intent = "Interview Coordination"
    elif any(x in text for x in ["refund", "payment", "failed"]):
        intent = "Payment Support"
    elif any(x in text for x in ["meeting", "schedule"]):
        intent = "Meeting Request"
    elif any(x in text for x in ["question", "information"]):
        intent = "Information Request"
    else:
        intent = "General Communication"

    negative = ["failed", "problem", "issue", "delay"]
    positive = ["thank", "great", "happy", "appreciate"]

    if any(x in text for x in negative):
        sentiment = "Concerned"
    elif any(x in text for x in positive):
        sentiment = "Positive"
    else:
        sentiment = "Neutral"

    return {
        "intent": intent,
        "sentiment": sentiment
    }
