
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "reviews.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS review_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                review TEXT NOT NULL,
                rating INTEGER NOT NULL,
                sentiment TEXT,
                confidence REAL,
                category TEXT,
                priority TEXT,
                reason TEXT,
                suggested_response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_analysis(result):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO review_history (
                review, rating, sentiment, confidence,
                category, priority, reason, suggested_response
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result["Review"],
            result["Rating"],
            result["Sentiment"],
            result["Confidence"],
            result["Category"],
            result["Priority"],
            result["Reason"],
            result["Suggested Response"]
        ))


def get_history():
    with get_connection() as connection:
        return connection.execute("""
            SELECT
                id, review, rating, sentiment, confidence,
                category, priority, reason, suggested_response,
                created_at
            FROM review_history
            ORDER BY created_at DESC, id DESC
        """).fetchall()
