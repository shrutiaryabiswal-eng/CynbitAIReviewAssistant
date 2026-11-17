
def classify_issue(review):
    """
    Identify all relevant issues mentioned in a customer review.
    Returns a comma-separated string to remain compatible
    with the existing application.
    """
    text = review.lower()

    categories = {
        "Delivery": [
            "delivery", "shipping", "late", "delayed",
            "arrived", "package", "tracking"
        ],
        "Product Quality": [
            "quality", "broken", "damaged", "defective",
            "stopped working", "malfunction", "replacement"
        ],
        "Customer Support": [
            "support", "service", "staff", "complaint",
            "responded", "helped", "contacted", "calls",
            "ignored", "follow-up"
        ],
        "Payment & Refund": [
            "refund", "payment", "money", "charged",
            "deducted", "reimbursement"
        ],
        "Pricing": [
            "price", "expensive", "cost", "overpriced",
            "charges"
        ]
    }

    detected_categories = []

    for category, keywords in categories.items():
        if any(keyword in text for keyword in keywords):
            detected_categories.append(category)

    if not detected_categories:
        return "Other"

    return ", ".join(detected_categories)
