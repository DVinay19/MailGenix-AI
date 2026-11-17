from core.classifier import classify_email
from core.email_analyzer import analyze_email
from rag.knowledge_base import retrieve_context


def test_career_classification():
    result = classify_email(
        "Interview Invitation",
        "Please confirm your interview availability."
    )

    assert result["category"] == "Career"


def test_support_classification():
    result = classify_email(
        "Refund Request",
        "My payment failed."
    )

    assert result["category"] == "Support"


def test_email_intent():
    result = analyze_email(
        "Meeting Request",
        "Please schedule a meeting."
    )

    assert result["intent"] == "Meeting Request" or result["intent"] == "Schedule a meeting"


def test_knowledge_retrieval():
    result = retrieve_context("interview scheduling recruiter")

    assert "Interview" in result
