from typing import List

from core import db, schemes

def paginate_qs(qs: list, params: schemes.Pagination) -> dict:
    limit = params.limit
    offset = params.offset
    items = list(qs)
    return {
        "limit": limit,
        "offset": offset + limit,
        "total": len(items),
        "items": items[offset : limit+offset]
    }


def create_review(review: schemes.Review) -> int:
    id = db.create_review(review)
    return db.get_review_by_id(id)

def search_reviews(params: schemes.SearchReviews) -> List[schemes.Review]:
    params.sentiment = schemes.as_tuple(params.sentiment)
    reviews = db.search_reviews(params)
    return paginate_qs(reviews, params)