
def generate_response(review, sentiment, category):
    """
    Generate a suggested customer response.
    This is a template-based demo, not an external LLM.
    """

    if sentiment == "negative":
        response = (
            f"We're sorry to hear about your experience with "
            f"{category.lower()}. Thank you for bringing this "
            "to our attention. Our team would like to investigate "
            "this issue and work towards a resolution. "
            "Please contact our support team with your order details."
        )

    elif sentiment == "positive":
        response = (
            "Thank you for sharing your positive experience! "
            "We truly appreciate your support and look forward "
            "to serving you again."
        )

    else:
        response = (
            "Thank you for your feedback. We appreciate your "
            "suggestions and will use them to improve our service."
        )

    return response
