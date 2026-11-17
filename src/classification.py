
def classify_issue(review):
    """
    Identify customer complaint categories using keyword matching.
    Avoid classifying positive payment experiences as complaints.
    """

    text = review.lower()

    categories = {
        "Delivery": [
            "delivery", "shipping", "late", "delayed",
            "arrived late", "package", "tracking"
        ],

        "Product Quality": [
            "quality", "broken", "damaged", "defective",
            "stopped working", "malfunction", "replacement"
        ],

        "Customer Support": [
            "support", "service", "staff", "complaint",
            "responded", "helped", "contacted", "calls",
            "ignored", "follow-up", "nobody helped",
            "no response", "not responded"
        ],

        "Payment & Refund": [
            "refund", "payment failed", "payment issue",
            "payment problem", "payment error",
            "charged", "deducted", "reimbursement",
            "money back", "charged twice",
            "incorrect charge", "unauthorized charge",
            "billing error", "billing issue",
            "transaction failed"
        ],

        "Pricing": [
            "expensive", "overpriced", "high price",
            "too costly", "price is too high"
        ]
    }

    detected_categories = []

    for category, keywords in categories.items():
        if any(keyword in text for keyword in keywords):
            detected_categories.append(category)

    if not detected_categories:
        return "Other"

    return ", ".join(detected_categories)
