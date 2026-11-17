
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from src.preprocessing import clean_text


class SentimentAnalyzer:

    def __init__(self):
        self.model = Pipeline([
            (
                "tfidf",
                TfidfVectorizer(
                    preprocessor=clean_text,
                    ngram_range=(1, 2),
                    max_features=3000
                )
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=42
                )
            )
        ])

    def get_labels(self, ratings):
        """Convert customer ratings into sentiment labels."""
        labels = []

        for rating in ratings:
            rating = int(rating)

            if rating >= 4:
                labels.append("positive")
            elif rating <= 2:
                labels.append("negative")
            else:
                labels.append("neutral")

        return labels

    def train(self, reviews, ratings):
        """Train the sentiment classification model."""
        if len(reviews) != len(ratings):
            raise ValueError("Reviews and ratings must have equal lengths.")

        if len(reviews) < 6:
            raise ValueError("At least 6 reviews are required for training.")

        labels = self.get_labels(ratings)

        self.model.fit(reviews, labels)

    def predict(self, review):
        """Predict sentiment and return model confidence."""
        prediction = self.model.predict([review])[0]

        probabilities = self.model.predict_proba([review])[0]

        confidence = max(probabilities)

        return {
            "sentiment": prediction,
            "confidence": round(float(confidence), 3)
        }

    def evaluate(self, reviews, ratings):
        """
        Evaluate performance on a held-out test set.
        Evaluation results are based on rating-derived labels.
        """
        labels = self.get_labels(ratings)

        X_train, X_test, y_train, y_test = train_test_split(
            reviews,
            labels,
            test_size=0.25,
            random_state=42,
            stratify=labels
        )

        evaluation_model = Pipeline([
            (
                "tfidf",
                TfidfVectorizer(
                    preprocessor=clean_text,
                    ngram_range=(1, 2),
                    max_features=3000
                )
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=42
                )
            )
        ])

        evaluation_model.fit(X_train, y_train)

        predictions = evaluation_model.predict(X_test)

        return {
            "accuracy": round(
                accuracy_score(y_test, predictions), 3
            ),
            "classification_report": classification_report(
                y_test,
                predictions,
                labels=["negative", "neutral", "positive"],
                output_dict=True,
                zero_division=0
            ),
            "confusion_matrix": confusion_matrix(
                y_test,
                predictions,
                labels=["negative", "neutral", "positive"]
            ).tolist(),
            "test_samples": len(y_test)
        }
