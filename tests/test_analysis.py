
import pytest

from src.preprocessing import clean_text
from src.sentiment import SentimentAnalyzer
from src.classification import classify_issue
from src.priority import detect_priority
from src.response_generator import generate_response
import src.database as database


def test_clean_text():
    result = clean_text("GREAT Product!!! Visit www.example.com")
    assert result == "great product visit"


def test_classify_multiple_issues():
    review = (
        "My delivery was late, the product was damaged, "
        "and customer support ignored my refund request."
    )

    result = classify_issue(review)

    assert "Delivery" in result
    assert "Product Quality" in result
    assert "Customer Support" in result
    assert "Payment & Refund" in result


def test_high_priority_detection():
    review = (
        "My order was damaged and nobody responded. "
        "I want a full refund immediately."
    )

    result = detect_priority(review, "negative", 2)

    assert result["priority"] == "High"
    assert len(result["reasons"]) > 0


def test_low_priority_detection():
    review = "Excellent product and very good experience."

    result = detect_priority(review, "positive", 5)

    assert result["priority"] == "Low"


def test_negative_response_generation():
    response = generate_response(
        "My product is damaged.",
        "negative",
        "Product Quality"
    )

    assert isinstance(response, str)
    assert len(response) > 0
    assert "sorry" in response.lower()


def test_sentiment_model_prediction():
    reviews = [
        "Excellent product and amazing service",
        "Very happy with my purchase",
        "Wonderful experience and great quality",
        "Terrible product and very poor service",
        "I hate this product and bad experience",
        "Very disappointed with the purchase",
        "The product is average",
        "Service was okay",
        "Nothing special, just an ordinary experience"
    ]

    ratings = [5, 4, 5, 1, 2, 1, 3, 3, 3]

    analyzer = SentimentAnalyzer()
    analyzer.train(reviews, ratings)

    result = analyzer.predict(
        "Excellent quality and wonderful experience"
    )

    assert result["sentiment"] in [
        "positive", "negative", "neutral"
    ]

    assert 0 <= result["confidence"] <= 1


def test_database_save_and_history(tmp_path, monkeypatch):
    test_db = tmp_path / "test_reviews.db"

    monkeypatch.setattr(database, "DB_PATH", test_db)

    database.initialize_database()

    result = {
        "Review": "Test customer review",
        "Rating": 1,
        "Sentiment": "negative",
        "Confidence": 0.85,
        "Category": "Delivery",
        "Priority": "High",
        "Reason": "Low rating",
        "Suggested Response": "We are sorry."
    }

    database.save_analysis(result)

    history = database.get_history()

    assert len(history) == 1
    assert history[0][1] == "Test customer review"
    assert history[0][6] == "High"

def test_positive_payment_not_classified_as_complaint():
    review = "Good value for money. Smooth payment process and helpful staff."

    result = classify_issue(review)

    assert "Payment & Refund" not in result


def test_actual_payment_complaint_is_detected():
    review = "I was charged twice and my refund has not arrived."

    result = classify_issue(review)

    assert "Payment & Refund" in result

def test_positive_payment_review_not_flagged():
    review = "Good value for money. Smooth payment process and helpful staff."

    result = detect_priority(review, "positive", 5)

    assert result["priority"] == "Low"
    assert "Payment or refund issue" not in result["reasons"]


def test_low_rating_positive_review_not_flagged_as_payment_issue():
    review = "The experience was good and the payment process was smooth."

    result = detect_priority(review, "positive", 2)

    assert result["priority"] == "Medium"
    assert "Low customer rating" in result["reasons"]
    assert "Payment or refund issue" not in result["reasons"]


def test_actual_refund_complaint_is_flagged():
    review = "I was charged twice and my refund has not arrived."

    result = detect_priority(review, "negative", 2)

    assert result["priority"] == "High"
    assert "Payment or refund issue" in result["reasons"]
