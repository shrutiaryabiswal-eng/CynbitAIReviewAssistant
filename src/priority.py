
def detect_priority(review, sentiment, rating):
    """
    Assign review priority using rating, sentiment, and
    complaint-specific urgency indicators.
    """
    text = review.lower()
    reasons = []

    urgent_terms = [
        "urgent",
        "immediately",
        "multiple times",
        "twice",
        "nobody responded",
        "nobody has responded",
        "not responded",
        "no response",
        "unresolved",
        "money back",
        "full refund",
        "replacement",
        "damaged",
        "broken",
        "defective",
        "charged twice"
    ]

    payment_issue_terms = [
        "refund",
        "payment failed",
        "payment issue",
        "payment problem",
        "payment error",
        "charged",
        "deducted",
        "reimbursement",
        "money back",
        "incorrect charge",
        "unauthorized charge",
        "billing error",
        "billing issue",
        "transaction failed"
    ]

    if rating <= 2:
        reasons.append("Low customer rating")

    if sentiment == "negative":
        reasons.append("Negative sentiment")

    if any(term in text for term in urgent_terms):
        reasons.append("Urgent customer issue detected")

    if any(term in text for term in payment_issue_terms):
        reasons.append("Payment or refund issue")

    if rating <= 2 and sentiment == "negative" and any(
        term in text for term in urgent_terms
    ):
        priority = "High"
    elif rating <= 2 or sentiment == "negative":
        priority = "Medium"
    else:
        priority = "Low"

    return {
        "priority": priority,
        "reasons": reasons
    }
