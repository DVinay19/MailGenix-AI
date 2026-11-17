import streamlit as st
import pandas as pd

from database.db import (
    init_db,
    seed_emails,
    get_emails,
    get_email,
    save_draft,
    update_status,
    get_metrics
)

from core.classifier import classify_email
from core.email_analyzer import analyze_email
from core.response_generator import generate_reply
from rag.knowledge_base import retrieve_context


st.set_page_config(
    page_title="MailGenix AI",
    page_icon="✉️",
    layout="wide"
)

init_db()
seed_emails()


# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>

.stApp {
    background: #0B1020;
    color: #E8EDF7;
}

[data-testid="stSidebar"] {
    background: #10182B;
}

.block-container {
    padding-top: 2rem;
    max-width: 1450px;
}

div[data-testid="stMetric"] {
    background: #141F35;
    border: 1px solid #263653;
    padding: 18px;
    border-radius: 14px;
}

.stButton button {
    border-radius: 9px;
    font-weight: 600;
    min-height: 42px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("# ✉️ MailGenix AI")

    st.caption("Intelligent Emails. Human Control.")

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Smart Inbox",
            "Knowledge Base",
            "About"
        ]
    )

    st.divider()

    st.success("Human approval enabled")

    st.caption("Local demonstration mode")


# ---------------- HEADER ----------------

st.title("MailGenix AI")

st.caption(
    "AI-powered email intelligence and automation platform."
)


# ---------------- OVERVIEW ----------------

if page == "Overview":

    metrics = get_metrics()

    st.subheader("Workspace Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Emails", metrics["total"])
    c2.metric("Pending Review", metrics["pending"])
    c3.metric("Approved", metrics["approved"])
    c4.metric("Rejected", metrics["rejected"])

    st.divider()

    st.subheader("Recent Emails")

    emails = get_emails()

    if emails:

        df = pd.DataFrame(emails)

        st.dataframe(
            df[
                [
                    "sender",
                    "subject",
                    "status"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


# ---------------- SMART INBOX ----------------

elif page == "Smart Inbox":

    emails = get_emails()

    left, right = st.columns(
        [1, 1.8],
        gap="large"
    )

    with left:

        st.subheader("Your Inbox")

        search = st.text_input(
            "Search emails",
            placeholder="Search sender or subject..."
        )

        status_filter = st.selectbox(
            "Filter status",
            ["All", "Pending", "Approved", "Rejected"]
        )

        filtered = [
            e for e in emails
            if search.lower() in (
                e["sender"] + e["subject"] + e["body"]
            ).lower()
            and (
                status_filter == "All"
                or e["status"] == status_filter
            )
        ]

        options = {
            f'{e["id"]} · {e["subject"]}': e["id"]
            for e in filtered
        }

        selected_id = None

        if options:

            selected = st.radio(
                "Select an email",
                list(options.keys())
            )

            selected_id = options[selected]

        else:

            st.info("No emails found.")


    # ---------------- EMAIL DETAILS ----------------

    with right:

        if selected_id:

            email = get_email(selected_id)

            st.subheader(email["subject"])

            st.caption(
                f'{email["sender"]} · {email["received"]}'
            )

            st.markdown("### Email Content")

            st.write(email["body"])

            # CLASSIFICATION

            classification = classify_email(
                email["subject"],
                email["body"]
            )

            analysis = analyze_email(
                email["subject"],
                email["body"]
            )

            st.divider()

            st.subheader("AI Email Intelligence")

            a, b, c = st.columns(3)

            a.metric(
                "Category",
                classification["category"]
            )

            b.metric(
                "Priority",
                classification["priority"]
            )

            c.metric(
                "Intent",
                analysis["intent"]
            )

            st.caption(
                f'Sentiment: {analysis["sentiment"]}'
            )

            # RAG RETRIEVAL

            context = retrieve_context(
                email["subject"] + " " + email["body"]
            )

            with st.expander("Retrieved Knowledge"):

                st.write(
                    context if context
                    else "No relevant knowledge found."
                )

            # GENERATE REPLY

            st.divider()

            if st.button(
                "✨ Generate AI Reply",
                type="primary",
                use_container_width=True
            ):

                draft = generate_reply(
                    email,
                    classification,
                    analysis,
                    context
                )

                save_draft(selected_id, draft)

                st.session_state[
                    f"draft_{selected_id}"
                ] = draft

                st.rerun()

            # DRAFT EDITOR

            saved_draft = email["draft"] or ""

            draft_value = st.session_state.get(
                f"draft_{selected_id}",
                saved_draft
            )

            draft = st.text_area(
                "Review and edit your response",
                value=draft_value,
                height=220,
                key=f"editor_{selected_id}"
            )

            if draft.strip():

                st.divider()

                x, y = st.columns(2)

                with x:

                    if st.button(
                        "✓ Approve Draft",
                        type="primary",
                        use_container_width=True
                    ):

                        save_draft(
                            selected_id,
                            draft
                        )

                        update_status(
                            selected_id,
                            "Approved"
                        )

                        st.success(
                            "Draft approved and saved."
                        )

                        st.rerun()

                with y:

                    if st.button(
                        "✕ Reject Draft",
                        use_container_width=True
                    ):

                        update_status(
                            selected_id,
                            "Rejected"
                        )

                        st.warning(
                            "Draft rejected."
                        )

                        st.rerun()

            st.info(
                "Approval only records your decision. "
                "This version does not send emails."
            )


# ---------------- KNOWLEDGE BASE ----------------

elif page == "Knowledge Base":

    st.subheader("Knowledge Base")

    st.write(
        "Reference information used to ground AI-generated replies."
    )

    st.markdown("""
    **Interview scheduling**

    Confirm interest and ask for available time slots.

    **Refund support**

    Acknowledge the issue and request transaction details.

    **Meeting requests**

    Confirm receipt and ask for the meeting agenda.

    **Professional communication**

    Keep responses clear, concise and polite.
    """)


# ---------------- ABOUT ----------------

elif page == "About":

    st.subheader("About MailGenix AI")

    st.write("""
    MailGenix AI is an intelligent email assistant
    built using Python, NLP, retrieval techniques
    and human-in-the-loop approval.

    It helps users understand incoming emails,
    classify messages and prepare professional replies.
    """)

    st.markdown("""
    ### Technology Stack

    - Python
    - Streamlit
    - NLP
    - Scikit-learn
    - TF-IDF Retrieval
    - SQLite
    """)

    st.markdown("""
    ### Safety

    - Human approval is mandatory.
    - Users can edit generated drafts.
    - No automatic email sending.
    - Approval records are stored locally.
    """)
