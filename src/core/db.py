from functools import wraps
import sqlite3

from core import config, schemes


def connection(commit=False):
    def _connection(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with sqlite3.connect(config.DATABASE) as connection:
                cursor = connection.cursor()
                
                result = func(cursor, *args, **kwargs)
                if commit:
                    connection.commit()
                return result
        return wrapper
    return _connection
        

@connection()
def init_db(cursor: sqlite3.Cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            created_at TEXT NOT NULL,
            CONSTRAINT sentiment_choices CHECK (sentiment IN ('negative', 'positive', 'neutral'))
        )
        """
    )

@connection(commit=True)
def create_review(cursor: sqlite3.Cursor, review) -> int:
    result = cursor.execute(
        f"""
        INSERT INTO reviews (text, sentiment, created_at) VALUES (
            '{review.text}', '{review.sentiment}', '{review.created_at}'
        )
        """
    )
    return result.lastrowid

@connection()
def get_review_by_id(cursor: sqlite3.Cursor, id: int):
    result = cursor.execute(
        f"""
        SELECT * FROM reviews WHERE id = {id}
        """
    )
    result.row_factory = sqlite3.Row
    return dict(result.fetchone())

@connection()
def search_reviews(cursor: sqlite3.Cursor, params: schemes.SearchReviews):
    results = cursor.execute(
        f"""
        SELECT * FROM reviews WHERE sentiment IN {params.sentiment}
        LIMIT {params.limit} OFFSET {params.offset}
        """
    )
    results.row_factory = sqlite3.Row
    return map(dict, results.fetchall())
