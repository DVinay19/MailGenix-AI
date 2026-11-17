import sqlite3
from pathlib import Path

DB_PATH = "data/mailgenix.db"

SAMPLE_EMAILS = [
    (
        "sarah@example.com",
        "Project Meeting",
        "I would like to schedule a meeting tomorrow to discuss our AI project.",
        "2026-11-18 09:30"
    ),
    (
        "hr@company.example",
        "Interview Invitation",
        "Your profile has been shortlisted. Please confirm your availability for an interview.",
        "2026-11-18 10:15"
    ),
    (
        "support@example.com",
        "Payment Refund Request",
        "My payment failed but the amount was deducted. Please help me resolve this issue.",
        "2026-11-18 10:45"
    ),
    (
        "alex@example.com",
        "Weekend Plans",
        "Are you free this weekend? Let's catch up over coffee.",
        "2026-11-18 11:00"
    )
]


def connect():
    Path("data").mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    with connect() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            subject TEXT,
            body TEXT,
            received TEXT,
            status TEXT DEFAULT 'Pending',
            draft TEXT DEFAULT ''
        )
        """)


def seed_emails():
    with connect() as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM emails"
        ).fetchone()[0]

        if count == 0:
            conn.executemany("""
            INSERT INTO emails
            (sender, subject, body, received)
            VALUES (?, ?, ?, ?)
            """, SAMPLE_EMAILS)


def get_emails():
    with connect() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM emails ORDER BY id DESC"
        ).fetchall()

        return [dict(row) for row in rows]


def get_email(email_id):
    with connect() as conn:
        conn.row_factory = sqlite3.Row

        row = conn.execute(
            "SELECT * FROM emails WHERE id=?",
            (email_id,)
        ).fetchone()

        return dict(row) if row else None


def save_draft(email_id, draft):
    with connect() as conn:
        conn.execute(
            "UPDATE emails SET draft=? WHERE id=?",
            (draft, email_id)
        )


def update_status(email_id, status):
    if status not in ["Pending", "Approved", "Rejected"]:
        raise ValueError("Invalid status")

    with connect() as conn:
        conn.execute(
            "UPDATE emails SET status=? WHERE id=?",
            (status, email_id)
        )


def get_metrics():
    emails = get_emails()

    return {
        "total": len(emails),
        "pending": sum(e["status"] == "Pending" for e in emails),
        "approved": sum(e["status"] == "Approved" for e in emails),
        "rejected": sum(e["status"] == "Rejected" for e in emails)
    }
