
def detect_priority(review, sentiment, rating):
    text = review.lower()

    urgent_terms = [
        "urgent",
        "immediately",
        "multiple times",
        "twice",
        "nobody responded",
        "nobody has responded",
        "not responded",
        "unresolved",
        "money back",
        "full refund",
        "replacement",
        "damaged",
        "broken",
        "defective",
        "charged twice"
    ]

    payment_terms = [
        "refund",
        "payment",
        "charged",
        "deducted",
        "money back"
    ]

    reasons = []

    if rating <= 2:
        reasons.append("Low customer rating")

    if sentiment == "negative":
        reasons.append("Negative sentiment")

    has_urgent_issue = any(term in text for term in urgent_terms)

    if has_urgent_issue:
        reasons.append("Urgent customer issue detected")

    if any(term in text for term in payment_terms):
        reasons.append("Payment or refund issue")

    if rating <= 2 and sentiment == "negative" and has_urgent_issue:
        priority = "High"
    elif rating <= 2 or sentiment == "negative":
        priority = "Medium"
    else:
        priority = "Low"

    return {
        "priority": priority,
        "reasons": reasons
    }
