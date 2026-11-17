def generate_reply(email, classification, analysis, context=""):

    category = classification["category"]

    if category == "Career":
        reply = """
Thank you for the interview invitation.

I appreciate the opportunity and would be happy
to attend the interview.

Could you please share the available time slots
and any preparation details?

"""
    elif category == "Support":
        reply = """
Thank you for bringing this issue to our attention.

I'm sorry for the inconvenience.

Please share your transaction reference and
payment details so the issue can be investigated.

We will review the details and advise you
on the next steps.

"""
    elif category == "Work":
        reply = """
Thank you for the update.

I would be happy to discuss the project.

Please share the proposed meeting time and
agenda so I can prepare accordingly.

"""
    elif category == "Personal":
        reply = """
Hey!

Thanks for reaching out.

I'd be happy to catch up. Let me check my
schedule and get back to you.

"""
    else:
        reply = """
Thank you for your email.

I've received your message and will review
the details.

I'll get back to you shortly.

"""

    context_note = ""

    if context:
        context_note = (
            "\nContext considered:\n" + context + "\n"
        )

    return (
        f"Hi,\n\n{reply}"
        f"{context_note}"
        "\nBest regards,\nMailGenix AI User"
    )
