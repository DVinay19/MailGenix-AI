
# ✉️ MailGenix AI

### Intelligent Emails. Smarter Decisions. Human Control.

MailGenix AI is an AI-powered email intelligence platform that helps users classify incoming emails, understand intent, retrieve relevant knowledge and generate professional responses with human approval.

## Features

- Smart Email Inbox
- Email Classification
- Priority Detection
- Intent and Sentiment Analysis
- Retrieval-Augmented Context
- AI Reply Drafting
- Editable Responses
- Human Approval Workflow
- SQLite Database
- Analytics Dashboard

## Technology Stack

- Python
- Streamlit
- NLP
- Scikit-learn
- TF-IDF
- SQLite
- Pandas

## Installation

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Architecture

Incoming Email → Classification → Intent Analysis → Knowledge Retrieval → Response Generation → Human Approval

## Safety

MailGenix AI requires human review before a draft is approved. This prototype does not automatically send emails or connect to external email accounts.

## Future Improvements

- Gmail OAuth Integration
- Local LLM Integration
- Advanced RAG
- Email Attachments
- Automated Evaluation
- Cloud Deployment
